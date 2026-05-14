"""
Estado concreto 'Descargando' del State Pattern para baterías EcoVolt.

Cuando la batería se encuentra en este estado, suministra energía al sistema.
Si la carga cae a 20% o menos, transiciona automáticamente a LowBatteryState
para proteger la vida útil de la batería.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from patterns.behavioral.states.battery_state import BatteryState

if TYPE_CHECKING:
    from domain.entities.battery import Battery


class DischargingState(BatteryState):
    """
    Estado que representa una batería suministrando energía activamente.

    Transiciones posibles:
    - Si la carga cae a 20% o menos → LowBatteryState (umbral de protección)
    - Si se solicita carga → ChargingState
    """

    def handle_charge(self, battery_context: "Battery") -> str:
        """
        Maneja una solicitud de carga cuando la batería está descargando.

        Cambia el estado a ChargingState porque la fuente solar o red
        ha comenzado a inyectar energía.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje indicando el inicio de la carga.
        """
        from patterns.behavioral.states.charging_state import ChargingState

        # Se recibe energía solar o de red: revertir a modo carga
        battery_context.set_state(ChargingState())
        return (
            f"Batería {battery_context.battery_id} comenzó a recibir carga. "
            f"Nivel actual: {battery_context.current_charge_percentage:.1f}%"
        )

    def handle_discharge(self, battery_context: "Battery") -> str:
        """
        Maneja una operación de descarga continua.

        Si la carga alcanza el umbral crítico del 20%, transiciona a LowBatteryState
        para activar alertas y proteger las celdas de la batería.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje con el estado de la descarga.
        """
        from patterns.behavioral.states.low_battery_state import LowBatteryState

        # Umbral de 20% — por debajo de este nivel la batería puede dañarse
        if battery_context.current_charge_percentage <= 20.0:
            battery_context.set_state(LowBatteryState())
            return (
                f"ADVERTENCIA: Batería {battery_context.battery_id} alcanzó nivel crítico "
                f"({battery_context.current_charge_percentage:.1f}%). Estado: Batería Baja"
            )

        return (
            f"Batería {battery_context.battery_id} descargando. "
            f"Nivel actual: {battery_context.current_charge_percentage:.1f}%"
        )

    def get_status_label(self) -> str:
        """Retorna la etiqueta legible del estado de descarga activa."""
        return "Descargando"
