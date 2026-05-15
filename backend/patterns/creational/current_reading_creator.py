"""
Patrón Factory Method: Creator concreto para lecturas de corriente eléctrica.
Crea productos de tipo SensorReadingProduct especializados en medición de corriente.
"""

from patterns.creational.sensor_reading_creator import (
    SensorReadingCreator,
    SensorReadingProduct,
)


class CurrentReadingCreator(SensorReadingCreator):
    """
    Creator concreto que fabrica lecturas de corriente eléctrica para paneles solares.
    Implementa el factory_method para producir SensorReadingProduct de tipo CORRIENTE.
    """

    def factory_method(self, panel_id: str, value: float) -> SensorReadingProduct:
        """
        Crea una lectura de corriente eléctrica para el panel indicado.
        La unidad de medida es Amperios (A) y el tipo es CORRIENTE.
        """
        timestamp = self._current_timestamp()
        return SensorReadingProduct(
            panel_id=panel_id,
            reading_type="CORRIENTE",
            value=value,
            unit="A",
            timestamp=timestamp,
        )
