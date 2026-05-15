"""
Patrón Abstract Factory: Interfaz abstracta para familias de productos de paneles solares.
Define los contratos para crear paneles y sensores compatibles entre sí.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PanelProduct:
    """
    Producto abstracto que representa un panel solar con sus características técnicas.
    Cada familia de fábricas produce una variante concreta de este producto.
    """
    # Identificador único del panel solar
    panel_id: str
    # Tipo de tecnología del panel: MONOCRISTALINO, POLICRISTALINO, PELICULA_DELGADA
    panel_type: str
    # Eficiencia de conversión energética expresada como proporción (0.0 - 1.0)
    efficiency: float
    # Potencia pico del panel en vatios bajo condiciones estándar de prueba
    peak_power_watts: float


@dataclass
class SensorProduct:
    """
    Producto abstracto que representa un sensor compatible con un panel solar.
    Cada familia de fábricas produce una variante concreta de este producto.
    """
    # Identificador único del sensor
    sensor_id: str
    # Tipo de sensor: SENSOR_PRECISION, SENSOR_ESTANDAR, SENSOR_FLEXIBLE
    sensor_type: str
    # Unidad de medida del sensor, por ejemplo W/m²
    measurement_unit: str


class SolarPanelAbstractFactory(ABC):
    """
    Fábrica abstracta que declara los métodos de creación para familias de productos solares.
    Las subclases concretas implementan cada método para producir productos compatibles.
    """

    @abstractmethod
    def create_panel(self, panel_id: str) -> PanelProduct:
        """
        Crea y retorna un PanelProduct correspondiente a la familia de tecnología concreta.
        """
        ...

    @abstractmethod
    def create_sensor(self, sensor_id: str) -> SensorProduct:
        """
        Crea y retorna un SensorProduct compatible con el panel de la misma familia.
        """
        ...
