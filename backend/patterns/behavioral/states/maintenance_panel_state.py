"""
Estado concreto 'En Mantenimiento' del State Pattern para paneles solares EcoVolt.

El panel ha sido puesto fuera de servicio intencionalmente por el equipo técnico
para limpieza, inspección o reemplazo de componentes. En este estado, todas las
lecturas de sensores son ignoradas para evitar falsos positivos en el sistema.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from patterns.behavioral.states.panel_state import PanelState

if TYPE_CHECKING:
    from domain.entities.solar_panel import SolarPanel


class MaintenancePanelState(PanelState):
    """
    Estado que representa un panel solar fuera de servicio por mantenimiento planificado.

    En este estado no se realizan transiciones automáticas. Solo el personal técnico
    puede cambiar el estado del panel manualmente a través del sistema de gestión.
    Todas las lecturas de sensores son descartadas para preservar la integridad
    de los datos históricos de generación.
    """

    def handle_reading(self, panel_context: "SolarPanel") -> str:
        """
        Ignora la lectura del sensor durante el mantenimiento.

        No se realizan transiciones de estado desde mantenimiento de forma automática.
        Solo el administrador del sistema puede sacar el panel de mantenimiento.

        :param panel_context: El panel solar que delega este comportamiento.
        :return: Mensaje informando que el panel está en mantenimiento.
        """
        # Las lecturas se reciben pero se descartan para no contaminar métricas
        return (
            f"Panel {panel_context.panel_id} en mantenimiento, lecturas ignoradas"
        )

    def get_status_label(self) -> str:
        """Retorna la etiqueta legible del estado de mantenimiento del panel."""
        return "En Mantenimiento"
