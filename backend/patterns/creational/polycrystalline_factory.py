"""
Patrón Abstract Factory: Fábrica concreta para paneles y sensores policristalinos.
Produce la familia de productos de eficiencia intermedia y costo moderado del sistema EcoVolt.
"""

from patterns.creational.solar_panel_abstract_factory import (
    SolarPanelAbstractFactory,
    PanelProduct,
    SensorProduct,
)


class PolycrystallineFactory(SolarPanelAbstractFactory):
    """
    Fábrica concreta que produce paneles policristalinos y sus sensores estándar.
    Esta familia ofrece eficiencia moderada (17%) y potencia pico de 300 W.
    """

    def create_panel(self, panel_id: str) -> PanelProduct:
        """
        Crea un panel solar policristalino con eficiencia estándar.
        Tipo: POLICRISTALINO | Eficiencia: 17% | Potencia pico: 300 W.
        """
        return PanelProduct(
            panel_id=panel_id,
            panel_type="POLICRISTALINO",
            efficiency=0.17,
            peak_power_watts=300.0,
        )

    def create_sensor(self, sensor_id: str) -> SensorProduct:
        """
        Crea un sensor estándar compatible con paneles policristalinos.
        Tipo: SENSOR_ESTANDAR | Unidad: W/m².
        """
        return SensorProduct(
            sensor_id=sensor_id,
            sensor_type="SENSOR_ESTANDAR",
            measurement_unit="W/m²",
        )
