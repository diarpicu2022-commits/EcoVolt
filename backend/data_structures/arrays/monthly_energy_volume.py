"""
Volumen 3D de energía solar mensual en EcoVolt.
La dimensión panel × día × mes permite análisis granular de producción:
identificar días nublados, comparar rendimiento entre meses, y detectar
degradación progresiva de paneles a lo largo del año.
"""


DAYS_PER_MONTH: int = 31
MONTHS_PER_YEAR: int = 12


class MonthlyEnergyVolume:
    """
    Array 3D donde volume[panel_index][day][month] = kWh producido.
    Almacena un año completo de producción energética por panel,
    con granularidad diaria, permitiendo análisis estacionales y detección
    de anomalías en la generación fotovoltaica.

    Convención de índices:
    - panel_index: 0-based
    - day: 0-based (0 = día 1, 30 = día 31)
    - month: 0-based (0 = enero, 11 = diciembre)
    """

    def __init__(self, num_panels: int) -> None:
        if num_panels <= 0:
            raise ValueError("El número de paneles debe ser mayor a cero.")
        self.__num_panels: int = num_panels
        # Tres dimensiones: paneles × días × meses; todos inician en 0.0
        self.__energy_volume: list[list[list[float]]] = [
            [[0.0] * MONTHS_PER_YEAR for _ in range(DAYS_PER_MONTH)]
            for _ in range(num_panels)
        ]

    def get(self, panel_index: int, day: int, month: int) -> float:
        """
        Retorna los kWh producidos por el panel en el día y mes indicados.
        Lanza IndexError si algún índice está fuera del rango válido.
        """
        self.__validate_all_indices(panel_index, day, month)
        return self.__energy_volume[panel_index][day][month]

    def set(self, panel_index: int, day: int, month: int, kwh_value: float) -> None:
        """
        Registra la energía producida por un panel en un día y mes específicos.
        No permite valores negativos ya que la producción solar es siempre >= 0.
        """
        self.__validate_all_indices(panel_index, day, month)
        if kwh_value < 0.0:
            raise ValueError(
                f"El valor de energía {kwh_value} kWh no puede ser negativo."
            )
        self.__energy_volume[panel_index][day][month] = kwh_value

    def get_panel_monthly_total(self, panel_index: int, month: int) -> float:
        """
        Calcula la energía total producida por un panel durante un mes completo.
        Suma los 31 días del panel y mes especificados.
        Los días sin datos reales permanecen en 0.0.
        """
        self.__validate_panel_index(panel_index)
        self.__validate_month_index(month)
        return sum(
            self.__energy_volume[panel_index][day_idx][month]
            for day_idx in range(DAYS_PER_MONTH)
        )

    def get_annual_total(self, panel_index: int) -> float:
        """
        Calcula la energía total producida por un panel durante todo el año.
        Suma los 12 meses y hasta 31 días por mes del panel especificado.
        Útil para calcular el rendimiento anual y ROI de la instalación.
        """
        self.__validate_panel_index(panel_index)
        annual_kwh = 0.0
        for month_idx in range(MONTHS_PER_YEAR):
            for day_idx in range(DAYS_PER_MONTH):
                annual_kwh += self.__energy_volume[panel_index][day_idx][month_idx]
        return annual_kwh

    def __validate_all_indices(self, panel_index: int, day: int, month: int) -> None:
        """
        Valida los tres índices en una sola llamada para reducir duplicación.
        """
        self.__validate_panel_index(panel_index)
        self.__validate_day_index(day)
        self.__validate_month_index(month)

    def __validate_panel_index(self, panel_index: int) -> None:
        if not (0 <= panel_index < self.__num_panels):
            raise IndexError(
                f"Índice de panel {panel_index} fuera de rango. "
                f"El volumen tiene {self.__num_panels} paneles (0-{self.__num_panels - 1})."
            )

    def __validate_day_index(self, day: int) -> None:
        if not (0 <= day < DAYS_PER_MONTH):
            raise IndexError(
                f"Día {day} fuera de rango. "
                f"El mes tiene hasta {DAYS_PER_MONTH} días (0-{DAYS_PER_MONTH - 1})."
            )

    def __validate_month_index(self, month: int) -> None:
        if not (0 <= month < MONTHS_PER_YEAR):
            raise IndexError(
                f"Mes {month} fuera de rango. "
                f"El año tiene {MONTHS_PER_YEAR} meses (0-{MONTHS_PER_YEAR - 1})."
            )

    @property
    def num_panels(self) -> int:
        return self.__num_panels

    def __repr__(self) -> str:
        return (
            f"MonthlyEnergyVolume(panels={self.__num_panels}, "
            f"days={DAYS_PER_MONTH}, months={MONTHS_PER_YEAR})"
        )
