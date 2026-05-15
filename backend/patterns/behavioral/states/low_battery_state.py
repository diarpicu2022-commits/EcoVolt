"""
Estado concreto 'Batería Baja' del State Pattern para baterías EcoVolt.

Representa una batería con nivel crítico de carga (≤ 20%). En este estado
el sistema debe activar alertas y priorizar la carga inmediata para evitar
daños en las celdas y pérdida de datos de configuración del inversor.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .battery_state import BatteryState

if TYPE_CHECKING:
    from ....domain.entities.battery import Battery


class LowBatteryState(BatteryState):
    """
    Estado que representa una batería en nivel críticamente bajo de carga.

    Transiciones posibles:
    - Si se solicita descarga adicional → permanece en LowBatteryState + advertencia crítica
    - Si se recibe carga → ChargingState
    """

    def handle_charge(self, battery_context: "Battery") -> str:
        """
        Maneja una solicitud de carga cuando la batería está en nivel crítico.

        Transiciona a ChargingState porque recibir carga es la acción correcta
        para sacar la batería del estado crítico.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje indicando el inicio de la carga de recuperación.
        """
        from .charging_state import ChargingState

        # Recuperación del estado crítico: el panel solar o la red está inyectando energía
        battery_context.set_state(ChargingState())
        return (
            f"Batería {battery_context.battery_id} comenzó carga de recuperación. "
            f"Nivel actual: {battery_context.current_charge_percentage:.1f}%"
        )

    def handle_discharge(self, battery_context: "Battery") -> str:
        """
        Maneja una solicitud de descarga adicional en nivel crítico.

        No transiciona de estado, pero emite una advertencia severa.
        Descargar por debajo de este umbral puede dañar permanentemente las celdas.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje de advertencia crítica.
        """
        # Descarga peligrosa: no se cambia estado pero se alerta al sistema
        return (
            f"ADVERTENCIA: Batería críticamente baja — "
            f"Batería {battery_context.battery_id} al {battery_context.current_charge_percentage:.1f}%. "
            f"Conectar fuente de carga inmediatamente."
        )

    def get_status(self) -> str:
        """Retorna la etiqueta legible del estado crítico de batería."""
        return "Batería Baja"
