"""
Patrón Bridge — Abstracción refinada (lado de la abstracción).

EnergyDisplayAbstraction es la clase base de la jerarquía de abstracción del
patrón Bridge. Mantiene una referencia al ChartRenderer (implementación) y
delega a él el renderizado concreto. Las subclases (PanelChartDisplay,
BatteryChartDisplay) deciden QUÉ datos mostrar; el renderer decide CÓMO.

La separación entre abstracción e implementación permite cambiar el formato de
salida (JSON, HTML, SVG) en tiempo de ejecución sin tocar la lógica de datos.
"""

import sys
import os
from abc import ABC, abstractmethod

# Insertar la raíz del backend en el path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from patterns.structural.chart_renderer import ChartRenderer


class EnergyDisplayAbstraction(ABC):
    """
    Abstracción base del patrón Bridge para visualización de datos EcoVolt.

    Mantiene una referencia al ChartRenderer que actúa como el 'puente'
    entre la lógica de preparación de datos y el formato de salida concreto.
    Las subclases refinadas implementan display() para preparar los datos
    específicos de su componente y luego delegan el renderizado al renderer.

    Permite sustituir el renderer en tiempo de ejecución (set_renderer) para
    cambiar el formato de salida sin modificar la lógica de datos del display.
    """

    def __init__(self, renderer: ChartRenderer) -> None:
        """
        Inicializa la abstracción con un renderizador concreto (el puente).

        :param renderer: Implementación concreta de ChartRenderer que realizará
                         el renderizado (JsonChartRenderer, HtmlChartRenderer, etc.).
        :raises TypeError: Si el renderer no es una instancia de ChartRenderer.
        """
        if not isinstance(renderer, ChartRenderer):
            raise TypeError(
                f"El renderer debe ser una instancia de ChartRenderer, "
                f"pero se recibió: {type(renderer).__name__}"
            )
        # El renderer es la implementación del puente — accesible por subclases
        self._chart_renderer: ChartRenderer = renderer

    @abstractmethod
    def display(self, component_id: str) -> str:
        """
        Prepara los datos del componente EcoVolt y los renderiza via el renderer.

        Las subclases implementan este método para construir el ChartData
        adecuado para su tipo de componente (panel, batería, carga) y luego
        llamar a self._chart_renderer.render(chart_data) para obtener la salida.

        :param component_id: Identificador del componente a visualizar
                              (panel_id, battery_id, etc.).
        :return: Cadena con el resultado renderizado (JSON, HTML, etc.)
                 dependiendo del ChartRenderer activo.
        """
        ...

    def set_renderer(self, renderer: ChartRenderer) -> None:
        """
        Cambia el renderizador en tiempo de ejecución (parte clave del Bridge).

        Permite al sistema EcoVolt cambiar el formato de salida dinámicamente:
        por ejemplo, pasar de HTML (dashboard web) a JSON (API REST) o a SVG
        (reporte imprimible) sin recrear el objeto de display.

        :param renderer: Nueva implementación de ChartRenderer a usar.
        :raises TypeError: Si el renderer no es una instancia de ChartRenderer.
        """
        if not isinstance(renderer, ChartRenderer):
            raise TypeError(
                f"El nuevo renderer debe ser una instancia de ChartRenderer, "
                f"pero se recibió: {type(renderer).__name__}"
            )
        # Reemplazar el renderer — el puente cambia en tiempo de ejecución
        self._chart_renderer = renderer

    @property
    def active_renderer(self) -> ChartRenderer:
        """Retorna el renderer actualmente activo en este display."""
        return self._chart_renderer

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"renderer={self._chart_renderer.__class__.__name__})"
        )
