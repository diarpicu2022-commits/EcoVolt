"""
Estado concreto 'Activo' del State Pattern para paneles solares EcoVolt.

El panel está operando normalmente: generando energía y produciendo lecturas
válidas de voltaje, corriente y temperatura. Las lecturas se verifican contra
umbrales de seguridad para detectar fallos o condiciones de inactividad.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .panel_state import PanelState

if TYPE_CHECKING:
    from ....domain.entities.solar_panel import SolarPanel


class ActivePanelState(PanelState):
    """
    Estado que representa un panel solar en operación normal y generando energía.

    Transiciones posibles:
    - Si temperatura > 75°C → FaultyPanelState (sobrecalentamiento)
    - Si voltaje < 1.0V → StandbyPanelState (sin luz solar suficiente)
    - Si las lecturas son normales → permanece en ActivePanelState
    """

    def handle_reading(self, panel_context: "SolarPanel") -> str:
        """
        Procesa una nueva lectura de sensores en estado activo.

        Evalúa los umbrales de temperatura y voltaje para determinar si el panel
        debe transicionar a un estado de fallo o en espera.

        Umbral de temperatura: 75°C — por encima las células fotovoltaicas
        se degradan y pueden producir microcriaturas permanentes.
        Umbral de voltaje mínimo: 1.0V — por debajo no hay incidencia solar útil.

        :param panel_context: El panel solar que delega este comportamiento.
        :return: Mensaje describiendo el resultado del procesamiento de la lectura.
        """
        from .faulty_panel_state import FaultyPanelState
        from .standby_panel_state import StandbyPanelState

        # Verificación de sobrecalentamiento — umbral crítico de las células fotovoltaicas
        if panel_context.current_temperature_celsius > 75.0:
            panel_context.set_state(FaultyPanelState())
            return (
                f"FALLO: Panel {panel_context.panel_id} sobrecalentado a "
                f"{panel_context.current_temperature_celsius:.1f}°C. "
                f"Estado cambiado a: Con Fallo"
            )

        # Verificación de voltaje mínimo — sin sol suficiente para generar
        if panel_context.current_voltage < 1.0:
            panel_context.set_state(StandbyPanelState())
            return (
                f"Panel {panel_context.panel_id} sin incidencia solar suficiente "
                f"({panel_context.current_voltage:.2f}V). Estado cambiado a: En Espera"
            )

        # Lectura normal: el panel continúa generando energía
        power_watts = panel_context.get_current_power_watts()
        return (
            f"Panel {panel_context.panel_id} activo — "
            f"{panel_context.current_voltage:.2f}V | "
            f"{panel_context.current_current_amps:.2f}A | "
            f"{panel_context.current_temperature_celsius:.1f}°C | "
            f"{power_watts:.2f}W generados"
        )

    def get_status(self) -> str:
        """Retorna la etiqueta legible del estado activo del panel."""
        return "Activo"
