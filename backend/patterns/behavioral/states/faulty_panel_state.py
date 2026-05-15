"""
Estado concreto 'Con Fallo' del State Pattern para paneles solares EcoVolt.

El panel ha detectado una condición anormal que impide su operación segura
(sobrecalentamiento, daño físico, fallo de conexiones). En este estado el
sistema debe generar una alerta y programar revisión técnica urgente.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .panel_state import PanelState

if TYPE_CHECKING:
    from ....domain.entities.solar_panel import SolarPanel


class FaultyPanelState(PanelState):
    """
    Estado que representa un panel solar con fallo técnico detectado.

    Un panel en estado de fallo no puede transicionar automáticamente a otro estado.
    Requiere intervención manual del técnico para diagnosticar y reparar el problema,
    después de lo cual el administrador puede cambiar el estado manualmente.

    Las lecturas siguen siendo registradas para diagnóstico pero no se procesan
    como generación activa de energía.
    """

    def handle_reading(self, panel_context: "SolarPanel") -> str:
        """
        Procesa una lectura de sensor cuando el panel está en estado de fallo.

        No realiza transiciones automáticas porque el fallo requiere diagnóstico
        humano para determinar si es seguro reactivar el panel.

        :param panel_context: El panel solar que delega este comportamiento.
        :return: Mensaje indicando que el panel requiere revisión técnica.
        """
        # Estado bloqueado: solo el técnico puede restaurar el panel
        return (
            f"FALLO DETECTADO: Panel {panel_context.panel_id} requiere revisión técnica — "
            f"Temp: {panel_context.current_temperature_celsius:.1f}°C | "
            f"V: {panel_context.current_voltage:.2f}V | "
            f"I: {panel_context.current_current_amps:.2f}A"
        )

    def get_status(self) -> str:
        """Retorna la etiqueta legible del estado de fallo del panel."""
        return "Con Fallo"
