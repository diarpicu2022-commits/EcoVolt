"""
Patrón Prototype: Clonación de configuraciones de paneles solares del sistema EcoVolt.
Permite crear nuevas configuraciones a partir de prototipos existentes sin acoplar al cliente
con los detalles de inicialización de cada tipo de panel.
"""

import copy
import uuid
from typing import Optional


class PanelConfiguration:
    """
    Prototipo de configuración para un panel solar del sistema EcoVolt.
    Soporta clonación profunda (deep copy) y superficial (shallow copy)
    para diferentes escenarios de reutilización de configuraciones.
    """

    def __init__(
        self,
        panel_id: str,
        panel_type: str,
        peak_power_watts: float,
        surface_area_m2: float,
        installation_location: str,
        monitoring_interval_seconds: int,
    ) -> None:
        # Identificador único del panel solar
        self.panel_id: str = panel_id
        # Tipo de tecnología del panel: MONOCRISTALINO, POLICRISTALINO, PELICULA_DELGADA
        self.panel_type: str = panel_type
        # Potencia pico del panel en vatios bajo condiciones estándar de prueba
        self.peak_power_watts: float = peak_power_watts
        # Área de superficie del panel en metros cuadrados
        self.surface_area_m2: float = surface_area_m2
        # Ubicación física de instalación del panel en la instalación
        self.installation_location: str = installation_location
        # Intervalo de monitoreo del sensor en segundos
        self.monitoring_interval_seconds: int = monitoring_interval_seconds

    def clone(self) -> 'PanelConfiguration':
        """
        Realiza una copia PROFUNDA de esta configuración.
        El clon recibe un nuevo panel_id generado automáticamente para garantizar unicidad.
        Usa copy.deepcopy para copiar correctamente objetos anidados si los hubiera.
        """
        # Copia profunda: todos los atributos, incluidos objetos anidados, se duplican
        cloned_config: PanelConfiguration = copy.deepcopy(self)
        # Asigna un identificador único al clon para diferenciarlo del original
        cloned_config.panel_id = f"PANEL-{uuid.uuid4().hex[:8].upper()}"
        return cloned_config

    def shallow_clone(self) -> 'PanelConfiguration':
        """
        Realiza una copia SUPERFICIAL de esta configuración.
        El clon comparte referencias a objetos internos mutables con el original.
        Útil cuando los atributos son tipos primitivos y el rendimiento es prioritario.
        """
        # Copia superficial: referencias compartidas para atributos compuestos
        shallow_copy: PanelConfiguration = copy.copy(self)
        # También asigna un nuevo panel_id para evitar colisión de identificadores
        shallow_copy.panel_id = f"PANEL-{uuid.uuid4().hex[:8].upper()}"
        return shallow_copy

    def to_dict(self) -> dict:
        """Convierte la configuración del panel a un diccionario serializable."""
        return {
            "panel_id": self.panel_id,
            "panel_type": self.panel_type,
            "peak_power_watts": self.peak_power_watts,
            "surface_area_m2": self.surface_area_m2,
            "installation_location": self.installation_location,
            "monitoring_interval_seconds": self.monitoring_interval_seconds,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PanelConfiguration':
        """
        Crea una instancia de PanelConfiguration a partir de un diccionario.
        Útil para deserializar configuraciones almacenadas en base de datos o JSON.
        """
        return cls(
            panel_id=data["panel_id"],
            panel_type=data["panel_type"],
            peak_power_watts=float(data["peak_power_watts"]),
            surface_area_m2=float(data["surface_area_m2"]),
            installation_location=data["installation_location"],
            monitoring_interval_seconds=int(data["monitoring_interval_seconds"]),
        )

    def __repr__(self) -> str:
        """Representación legible de la configuración del panel para depuración."""
        return (
            f"PanelConfiguration("
            f"panel_id='{self.panel_id}', "
            f"type='{self.panel_type}', "
            f"peak_power={self.peak_power_watts}W, "
            f"area={self.surface_area_m2}m², "
            f"location='{self.installation_location}', "
            f"interval={self.monitoring_interval_seconds}s)"
        )
