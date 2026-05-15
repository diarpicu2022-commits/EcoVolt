"""
Patrón Factory Method: Creator concreto para lecturas de temperatura.
Crea productos de tipo SensorReadingProduct especializados en medición de temperatura.
"""

from patterns.creational.sensor_reading_creator import (
    SensorReadingCreator,
    SensorReadingProduct,
)


class TemperatureReadingCreator(SensorReadingCreator):
    """
    Creator concreto que fabrica lecturas de temperatura para paneles solares.
    Implementa el factory_method para producir SensorReadingProduct de tipo TEMPERATURA.
    """

    def factory_method(self, panel_id: str, value: float) -> SensorReadingProduct:
        """
        Crea una lectura de temperatura para el panel indicado.
        La unidad de medida es grados Celsius (°C) y el tipo es TEMPERATURA.
        """
        timestamp = self._current_timestamp()
        return SensorReadingProduct(
            panel_id=panel_id,
            reading_type="TEMPERATURA",
            value=value,
            unit="°C",
            timestamp=timestamp,
        )
