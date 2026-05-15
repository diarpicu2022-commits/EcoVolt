"""
Implementación concreta de batería de plomo-ácido para el sistema EcoVolt.

Las baterías de plomo-ácido son la tecnología más madura y económica para
almacenamiento en sistemas fotovoltaicos. Aunque tienen menor eficiencia (80%)
y vida útil (500 ciclos) que las de litio, su bajo costo inicial las hace
viables para instalaciones de menor presupuesto o como respaldo de emergencia.
"""
from domain.entities.battery import Battery


class LeadAcidBattery(Battery):
    """
    Nivel 3 — Batería de plomo-ácido de tecnología madura y bajo costo.

    Características técnicas:
    - Eficiencia de ciclo: 80% (0.80) — pérdidas por calor y reacciones secundarias
    - Voltaje nominal: 24V (configuración estándar para sistemas pequeños/medianos)
    - Ciclos de vida típicos: 500 ciclos antes de degradación significativa
    - Densidad energética: ~30-50 Wh/kg — mucho menor que litio
    - Requiere ventilación adecuada por emisión de hidrógeno durante la carga

    La eficiencia del 80% significa que por cada 100 kWh almacenados, solo se
    pueden recuperar 80 kWh útiles. El 20% se pierde como calor y en la
    electrólisis del agua del electrolito durante los ciclos.
    """

    # Ciclos de vida típicos — significativamente menor que litio
    TYPICAL_CYCLE_LIFE: int = 500

    # Voltaje nominal del sistema de 24V (plomo-ácido típicamente trabaja a 12V o 24V)
    NOMINAL_VOLTAGE_VOLTS: float = 24.0

    # Eficiencia de ciclo de carga/descarga del plomo-ácido
    LEAD_ACID_EFFICIENCY: float = 0.80

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        battery_id: str,
        capacity_kwh: float = 5.0,  # Capacidad típica para sistema pequeño
        initial_charge_percentage: float = 50.0,
        initial_cycle_count: int = 0,
    ) -> None:
        """
        Inicializa la batería de plomo-ácido con sus parámetros técnicos.

        :param component_id: ID del componente base.
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param battery_id: Identificador de la batería (p. ej. 'LA-001').
        :param capacity_kwh: Capacidad nominal en kWh (por defecto 5 kWh).
        :param initial_charge_percentage: Nivel de carga inicial (0.0 a 100.0).
        :param initial_cycle_count: Ciclos previos de carga/descarga.
        """
        super().__init__(
            component_id=component_id,
            installation_location=installation_location,
            installation_date=installation_date,
            battery_id=battery_id,
            capacity_kwh=capacity_kwh,
            initial_charge_percentage=initial_charge_percentage,
            initial_cycle_count=initial_cycle_count,
            nominal_voltage=self.NOMINAL_VOLTAGE_VOLTS,
        )

    # -------------------------------------------------------------------------
    # Implementación de métodos abstractos de EnergyComponent y Battery
    # -------------------------------------------------------------------------

    def generate(self) -> float:
        """
        Calcula la energía disponible en la batería de plomo-ácido.

        Retorna la energía útil que la batería puede entregar al sistema.
        Para el plomo-ácido, no se recomienda descargar por debajo del 50%
        (descarga profunda) para preservar la vida útil, pero el sistema
        registra la capacidad total para la gestión de energía.

        :return: Energía disponible en kilovatios-hora (kWh).
        """
        # Energía disponible = capacidad total × fracción de carga actual
        return self._capacity_kwh * (self._current_charge_percentage / 100.0)

    def get_efficiency(self) -> float:
        """
        Retorna la eficiencia de ciclo de la batería de plomo-ácido.

        La eficiencia del 80% refleja las pérdidas por resistencia interna
        mayor, reacciones parásitas de electrólisis y disipación térmica.
        Esta pérdida del 20% por ciclo hace que el plomo-ácido sea menos
        rentable a largo plazo que el litio pese a su menor costo inicial.

        :return: 0.80 — eficiencia del 80%.
        """
        return self.LEAD_ACID_EFFICIENCY

    def get_status(self) -> str:
        """
        Retorna el estado operativo de la batería de plomo-ácido.

        Incluye advertencia adicional si la carga está por debajo del 50%,
        ya que la descarga profunda es especialmente dañina para esta tecnología.

        :return: Cadena descriptiva del estado actual de la batería.
        """
        # Llamar al get_status del padre para obtener el estado base del State Pattern
        base_status = super().get_status()

        # Advertencia específica de plomo-ácido: la descarga profunda daña las placas
        if self._current_charge_percentage < 50.0:
            return f"{base_status} | ADVERTENCIA: Descarga profunda detectada (plomo-ácido)"

        return base_status

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos de la batería de plomo-ácido a un diccionario.

        Incluye información sobre el nivel de descarga profunda para orientar
        las decisiones de gestión energética del sistema.

        :return: Diccionario con todos los campos de la batería para API REST.
        """
        # Calcular salud estimada de la batería según ciclos consumidos
        remaining_cycle_percentage = max(
            0.0,
            ((self.TYPICAL_CYCLE_LIFE - self._cycle_count) / self.TYPICAL_CYCLE_LIFE) * 100.0
        )

        # Indicador de descarga profunda — crítico para preservar la batería de plomo-ácido
        is_deep_discharged = self._current_charge_percentage < 50.0

        return {
            # Campos de identidad heredados de EnergyComponent
            "component_id": self.component_id,
            "installation_location": self.installation_location,
            "installation_date": self.installation_date,
            # Campos específicos de la batería
            "battery_id": self._battery_id,
            "battery_type": "lead_acid",
            "capacity_kwh": self._capacity_kwh,
            "nominal_voltage": self.NOMINAL_VOLTAGE_VOLTS,
            "efficiency": self.LEAD_ACID_EFFICIENCY,
            "typical_cycle_life": self.TYPICAL_CYCLE_LIFE,
            # Estado en tiempo real
            "current_charge_percentage": self._current_charge_percentage,
            "current_voltage": self._current_voltage,
            "cycle_count": self._cycle_count,
            "remaining_cycle_percentage": round(remaining_cycle_percentage, 1),
            "is_deep_discharged": is_deep_discharged,
            # Métricas calculadas
            "available_energy_kwh": self.generate(),
            "status": self.get_status(),
        }
