"""
Matriz 2D de producción de energía solar por panel y hora del día en EcoVolt.
La dimensión panel_index × hora_del_día permite identificar con precisión
en qué horas cada panel genera más o menos energía, facilitando el análisis
de sombras, suciedad o degradación de células fotovoltaicas.
"""

from typing import Optional


HOURS_PER_DAY: int = 24


class EnergyProductionMatrix:
    """
    Matriz 2D donde matrix[panel_index][hour_of_day] = kWh generado.
    Permite analizar el perfil horario de producción de cada panel
    y calcular totales diarios por panel o por hora del día completa.
    """

    def __init__(self, num_panels: int) -> None:
        if num_panels <= 0:
            raise ValueError("El número de paneles debe ser mayor a cero.")
        self.__num_panels: int = num_panels
        # Inicializa toda la matriz con 0.0 para representar sin producción
        self.__production_matrix: list[list[float]] = [
            [0.0] * HOURS_PER_DAY for _ in range(num_panels)
        ]

    def get(self, panel_index: int, hour_of_day: int) -> float:
        """
        Retorna los kWh generados por el panel indicado en la hora especificada.
        Lanza IndexError si alguno de los índices está fuera de rango.
        """
        self.__validate_panel_index(panel_index)
        self.__validate_hour_index(hour_of_day)
        return self.__production_matrix[panel_index][hour_of_day]

    def set(self, panel_index: int, hour_of_day: int, kwh_value: float) -> None:
        """
        Registra la energía producida por un panel en una hora específica.
        Lanza ValueError si kwh_value es negativo, ya que la producción
        solar nunca puede ser negativa en condiciones físicas reales.
        """
        self.__validate_panel_index(panel_index)
        self.__validate_hour_index(hour_of_day)
        if kwh_value < 0.0:
            raise ValueError(
                f"El valor de energía {kwh_value} kWh no puede ser negativo."
            )
        self.__production_matrix[panel_index][hour_of_day] = kwh_value

    def get_panel_daily_total(self, panel_index: int) -> float:
        """
        Calcula la energía total producida por un panel durante todo el día.
        Suma las 24 lecturas horarias del panel especificado.
        """
        self.__validate_panel_index(panel_index)
        return sum(self.__production_matrix[panel_index])

    def get_hour_total(self, hour_of_day: int) -> float:
        """
        Calcula la energía total generada por TODOS los paneles en una hora.
        Útil para identificar las horas pico de producción de toda la planta.
        """
        self.__validate_hour_index(hour_of_day)
        return sum(
            self.__production_matrix[panel_idx][hour_of_day]
            for panel_idx in range(self.__num_panels)
        )

    def get_full_matrix(self) -> list[list[float]]:
        """
        Retorna una copia profunda de la matriz completa de producción.
        Se usa copia para evitar modificaciones externas accidentales.
        """
        return [list(hour_readings) for hour_readings in self.__production_matrix]

    def __validate_panel_index(self, panel_index: int) -> None:
        if not (0 <= panel_index < self.__num_panels):
            raise IndexError(
                f"Índice de panel {panel_index} fuera de rango. "
                f"La matriz tiene {self.__num_panels} paneles (0-{self.__num_panels - 1})."
            )

    def __validate_hour_index(self, hour_of_day: int) -> None:
        if not (0 <= hour_of_day < HOURS_PER_DAY):
            raise IndexError(
                f"Hora {hour_of_day} fuera de rango. "
                f"El día tiene {HOURS_PER_DAY} horas (0-{HOURS_PER_DAY - 1})."
            )

    @property
    def num_panels(self) -> int:
        return self.__num_panels

    def __repr__(self) -> str:
        return (
            f"EnergyProductionMatrix(panels={self.__num_panels}, "
            f"hours_per_day={HOURS_PER_DAY})"
        )
