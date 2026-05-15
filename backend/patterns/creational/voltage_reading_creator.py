"""
Patrón Factory Method: Creator concreto para lecturas de voltaje.
Crea productos de tipo SensorReadingProduct especializados en medición de voltaje.
"""

from patterns.creational.sensor_reading_creator import (
    SensorReadingCreator,
    SensorReadingProduct,
)


class VoltageReadingCreator(SensorReadingCreator):
    """
    Creator concreto que fabrica lecturas de voltaje para paneles solares.
    Implementa el factory_method para producir SensorReadingProduct de tipo VOLTAJE.
    """

    def factory_method(self, panel_id: str, value: float) -> SensorReadingProduct:
        """
        Crea una lectura de voltaje para el panel indicado.
        La unidad de medida es Voltios (V) y el tipo es VOLTAJE.
        """
        timestamp = self._current_timestamp()
        return SensorReadingProduct(
            panel_id=panel_id,
            reading_type="VOLTAJE",
            value=value,
            unit="V",
            timestamp=timestamp,
        )
