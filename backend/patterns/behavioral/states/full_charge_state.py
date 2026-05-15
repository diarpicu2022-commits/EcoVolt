"""
Estado concreto 'Carga Completa' del State Pattern para baterías EcoVolt.

Representa una batería al 100% de su capacidad. No acepta más carga,
pero puede comenzar a descargar cuando el sistema demande energía.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .battery_state import BatteryState

if TYPE_CHECKING:
    from ....domain.entities.battery import Battery


class FullChargeState(BatteryState):
    """
    Estado que representa una batería completamente cargada (100%).

    Transiciones posibles:
    - Si se solicita carga → permanece en FullChargeState (ya está llena)
    - Si se solicita descarga → DischargingState
    """

    def handle_charge(self, battery_context: "Battery") -> str:
        """
        Maneja una solicitud de carga cuando la batería ya está llena.

        No realiza ninguna transición porque la batería no puede recibir
        más energía sin riesgo de sobrecarga.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje informando que la batería ya está completamente cargada.
        """
        # No se cambia de estado: ya está al máximo de su capacidad
        return "Batería ya está completamente cargada"

    def handle_discharge(self, battery_context: "Battery") -> str:
        """
        Maneja una solicitud de descarga cuando la batería está llena.

        El sistema demanda energía, por lo que la batería comienza a suministrarla
        transicionando al estado DischargingState.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje indicando el inicio del suministro de energía.
        """
        from .discharging_state import DischargingState

        # La batería pasa de reserva completa a suministrar energía al sistema
        battery_context.set_state(DischargingState())
        return (
            f"Batería {battery_context.battery_id} comenzó a suministrar energía. "
            f"Nivel actual: {battery_context.current_charge_percentage:.1f}%"
        )

    def get_status(self) -> str:
        """Retorna la etiqueta legible del estado de carga completa."""
        return "Carga Completa"
