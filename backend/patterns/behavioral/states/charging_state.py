"""
Estado concreto 'Cargando' del State Pattern para baterías EcoVolt.

Cuando la batería se encuentra en este estado, acepta carga adicional
y puede transicionar a FullChargeState o DischargingState según la operación.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .battery_state import BatteryState

# Importaciones diferidas para evitar ciclos: los estados se referencian entre sí
if TYPE_CHECKING:
    from ....domain.entities.battery import Battery


class ChargingState(BatteryState):
    """
    Estado que representa una batería en proceso activo de carga.

    Transiciones posibles:
    - Si la carga alcanza 100% → FullChargeState
    - Si se solicita descarga → DischargingState
    """

    def handle_charge(self, battery_context: "Battery") -> str:
        """
        Maneja una operación de carga adicional.

        Si el porcentaje de carga llega o supera 100%, la batería transiciona
        al estado FullChargeState para evitar sobrecarga.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje con el resultado de la carga.
        """
        # Se importa aquí dentro para romper la dependencia circular en tiempo de ejecución
        from .full_charge_state import FullChargeState

        # Verificar si la batería ya alcanzó capacidad máxima tras la carga
        if battery_context.current_charge_percentage >= 100.0:
            battery_context.set_state(FullChargeState())
            return (
                f"Batería {battery_context.battery_id} completamente cargada. "
                f"Estado cambiado a: {FullChargeState().get_status()}"
            )

        return (
            f"Batería {battery_context.battery_id} cargando... "
            f"Nivel actual: {battery_context.current_charge_percentage:.1f}%"
        )

    def handle_discharge(self, battery_context: "Battery") -> str:
        """
        Maneja una solicitud de descarga cuando la batería está cargando.

        Interrumpe la carga y transiciona al estado DischargingState.

        :param battery_context: La batería que delega este comportamiento.
        :return: Mensaje indicando el cambio de estado.
        """
        from .discharging_state import DischargingState

        # La carga se interrumpe porque hay demanda de energía
        battery_context.set_state(DischargingState())
        return (
            f"Batería {battery_context.battery_id} interrumpió carga. "
            f"Iniciando descarga desde {battery_context.current_charge_percentage:.1f}%"
        )

    def get_status(self) -> str:
        """Retorna la etiqueta legible del estado de carga activa."""
        return "Cargando"
