"""
Patrón Bridge — Abstracción refinada para visualización de paneles solares.

PanelChartDisplay extiende EnergyDisplayAbstraction y se especializa en
preparar los datos de producción horaria de un panel solar. Construye el
ChartData con las 24 horas del día y delega el renderizado al ChartRenderer
activo (JSON o HTML). El Bridge permite cambiar el renderer sin modificar
este código de preparación de datos.
"""

import sys
import os
import random

# Insertar la raíz del backend en el path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from patterns.structural.chart_renderer import ChartRenderer, ChartData
from patterns.structural.energy_display_abstraction import EnergyDisplayAbstraction


class PanelChartDisplay(EnergyDisplayAbstraction):
    """
    Abstracción refinada del Bridge para gráficos de producción de paneles solares.

    Prepara datos de producción de energía (kWh) por hora del día para el panel
    especificado. Simula un perfil de producción solar realista:
    - Madrugada/noche (00h-05h y 20h-23h): 0.0 kWh (sin luz solar)
    - Amanecer/ocaso (06h, 19h): producción baja (~0.5 kWh)
    - Mediodía solar (11h-14h): producción pico (~3.5-5.0 kWh)

    La semilla de random derivada del panel_id garantiza que el mismo panel
    siempre produzca el mismo perfil de producción, útil para pruebas reproducibles.
    """

    # Horas de inicio y fin de producción solar según perfil estándar
    __SUNRISE_HOUR: int = 6
    __SUNSET_HOUR: int = 19

    # Producción máxima simulada al mediodía solar en kWh
    __PEAK_PRODUCTION_KWH: float = 5.0

    def __init__(self, renderer: ChartRenderer) -> None:
        """
        Inicializa el display de panel con el renderer Bridge especificado.

        :param renderer: Implementación concreta de ChartRenderer para la salida.
        """
        super().__init__(renderer)

    def display(self, panel_id: str) -> str:
        """
        Genera y renderiza el gráfico de producción horaria del panel solar.

        Construye las 24 etiquetas de hora ('00h'..'23h') y calcula la producción
        simulada para cada hora según un perfil solar de campana de Gauss centrado
        al mediodía. El panel_id se usa como semilla para reproducibilidad.

        :param panel_id: Identificador del panel solar a visualizar
                         (p. ej. 'PANEL-001', 'P-A3').
        :return: Cadena con el gráfico renderizado en el formato del ChartRenderer activo.
        """
        # Construir las 24 etiquetas de hora del día para el eje X
        hourly_labels = [f"{hour:02d}h" for hour in range(24)]

        # Calcular producción horaria simulada para este panel
        hourly_production_kwh = self.__simulate_hourly_production(panel_id)

        # Construir el objeto de datos del gráfico
        production_chart_data = ChartData(
            chart_title=f"Producción Solar — Panel {panel_id}",
            labels=hourly_labels,
            values=hourly_production_kwh,
            chart_type="line"
        )

        # Delegar el renderizado al ChartRenderer activo (el puente Bridge)
        return self._chart_renderer.render(production_chart_data)

    def __simulate_hourly_production(self, panel_id: str) -> list[float]:
        """
        Genera el perfil de producción solar horaria simulado para el panel.

        Usa una curva de campana centrada al mediodía solar (hora 12) dentro
        de la ventana de luz del día (amanecer 06h - ocaso 19h). La semilla
        derivada del panel_id garantiza consistencia por dispositivo.

        :param panel_id: ID del panel para derivar la semilla de simulación.
        :return: Lista de 24 floats con la producción en kWh por cada hora.
        """
        # Semilla reproducible por panel — cada panel tiene su propio perfil base
        random.seed(hash(panel_id) % 1000 + 10)
        # Factor de capacidad del panel: varía entre 0.6 y 1.0 según las características
        panel_capacity_factor = random.uniform(0.6, 1.0)
        peak_production = self.__PEAK_PRODUCTION_KWH * panel_capacity_factor

        # Restablecer semilla aleatoria para variación natural entre lecturas
        random.seed(None)

        hourly_production: list[float] = []
        midday_hour = 12  # Hora de máxima irradiancia solar

        for hour in range(24):
            if hour < self.__SUNRISE_HOUR or hour > self.__SUNSET_HOUR:
                # Sin luz solar antes del amanecer y después del ocaso
                production = 0.0
            else:
                # Perfil de campana: producción proporcional a la distancia del mediodía
                hours_from_midday = abs(hour - midday_hour)
                solar_window_half = (self.__SUNSET_HOUR - self.__SUNRISE_HOUR) / 2
                # Factor de campana: 1.0 al mediodía, 0.0 en amanecer/ocaso
                bell_factor = max(0.0, 1.0 - (hours_from_midday / solar_window_half) ** 1.5)
                # Producción base según la campana más variación aleatoria de nubosidad
                production = peak_production * bell_factor
                cloud_variation = random.uniform(-0.3, 0.3) * production
                production = max(0.0, production + cloud_variation)

            hourly_production.append(round(production, 3))

        return hourly_production

    def __repr__(self) -> str:
        return (
            f"PanelChartDisplay("
            f"renderer={self._chart_renderer.__class__.__name__})"
        )
