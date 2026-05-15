"""
Estado concreto 'En Espera' del State Pattern para paneles solares EcoVolt.

El panel está instalado y funcionalmente correcto, pero no recibe suficiente
irradiación solar para generar energía útil (noche, nubosidad densa, sombra).
Monitorea el voltaje para detectar cuando vuelve la incidencia solar.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .panel_state import PanelState

if TYPE_CHECKING:
    from ....domain.entities.solar_panel import SolarPanel


class StandbyPanelState(PanelState):
    """
    Estado que representa un panel solar en espera de irradiación solar suficiente.

    Transiciones posibles:
    - Si voltaje > 5.0V → ActivePanelState (hay incidencia solar suficiente)
    - Si voltaje ≤ 5.0V → permanece en StandbyPanelState
    """

    def handle_reading(self, panel_context: "SolarPanel") -> str:
        """
        Procesa una nueva lectura mientras el panel está en espera.

        Verifica si el voltaje ha superado el umbral de 5.0V que indica
        que hay suficiente irradiación solar para generar energía útil.

        Umbral de activación: 5.0V — valor mínimo para iniciar generación
        eficiente según las especificaciones de los paneles fotovoltaicos típicos.

        :param panel_context: El panel solar que delega este comportamiento.
        :return: Mensaje describiendo el estado del panel en espera.
        """
        from .active_panel_state import ActivePanelState

        # Umbral de activación: suficiente voltaje indica irradiación solar útil
        if panel_context.current_voltage > 5.0:
            panel_context.set_state(ActivePanelState())
            return (
                f"Panel {panel_context.panel_id} detectó irradiación solar "
                f"({panel_context.current_voltage:.2f}V). Estado cambiado a: Activo"
            )

        # Sin cambio de estado: el panel sigue esperando luz solar
        return (
            f"Panel {panel_context.panel_id} en espera. "
            f"Voltaje actual: {panel_context.current_voltage:.2f}V "
            f"(mínimo requerido: 5.0V)"
        )

    def get_status(self) -> str:
        """Retorna la etiqueta legible del estado en espera del panel."""
        return "En Espera"
