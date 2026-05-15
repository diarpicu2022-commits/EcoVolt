"""
Patrón Builder: Director que orquesta la construcción de reportes de energía EcoVolt.
Define recetas predefinidas de construcción usando el EnergyReportBuilder.
"""

from datetime import datetime
from patterns.creational.energy_report_builder import EnergyReportBuilder, EnergyReport


class EnergyReportDirector:
    """
    Director del patrón Builder para reportes de energía del sistema solar EcoVolt.
    Encapsula las secuencias de construcción más comunes, liberando al cliente
    de conocer el orden y los pasos necesarios para ensamblar cada tipo de reporte.
    """

    def __init__(self, builder: EnergyReportBuilder) -> None:
        """
        Inicializa el director con el builder a utilizar para construir reportes.
        El builder puede sustituirse en tiempo de ejecución si se requiere.
        """
        # Builder concreto que el director usará para ensamblar los reportes
        self.__builder: EnergyReportBuilder = builder

    @property
    def builder(self) -> EnergyReportBuilder:
        """Retorna el builder actualmente configurado en el director."""
        return self.__builder

    @builder.setter
    def builder(self, new_builder: EnergyReportBuilder) -> None:
        """Permite sustituir el builder del director en tiempo de ejecución."""
        self.__builder = new_builder

    def build_daily_report(
        self,
        panel_data: dict,
        battery_data: dict,
    ) -> EnergyReport:
        """
        Construye un reporte diario con resumen de paneles y baterías.
        Incluye solo las secciones esenciales para el monitoreo cotidiano.
        """
        report_date = datetime.now().strftime("%Y-%m-%d")
        return (
            self.__builder
            .set_title(f"Reporte Diario EcoVolt — {report_date}")
            .add_panel_summary(panel_data)
            .add_battery_summary(battery_data)
            .build()
        )

    def build_weekly_report(
        self,
        panel_data: dict,
        battery_data: dict,
        alert_data: dict,
    ) -> EnergyReport:
        """
        Construye un reporte semanal con paneles, baterías y resumen de alertas.
        Proporciona una visión extendida para análisis de tendencias semanales.
        """
        report_date = datetime.now().strftime("%Y-%m-%d")
        return (
            self.__builder
            .set_title(f"Reporte Semanal EcoVolt — Semana del {report_date}")
            .add_panel_summary(panel_data)
            .add_battery_summary(battery_data)
            .add_alert_summary(alert_data)
            .build()
        )

    def build_full_report(
        self,
        panel_data: dict,
        battery_data: dict,
        alert_data: dict,
        stats: dict,
    ) -> EnergyReport:
        """
        Construye un reporte completo con todas las secciones disponibles.
        Incluye paneles, baterías, alertas y estadísticas de producción completas.
        """
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            self.__builder
            .set_title(f"Reporte Completo EcoVolt — {report_date}")
            .add_panel_summary(panel_data)
            .add_battery_summary(battery_data)
            .add_alert_summary(alert_data)
            .add_production_stats(stats)
            .build()
        )
