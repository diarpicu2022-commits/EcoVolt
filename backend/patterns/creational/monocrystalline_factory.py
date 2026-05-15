"""
Patrón Abstract Factory: Fábrica concreta para paneles y sensores monocristalinos.
Produce la familia de productos de mayor eficiencia del sistema EcoVolt.
"""

from patterns.creational.solar_panel_abstract_factory import (
    SolarPanelAbstractFactory,
    PanelProduct,
    SensorProduct,
)


class MonocrystallineFactory(SolarPanelAbstractFactory):
    """
    Fábrica concreta que produce paneles monocristalinos y sus sensores de precisión.
    Esta familia ofrece la mayor eficiencia (22%) y mayor potencia pico (400 W).
    """

    def create_panel(self, panel_id: str) -> PanelProduct:
        """
        Crea un panel solar monocristalino con alta eficiencia.
        Tipo: MONOCRISTALINO | Eficiencia: 22% | Potencia pico: 400 W.
        """
        return PanelProduct(
            panel_id=panel_id,
            panel_type="MONOCRISTALINO",
            efficiency=0.22,
            peak_power_watts=400.0,
        )

    def create_sensor(self, sensor_id: str) -> SensorProduct:
        """
        Crea un sensor de precisión compatible con paneles monocristalinos.
        Tipo: SENSOR_PRECISION | Unidad: W/m².
        """
        return SensorProduct(
            sensor_id=sensor_id,
            sensor_type="SENSOR_PRECISION",
            measurement_unit="W/m²",
        )
