"""
Clase abstracta de Nivel 2 que representa una batería genérica en EcoVolt.

Extiende EnergyComponent con atributos de almacenamiento energético y delega
el comportamiento operativo al State Pattern para evitar lógica dispersa.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from .energy_component import EnergyComponent

if TYPE_CHECKING:
    from ...patterns.behavioral.states.battery_state import BatteryState


class Battery(EnergyComponent):
    """
    Clase abstracta base para baterías del sistema EcoVolt.

    Modela el almacenamiento de energía y el estado de carga actual. Las
    transiciones de carga y descarga se delegan a objetos de estado concretos.
    """

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        battery_id: str,
        capacity_kwh: float,
        current_charge_percentage: float,
        cycle_count: int = 0,
    ) -> None:
        super().__init__(component_id, installation_location, installation_date)
        self._battery_id: str = battery_id
        self._capacity_kwh: float = capacity_kwh
        self._current_charge_percentage: float = current_charge_percentage
        self._cycle_count: int = cycle_count

        # La batería inicia descargando hasta que un flujo de carga la reactive.
        from ...patterns.behavioral.states.discharging_state import DischargingState

        self.__battery_state: Any = DischargingState()

    @property
    def battery_id(self) -> str:
        return self._battery_id

    @property
    def capacity_kwh(self) -> float:
        return self._capacity_kwh

    @property
    def current_charge_percentage(self) -> float:
        return self._current_charge_percentage

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    def update_charge_percentage(self, new_charge_percentage: float) -> None:
        # Se acota el porcentaje para no propagar estados físicamente imposibles.
        self._current_charge_percentage = max(0.0, min(100.0, new_charge_percentage))

    def set_state(self, new_state: "BatteryState") -> None:
        self.__battery_state = new_state

    def handle_charge(self) -> str:
        return self.__battery_state.handle_charge(self)

    def handle_discharge(self) -> str:
        return self.__battery_state.handle_discharge(self)

    def get_component_info(self) -> str:
        base_info = super().get_component_info()
        return (
            f"{base_info} | "
            f"Battery ID: {self._battery_id} | "
            f"Capacity: {self._capacity_kwh}kWh | "
            f"Charge: {self._current_charge_percentage:.1f}% | "
            f"State: {self.__battery_state.get_status()}"
        )

    @abstractmethod
    def generate(self) -> float:
        ...

    @abstractmethod
    def get_status(self) -> str:
        ...

    @abstractmethod
    def get_efficiency(self) -> float:
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        ...
