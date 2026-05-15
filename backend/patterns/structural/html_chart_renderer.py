"""
Patrón Bridge — Implementación concreta: renderizador HTML con Chart.js.

HtmlChartRenderer implementa ChartRenderer produciendo markup HTML completo
con un elemento <canvas> y el script JavaScript necesario para renderizar
el gráfico usando la biblioteca Chart.js. La salida puede insertarse
directamente en un dashboard web del sistema EcoVolt.
"""

import sys
import os
import json
import re

# Insertar la raíz del backend en el path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from patterns.structural.chart_renderer import ChartRenderer, ChartData


class HtmlChartRenderer(ChartRenderer):
    """
    Implementación del patrón Bridge que genera HTML con Chart.js para EcoVolt.

    Produce un fragmento HTML autónomo con <canvas> y <script> que puede
    embeberse en cualquier página del dashboard web. Asume que Chart.js está
    disponible en el scope global de la página (cargado via CDN o bundle).

    El ID del canvas se deriva del título del gráfico para garantizar unicidad
    cuando múltiples gráficos coexisten en la misma página del dashboard.
    """

    # Versión de Chart.js usada en el comentario de la plantilla HTML generada
    __CHARTJS_VERSION: str = "4.x"

    def __init__(self, chart_width: int = 600, chart_height: int = 400) -> None:
        """
        Inicializa el renderizador HTML con dimensiones predeterminadas del canvas.

        :param chart_width: Ancho del canvas en píxeles (para el atributo CSS).
        :param chart_height: Alto del canvas en píxeles (para el atributo CSS).
        """
        # Dimensiones del elemento canvas en píxeles
        self.__canvas_width_px: int = chart_width
        self.__canvas_height_px: int = chart_height

    def render(self, chart_data: ChartData) -> str:
        """
        Genera un fragmento HTML con <canvas> y <script> Chart.js para el gráfico.

        El ID del canvas se sanitiza para ser un identificador HTML válido:
        se reemplazan espacios y caracteres especiales por guiones bajos.
        Los datos de etiquetas y valores se insertan como literales JSON para
        evitar problemas de escape en el contexto JavaScript.

        :param chart_data: Datos del gráfico a renderizar como HTML+Chart.js.
        :return: Cadena HTML con el fragmento completo del gráfico.
        """
        # Sanitizar el título para usarlo como ID de elemento HTML
        canvas_element_id = self.__build_canvas_id(chart_data.chart_title)

        # Serializar listas como JSON para inserción segura en el script JS
        labels_json = json.dumps(chart_data.labels, ensure_ascii=False)
        values_json = json.dumps(chart_data.values, ensure_ascii=False)

        # Color de relleno y borde para la serie de datos — paleta EcoVolt (verde solar)
        fill_color = "rgba(34, 197, 94, 0.2)"
        border_color = "rgba(34, 197, 94, 1)"

        html_fragment = (
            f'<!-- Gráfico EcoVolt: {chart_data.chart_title} | Chart.js {self.__CHARTJS_VERSION} -->\n'
            f'<div class="ecovolt-chart-container" '
            f'style="width:{self.__canvas_width_px}px; height:{self.__canvas_height_px}px;">\n'
            f'  <canvas id="chart_{canvas_element_id}"></canvas>\n'
            f'</div>\n'
            f'<script>\n'
            f'(function() {{\n'
            f'  var ctx = document.getElementById("chart_{canvas_element_id}");\n'
            f'  new Chart(ctx, {{\n'
            f'    type: "{chart_data.chart_type}",\n'
            f'    data: {{\n'
            f'      labels: {labels_json},\n'
            f'      datasets: [{{\n'
            f'        label: "{chart_data.chart_title}",\n'
            f'        data: {values_json},\n'
            f'        backgroundColor: "{fill_color}",\n'
            f'        borderColor: "{border_color}",\n'
            f'        borderWidth: 2,\n'
            f'        tension: 0.4,\n'
            f'        fill: true\n'
            f'      }}]\n'
            f'    }},\n'
            f'    options: {{\n'
            f'      responsive: true,\n'
            f'      maintainAspectRatio: false,\n'
            f'      plugins: {{\n'
            f'        legend: {{ display: true }},\n'
            f'        title: {{\n'
            f'          display: true,\n'
            f'          text: "{chart_data.chart_title}"\n'
            f'        }}\n'
            f'      }},\n'
            f'      scales: {{\n'
            f'        y: {{ beginAtZero: true }}\n'
            f'      }}\n'
            f'    }}\n'
            f'  }});\n'
            f'}})();\n'
            f'</script>'
        )
        return html_fragment

    def __build_canvas_id(self, chart_title: str) -> str:
        """
        Transforma el título del gráfico en un ID de elemento HTML válido.

        Reemplaza espacios, tildes y caracteres especiales por guiones bajos
        para garantizar compatibilidad con los selectores DOM de JavaScript.

        :param chart_title: Título del gráfico a transformar en ID.
        :return: Cadena apta para usar como atributo id de un elemento HTML.
        """
        # Reemplazar caracteres no alfanuméricos y guiones por guión bajo
        sanitized_id = re.sub(r'[^a-zA-Z0-9\-]', '_', chart_title)
        # Eliminar guiones bajos múltiples consecutivos para limpieza visual
        sanitized_id = re.sub(r'_+', '_', sanitized_id)
        # Asegurarse de que no empiece con un dígito (regla de IDs HTML)
        if sanitized_id and sanitized_id[0].isdigit():
            sanitized_id = "chart_" + sanitized_id
        return sanitized_id.lower()

    @property
    def canvas_width_px(self) -> int:
        """Ancho del canvas en píxeles configurado para este renderizador."""
        return self.__canvas_width_px

    @property
    def canvas_height_px(self) -> int:
        """Alto del canvas en píxeles configurado para este renderizador."""
        return self.__canvas_height_px

    def __repr__(self) -> str:
        return (
            f"HtmlChartRenderer("
            f"width={self.__canvas_width_px}px, "
            f"height={self.__canvas_height_px}px)"
        )
