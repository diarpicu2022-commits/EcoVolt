"""
Patrón Bridge — Implementación (interfaz del lado del renderizador).

ChartRenderer define el contrato de la implementación en el patrón Bridge.
Las clases concretas (JsonChartRenderer, HtmlChartRenderer) implementan esta
interfaz para distintos formatos de salida. La abstracción (EnergyDisplayAbstraction)
solo conoce ChartRenderer — el puente que separa qué mostrar de cómo renderizarlo.

También define ChartData, el objeto de transferencia de datos que viaja por el puente.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ChartData:
    """
    Objeto de transferencia de datos para gráficos del sistema EcoVolt.

    Encapsula toda la información necesaria para que cualquier renderizador
    (JSON, HTML, SVG, etc.) pueda producir una visualización coherente.
    Al ser un dataclass, es inmutable y fácil de serializar.

    Atributos:
        chart_title: Título descriptivo del gráfico (p. ej. 'Producción Panel P-01').
        labels: Etiquetas del eje X (p. ej. horas del día '00h', '01h', ...).
        values: Valores numéricos correspondientes a cada etiqueta del eje X.
        chart_type: Tipo de gráfico según Chart.js ('line', 'bar', 'pie', 'doughnut').
    """
    chart_title: str
    labels: list[str]
    values: list[float]
    chart_type: str = "line"

    def __post_init__(self) -> None:
        """Valida la consistencia entre etiquetas y valores al construir el objeto."""
        if len(self.labels) != len(self.values):
            raise ValueError(
                f"La cantidad de etiquetas ({len(self.labels)}) no coincide "
                f"con la cantidad de valores ({len(self.values)}). "
                f"Ambas listas deben tener el mismo tamaño."
            )
        if not self.chart_title.strip():
            raise ValueError("El título del gráfico no puede estar vacío.")

        # Tipos soportados por Chart.js — validar para evitar HTML inválido
        supported_chart_types = {"line", "bar", "pie", "doughnut", "radar", "polarArea"}
        if self.chart_type not in supported_chart_types:
            raise ValueError(
                f"Tipo de gráfico no soportado: '{self.chart_type}'. "
                f"Tipos válidos: {', '.join(sorted(supported_chart_types))}"
            )


class ChartRenderer(ABC):
    """
    Interfaz de implementación del patrón Bridge para renderizado de gráficos EcoVolt.

    Define el contrato mínimo que toda implementación de renderizado debe cumplir.
    Las abstracciones (EnergyDisplayAbstraction y subclases) delegan el renderizado
    a través de esta interfaz sin conocer el formato de salida concreto.

    Implementaciones previstas:
    - JsonChartRenderer: serializa gráficos como JSON para APIs REST.
    - HtmlChartRenderer: genera markup HTML con Chart.js para dashboards web.
    - SvgChartRenderer: renderiza gráficos vectoriales para reportes imprimibles.
    - CsvChartRenderer: exporta datos tabulares para análisis en hojas de cálculo.
    """

    @abstractmethod
    def render(self, chart_data: ChartData) -> str:
        """
        Renderiza el gráfico con los datos proporcionados al formato de salida concreto.

        La implementación concreta decide el formato de salida (JSON, HTML, SVG, CSV).
        La abstracción no necesita conocer este detalle — solo llama a render().

        :param chart_data: Datos estructurados del gráfico a renderizar.
        :return: Cadena con el resultado renderizado en el formato de la implementación.
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
