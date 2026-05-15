"""
Implementación concreta de batería de litio para el sistema EcoVolt.

Las baterías de litio-ion (Li-Ion) y litio-hierro-fosfato (LiFePO4) son la
tecnología de almacenamiento preferida en sistemas fotovoltaicos modernos por
su alta densidad energética, larga vida útil y alta eficiencia de ciclo (~95%).
"""
from domain.entities.battery import Battery


class LithiumBattery(Battery):
    """
    Nivel 3 — Batería de litio de alta eficiencia y larga vida útil.

    Características técnicas:
    - Eficiencia de ciclo: 95% (0.95) — la más alta disponible comercialmente
    - Voltaje nominal: 48V (configuración típica para sistemas residenciales/comerciales)
    - Ciclos de vida típicos: 3000 ciclos antes de degradación significativa
    - Densidad energética: ~150-200 Wh/kg — mayor que plomo-ácido
    - Sin efecto memoria: puede cargarse parcialmente sin degradación

    La eficiencia del 95% significa que por cada 100 kWh almacenados, se pueden
    recuperar 95 kWh útiles, siendo las pérdidas principalmente térmicas.
    """

    # Ciclos de vida típicos de una batería de litio de calidad
    TYPICAL_CYCLE_LIFE: int = 3000

    # Voltaje nominal de sistema (48V es el estándar para sistemas medianos)
    NOMINAL_VOLTAGE_VOLTS: float = 48.0

    # Eficiencia de ida y vuelta del ciclo de carga/descarga
    LITHIUM_EFFICIENCY: float = 0.95

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        battery_id: str,
        capacity_kwh: float = 10.0,  # Capacidad típica para sistema residencial
        initial_charge_percentage: float = 50.0,
        initial_cycle_count: int = 0,
    ) -> None:
        """
        Inicializa la batería de litio con sus parámetros técnicos.

        :param component_id: ID del componente base.
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param battery_id: Identificador de la batería (p. ej. 'LI-001').
        :param capacity_kwh: Capacidad nominal en kWh (por defecto 10 kWh).
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
        Calcula la energía disponible en la batería según su nivel de carga.

        Retorna la energía útil que la batería puede entregar al sistema,
        calculada como la fracción de la capacidad total correspondiente
        al nivel de carga actual.

        :return: Energía disponible en kilovatios-hora (kWh).
        """
        # Energía disponible = capacidad total × fracción de carga actual
        return self._capacity_kwh * (self._current_charge_percentage / 100.0)

    def get_efficiency(self) -> float:
        """
        Retorna la eficiencia de ciclo de la batería de litio.

        La eficiencia del 95% es la tasa de retorno energético: por cada kWh
        almacenado, se pueden recuperar 0.95 kWh. El 5% restante se disipa
        como calor durante los procesos electroquímicos de carga/descarga.

        :return: 0.95 — eficiencia del 95%, la más alta disponible.
        """
        return self.LITHIUM_EFFICIENCY

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos de la batería de litio a un diccionario.

        El diccionario incluye información sobre salud de la batería basada
        en los ciclos consumidos respecto a la vida útil máxima estimada.

        :return: Diccionario con todos los campos de la batería para API REST.
        """
        # Calcular salud estimada de la batería según ciclos restantes
        remaining_cycle_percentage = max(
            0.0,
            ((self.TYPICAL_CYCLE_LIFE - self._cycle_count) / self.TYPICAL_CYCLE_LIFE) * 100.0
        )

        return {
            # Campos de identidad heredados de EnergyComponent
            "component_id": self.component_id,
            "installation_location": self.installation_location,
            "installation_date": self.installation_date,
            # Campos específicos de la batería
            "battery_id": self._battery_id,
            "battery_type": "lithium",
            "capacity_kwh": self._capacity_kwh,
            "nominal_voltage": self.NOMINAL_VOLTAGE_VOLTS,
            "efficiency": self.LITHIUM_EFFICIENCY,
            "typical_cycle_life": self.TYPICAL_CYCLE_LIFE,
            # Estado en tiempo real
            "current_charge_percentage": self._current_charge_percentage,
            "current_voltage": self._current_voltage,
            "cycle_count": self._cycle_count,
            "remaining_cycle_percentage": round(remaining_cycle_percentage, 1),
            # Métricas calculadas
            "available_energy_kwh": self.generate(),
            "status": self.get_status(),
        }
