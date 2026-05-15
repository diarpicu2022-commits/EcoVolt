"""
Patrón Bridge — Implementación concreta: renderizador JSON.

JsonChartRenderer implementa ChartRenderer produciendo una cadena JSON
que puede ser consumida por APIs REST, almacenada en bases de datos NoSQL
o enviada a clientes frontend que construyan la visualización por su cuenta.

Las claves del JSON están en español para mantener coherencia con el dominio
EcoVolt y los comentarios internos del sistema.
"""

import sys
import os
import json

# Insertar la raíz del backend en el path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from patterns.structural.chart_renderer import ChartRenderer, ChartData


class JsonChartRenderer(ChartRenderer):
    """
    Implementación del patrón Bridge que serializa gráficos EcoVolt a formato JSON.

    Produce JSON válido con claves en español, listo para ser retornado por
    la API REST del sistema o almacenado en el historial de visualizaciones.
    Usa ensure_ascii=False para preservar caracteres especiales del español
    (acentos, eñes) en títulos y etiquetas de gráficos.
    """

    def __init__(self, indent: int = 2) -> None:
        """
        Inicializa el renderizador JSON con configuración de formato.

        :param indent: Número de espacios de indentación en el JSON de salida.
                       Usar 0 o None para JSON compacto (sin saltos de línea).
        """
        # Nivel de indentación para el JSON — 2 espacios por defecto para legibilidad
        self.__json_indent: int = indent

    def render(self, chart_data: ChartData) -> str:
        """
        Serializa los datos del gráfico EcoVolt a una cadena JSON.

        El JSON resultante tiene la siguiente estructura:
        {
          "titulo": "Producción Panel P-01",
          "etiquetas": ["00h", "01h", ..., "23h"],
          "valores": [0.0, 0.0, ..., 4.5, 6.2, ...],
          "tipo": "line"
        }

        :param chart_data: Datos del gráfico a serializar.
        :return: Cadena JSON con los datos del gráfico, indentada según configuración.
        """
        # Construir el diccionario con claves en español según el dominio EcoVolt
        chart_dict = {
            "titulo": chart_data.chart_title,
            "etiquetas": chart_data.labels,
            "valores": chart_data.values,
            "tipo": chart_data.chart_type,
        }

        # ensure_ascii=False preserva tildes y ñ en títulos y etiquetas
        json_output = json.dumps(chart_dict, ensure_ascii=False, indent=self.__json_indent)
        return json_output

    @property
    def json_indent(self) -> int:
        """Nivel de indentación actual del renderizador JSON."""
        return self.__json_indent

    @json_indent.setter
    def json_indent(self, indent: int) -> None:
        """
        Cambia el nivel de indentación del JSON de salida.

        :param indent: Número de espacios de indentación (0 para JSON compacto).
        :raises ValueError: Si el valor de indentación es negativo.
        """
        if indent < 0:
            raise ValueError("La indentación JSON no puede ser negativa.")
        self.__json_indent = indent

    def __repr__(self) -> str:
        return f"JsonChartRenderer(indent={self.__json_indent})"
