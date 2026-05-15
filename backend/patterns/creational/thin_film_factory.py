"""
Patrón Abstract Factory: Fábrica concreta para paneles y sensores de película delgada.
Produce la familia de productos más ligeros y flexibles del sistema EcoVolt.
"""

from patterns.creational.solar_panel_abstract_factory import (
    SolarPanelAbstractFactory,
    PanelProduct,
    SensorProduct,
)


class ThinFilmFactory(SolarPanelAbstractFactory):
    """
    Fábrica concreta que produce paneles de película delgada y sus sensores flexibles.
    Esta familia ofrece la menor eficiencia (13%) pero mayor flexibilidad de instalación,
    con una potencia pico de 200 W.
    """

    def create_panel(self, panel_id: str) -> PanelProduct:
        """
        Crea un panel solar de película delgada con alta flexibilidad.
        Tipo: PELICULA_DELGADA | Eficiencia: 13% | Potencia pico: 200 W.
        """
        return PanelProduct(
            panel_id=panel_id,
            panel_type="PELICULA_DELGADA",
            efficiency=0.13,
            peak_power_watts=200.0,
        )

    def create_sensor(self, sensor_id: str) -> SensorProduct:
        """
        Crea un sensor flexible compatible con paneles de película delgada.
        Tipo: SENSOR_FLEXIBLE | Unidad: W/m².
        """
        return SensorProduct(
            sensor_id=sensor_id,
            sensor_type="SENSOR_FLEXIBLE",
            measurement_unit="W/m²",
        )
