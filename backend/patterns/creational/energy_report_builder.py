"""
Patrón Builder: Constructor paso a paso de reportes de energía del sistema EcoVolt.
Separa la construcción de un reporte complejo de su representación final.
"""

from datetime import datetime
from typing import Optional


class EnergyReport:
    """
    Producto complejo que representa un reporte de energía del sistema solar.
    Sus secciones son opcionales y se ensamblan mediante el Builder.
    """

    def __init__(self) -> None:
        # Título descriptivo del reporte de energía
        self.title: str = ""
        # Fecha y hora de generación del reporte
        self.generation_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Resumen de estado y producción de los paneles solares
        self.panel_summary: Optional[dict] = None
        # Resumen del estado de las baterías del sistema
        self.battery_summary: Optional[dict] = None
        # Resumen de alertas generadas durante el período analizado
        self.alert_summary: Optional[dict] = None
        # Estadísticas de producción energética del período
        self.production_stats: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convierte el reporte a un diccionario serializable para exportación o API."""
        return {
            "title": self.title,
            "generation_date": self.generation_date,
            "panel_summary": self.panel_summary,
            "battery_summary": self.battery_summary,
            "alert_summary": self.alert_summary,
            "production_stats": self.production_stats,
        }

    def __repr__(self) -> str:
        """Representación legible del reporte para depuración."""
        sections = []
        if self.panel_summary is not None:
            sections.append("paneles")
        if self.battery_summary is not None:
            sections.append("baterías")
        if self.alert_summary is not None:
            sections.append("alertas")
        if self.production_stats is not None:
            sections.append("estadísticas")
        sections_str = ", ".join(sections) if sections else "sin secciones"
        return f"EnergyReport(title='{self.title}', secciones=[{sections_str}])"


class EnergyReportBuilder:
    """
    Builder concreto que construye un EnergyReport paso a paso.
    Cada método de configuración retorna self para permitir encadenamiento de llamadas.
    """

    def __init__(self) -> None:
        """Inicializa el builder con un reporte vacío listo para configurar."""
        # Reporte interno que se ensambla progresivamente
        self.__report: EnergyReport = EnergyReport()

    def set_title(self, title: str) -> 'EnergyReportBuilder':
        """
        Establece el título del reporte.
        Retorna self para permitir encadenamiento de métodos.
        """
        self.__report.title = title
        return self

    def add_panel_summary(self, panel_data: dict) -> 'EnergyReportBuilder':
        """
        Agrega el resumen de estado de los paneles solares al reporte.
        Retorna self para permitir encadenamiento de métodos.
        """
        self.__report.panel_summary = panel_data
        return self

    def add_battery_summary(self, battery_data: dict) -> 'EnergyReportBuilder':
        """
        Agrega el resumen del estado de las baterías al reporte.
        Retorna self para permitir encadenamiento de métodos.
        """
        self.__report.battery_summary = battery_data
        return self

    def add_alert_summary(self, alert_data: dict) -> 'EnergyReportBuilder':
        """
        Agrega el resumen de alertas del sistema al reporte.
        Retorna self para permitir encadenamiento de métodos.
        """
        self.__report.alert_summary = alert_data
        return self

    def add_production_stats(self, stats: dict) -> 'EnergyReportBuilder':
        """
        Agrega las estadísticas de producción energética al reporte.
        Retorna self para permitir encadenamiento de métodos.
        """
        self.__report.production_stats = stats
        return self

    def build(self) -> EnergyReport:
        """
        Finaliza la construcción y retorna el EnergyReport ensamblado.
        Reinicia el builder interno para permitir la creación de un nuevo reporte.
        """
        finished_report = self.__report
        # Reinicia el builder para que pueda reutilizarse en reportes futuros
        self.__report = EnergyReport()
        return finished_report
