"""
Patrón Bridge — Abstracción refinada para visualización de baterías.

BatteryChartDisplay extiende EnergyDisplayAbstraction y se especializa en
preparar datos del estado de carga (SoC, State of Charge) de una batería
durante las últimas 12 horas. Usa el ChartRenderer activo para el renderizado
sin conocer si la salida será JSON, HTML u otro formato.
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Insertar la raíz del backend en el path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from patterns.structural.chart_renderer import ChartRenderer, ChartData
from patterns.structural.energy_display_abstraction import EnergyDisplayAbstraction


class BatteryChartDisplay(EnergyDisplayAbstraction):
    """
    Abstracción refinada del Bridge para gráficos de estado de carga de baterías.

    Muestra el porcentaje de carga (SoC) de la batería para cada una de las
    últimas 12 horas. El perfil simulado refleja el comportamiento típico de una
    batería de respaldo solar:
    - Carga durante horas de producción solar (se sube al 100%).
    - Descarga durante la noche por consumo de cargas activas.

    La semilla derivada del battery_id garantiza que el mismo dispositivo
    siempre produzca el mismo perfil base, reproducible en pruebas.
    """

    # Número de horas del historial a mostrar en el gráfico
    __HISTORY_HOURS: int = 12

    # Estado de carga máximo y mínimo del sistema EcoVolt (porcentaje)
    __SOC_MAX_PERCENT: float = 100.0
    __SOC_MIN_PERCENT: float = 10.0

    # Umbral de batería baja según configuración estándar EcoVolt
    __LOW_BATTERY_THRESHOLD_PERCENT: float = 20.0

    def __init__(self, renderer: ChartRenderer) -> None:
        """
        Inicializa el display de batería con el renderer Bridge especificado.

        :param renderer: Implementación concreta de ChartRenderer para la salida.
        """
        super().__init__(renderer)

    def display(self, battery_id: str) -> str:
        """
        Genera y renderiza el gráfico de estado de carga de la batería.

        Construye las etiquetas de las últimas 12 horas en formato 'HH:00'
        y simula el historial de SoC hora por hora. El battery_id se usa como
        semilla de simulación para consistencia por dispositivo.

        :param battery_id: Identificador de la batería a visualizar
                           (p. ej. 'BAT-001', 'LITIO-A1').
        :return: Cadena con el gráfico renderizado en el formato del ChartRenderer activo.
        """
        # Generar etiquetas de las últimas 12 horas en formato 'HH:00'
        hourly_labels = self.__build_last_12_hour_labels()

        # Calcular historial de estado de carga simulado para esta batería
        soc_history_percent = self.__simulate_soc_history(battery_id)

        # Construir el objeto de datos del gráfico de batería
        battery_chart_data = ChartData(
            chart_title=f"Estado de Carga — Batería {battery_id}",
            labels=hourly_labels,
            values=soc_history_percent,
            chart_type="line"
        )

        # Delegar el renderizado al ChartRenderer activo (el puente Bridge)
        return self._chart_renderer.render(battery_chart_data)

    def __build_last_12_hour_labels(self) -> list[str]:
        """
        Construye las etiquetas de tiempo para las últimas 12 horas.

        Las etiquetas se generan hacia atrás desde la hora actual para reflejar
        el historial cronológico real en el eje X del gráfico.

        :return: Lista de 12 cadenas en formato 'HH:00' desde hace 11 horas hasta ahora.
        """
        reference_time = datetime.now()
        hour_labels: list[str] = []

        for hours_back in range(self.__HISTORY_HOURS - 1, -1, -1):
            # Calcular la hora correspondiente restando las horas hacia atrás
            past_hour = reference_time - timedelta(hours=hours_back)
            hour_labels.append(past_hour.strftime("%H:00"))

        return hour_labels

    def __simulate_soc_history(self, battery_id: str) -> list[float]:
        """
        Simula el historial de estado de carga (SoC) para las últimas 12 horas.

        El perfil refleja el comportamiento típico de una batería solar:
        - Durante horas diurnas (08h-18h): tendencia de carga por producción solar.
        - Durante horas nocturnas: tendencia de descarga por consumo de cargas.
        - Con variaciones aleatorias para simular cambios de consumo/generación.

        :param battery_id: ID de la batería para derivar la semilla de simulación.
        :return: Lista de 12 floats con el SoC en porcentaje (%) por cada hora.
        """
        # Semilla reproducible por batería — determina el SoC inicial del historial
        random.seed(hash(battery_id) % 1000 + 20)
        # Estado de carga de inicio del historial (12 horas atrás)
        initial_soc = random.uniform(40.0, 85.0)

        # Restablecer semilla para variaciones naturales de la simulación
        random.seed(None)

        reference_time = datetime.now()
        soc_history: list[float] = []
        current_soc = initial_soc

        for hours_back in range(self.__HISTORY_HOURS - 1, -1, -1):
            # Determinar la hora del día para calcular la tendencia de carga/descarga
            past_hour_time = reference_time - timedelta(hours=hours_back)
            hour_of_day = past_hour_time.hour

            # Tendencia por hora del día: carga solar de 8h a 18h, descarga el resto
            if 8 <= hour_of_day <= 18:
                # Producción solar: tendencia de carga (+2% a +6% por hora)
                trend_percent = random.uniform(2.0, 6.0)
            else:
                # Consumo nocturno: tendencia de descarga (-1% a -4% por hora)
                trend_percent = random.uniform(-4.0, -1.0)

            # Aplicar variación aleatoria adicional por consumo irregular y nubes
            random_variation = random.uniform(-2.0, 2.0)
            current_soc += trend_percent + random_variation

            # Mantener el SoC dentro de los límites físicos del sistema
            current_soc = max(self.__SOC_MIN_PERCENT, min(self.__SOC_MAX_PERCENT, current_soc))
            soc_history.append(round(current_soc, 1))

        return soc_history

    def __repr__(self) -> str:
        return (
            f"BatteryChartDisplay("
            f"renderer={self._chart_renderer.__class__.__name__})"
        )
