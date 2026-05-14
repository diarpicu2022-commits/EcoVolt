"""
Clase abstracta de Nivel 2 que representa una batería de almacenamiento en EcoVolt.

Extiende EnergyComponent con los atributos de capacidad y estado de carga
propios de los sistemas de almacenamiento energético, e integra el State Pattern
para gestionar las transiciones operativas sin condicionales if/else.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from domain.entities.energy_component import EnergyComponent

# Importación diferida: BatteryState referencia a Battery en sus métodos, evitamos ciclo
if TYPE_CHECKING:
    from patterns.behavioral.states.battery_state import BatteryState


class Battery(EnergyComponent):
    """
    Nivel 2 de la jerarquía — Clase abstracta para baterías de almacenamiento.

    Modela los atributos comunes de cualquier tecnología de batería
    (litio-ion, plomo-ácido, flujo): capacidad total, nivel de carga actual,
    contador de ciclos y voltaje de operación.

    Integra el State Pattern para que las operaciones de carga y descarga
    sean delegadas al estado activo, permitiendo transiciones limpias entre
    Cargando → Carga Completa → Descargando → Batería Baja sin if/else.

    Los campos de medición son PROTEGIDOS (_campo) para que las subclases
    concretas puedan calcular la energía disponible según su tecnología.
    """

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        battery_id: str,
        capacity_kwh: float,
        initial_charge_percentage: float = 50.0,
        initial_cycle_count: int = 0,
        nominal_voltage: float = 48.0,
    ) -> None:
        """
        Inicializa la batería con sus parámetros de capacidad y estado inicial.

        :param component_id: ID del componente base (herencia de EnergyComponent).
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param battery_id: Identificador específico de la batería (p. ej. 'LI-001').
        :param capacity_kwh: Capacidad nominal total de la batería en kilovatios-hora.
        :param initial_charge_percentage: Nivel de carga inicial (0.0 a 100.0).
        :param initial_cycle_count: Número de ciclos de carga/descarga ya realizados.
        :param nominal_voltage: Voltaje nominal de operación en voltios.
        """
        # Inicializa los campos de identidad del componente base
        super().__init__(component_id, installation_location, installation_date)

        # Campos protegidos: accesibles por subclases para cálculos de generación
        self._battery_id: str = battery_id
        self._capacity_kwh: float = capacity_kwh
        self._current_charge_percentage: float = max(0.0, min(100.0, initial_charge_percentage))
        self._cycle_count: int = initial_cycle_count
        self._current_voltage: float = nominal_voltage

        # Campo privado: el estado solo se cambia a través de set_state()
        # Se inicializa en DischargingState porque la batería arranca suministrando energía
        from patterns.behavioral.states.discharging_state import DischargingState
        self.__battery_state: Any = DischargingState()

    # -------------------------------------------------------------------------
    # Properties de solo lectura para los atributos de la batería
    # -------------------------------------------------------------------------

    @property
    def battery_id(self) -> str:
        """Identificador único de la batería dentro del sistema EcoVolt."""
        return self._battery_id

    @property
    def capacity_kwh(self) -> float:
        """Capacidad nominal total de almacenamiento en kilovatios-hora."""
        return self._capacity_kwh

    @property
    def current_charge_percentage(self) -> float:
        """Nivel de carga actual como porcentaje (0.0 = vacía, 100.0 = llena)."""
        return self._current_charge_percentage

    @property
    def cycle_count(self) -> int:
        """Número acumulado de ciclos de carga y descarga completados."""
        return self._cycle_count

    @property
    def current_voltage(self) -> float:
        """Voltaje actual medido en los terminales de la batería (en voltios)."""
        return self._current_voltage

    # -------------------------------------------------------------------------
    # Métodos de operación de la batería
    # -------------------------------------------------------------------------

    def charge(self, amount_kwh: float) -> None:
        """
        Añade energía a la batería, aumentando su nivel de carga.

        Convierte los kWh recibidos a porcentaje de carga relativo a la capacidad
        total y acumula el total. El nivel se limita a 100% para evitar sobrecarga.
        Después de actualizar el nivel, delega al estado para posibles transiciones.

        :param amount_kwh: Cantidad de energía en kWh a cargar en la batería.
        """
        # Calcular el porcentaje equivalente a la energía recibida
        percentage_added = (amount_kwh / self._capacity_kwh) * 100.0

        # Acumular la carga sin superar el 100%
        self._current_charge_percentage = min(
            100.0, self._current_charge_percentage + percentage_added
        )

    def discharge(self, amount_kwh: float) -> None:
        """
        Extrae energía de la batería, disminuyendo su nivel de carga.

        Convierte los kWh consumidos a porcentaje de descarga relativo a la
        capacidad total. El nivel se limita a 0% para evitar descarga profunda
        que dañaría las celdas. Incrementa el contador de ciclos cuando la
        descarga es significativa.

        :param amount_kwh: Cantidad de energía en kWh a extraer de la batería.
        """
        # Calcular el porcentaje equivalente a la energía consumida
        percentage_removed = (amount_kwh / self._capacity_kwh) * 100.0

        # Reducir la carga sin bajar de 0%
        self._current_charge_percentage = max(
            0.0, self._current_charge_percentage - percentage_removed
        )

        # Incrementar ciclos cuando la descarga es suficientemente significativa (>5%)
        # Un ciclo completo se define como carga + descarga significativa
        if percentage_removed >= 5.0:
            self._cycle_count += 1

    def set_state(self, new_state: "BatteryState") -> None:
        """
        Cambia el estado operativo de la batería (usado por los estados concretos).

        Este método es llamado por los estados durante las transiciones,
        implementando el mecanismo central del State Pattern.

        :param new_state: Nueva instancia de BatteryState que reemplaza al estado actual.
        """
        # El cambio de estado es controlado por el propio estado, no por la batería
        self.__battery_state = new_state

    def handle_charge(self) -> str:
        """
        Delega la operación de carga al estado activo de la batería.

        Aplica el principio de delegación del State Pattern: la batería no decide
        cómo comportarse al cargar, sino que lo delega al estado que lo encapsula.

        :return: Mensaje descriptivo del resultado según el estado actual.
        """
        # Delegación completa al estado actual — sin if/else para determinar comportamiento
        return self.__battery_state.handle_charge(self)

    def handle_discharge(self) -> str:
        """
        Delega la operación de descarga al estado activo de la batería.

        :return: Mensaje descriptivo del resultado según el estado actual.
        """
        # Delegación completa al estado actual — sin if/else
        return self.__battery_state.handle_discharge(self)

    # -------------------------------------------------------------------------
    # Implementación concreta del método heredado de EnergyComponent
    # -------------------------------------------------------------------------

    def get_status(self) -> str:
        """
        Retorna el estado operativo de la batería usando el estado del State Pattern.

        Implementa el método abstracto de EnergyComponent delegando la etiqueta
        de estado al objeto de estado actual, asegurando consistencia con las
        transiciones del State Pattern.

        :return: Cadena descriptiva con el ID, nivel de carga y etiqueta de estado.
        """
        return (
            f"Batería {self._battery_id}: "
            f"{self._current_charge_percentage:.1f}% cargada | "
            f"Estado: {self.__battery_state.get_status_label()} | "
            f"Ciclos: {self._cycle_count}"
        )

    # -------------------------------------------------------------------------
    # Métodos abstractos — deben implementarse para cada tecnología de batería
    # -------------------------------------------------------------------------

    @abstractmethod
    def generate(self) -> float:
        """Retorna la energía disponible en la batería según su nivel de carga."""
        ...

    @abstractmethod
    def get_efficiency(self) -> float:
        """Retorna la eficiencia de carga/descarga de la tecnología de batería."""
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        """Serializa todos los atributos de la batería a un diccionario."""
        ...
