"""
Patrón Factory Method: Creator abstracto para lecturas de sensores solares.
Define la interfaz de creación y el producto base que todos los creadores deben implementar.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from patterns.creational.system_logger import SystemLogger


class SensorReadingProduct:
    """
    Producto base que representa una lectura de sensor de un panel solar.
    Contiene los datos esenciales de cualquier tipo de medición.
    """

    def __init__(
        self,
        panel_id: str,
        reading_type: str,
        value: float,
        unit: str,
        timestamp: str,
    ) -> None:
        # Identificador único del panel solar al que pertenece la lectura
        self.panel_id: str = panel_id
        # Tipo de lectura: VOLTAJE, CORRIENTE, TEMPERATURA, etc.
        self.reading_type: str = reading_type
        # Valor numérico medido por el sensor
        self.value: float = value
        # Unidad de medida: V, A, °C, etc.
        self.unit: str = unit
        # Marca de tiempo en que se tomó la lectura
        self.timestamp: str = timestamp

    def __repr__(self) -> str:
        """Representación legible de la lectura del sensor."""
        return (
            f"SensorReadingProduct("
            f"panel_id='{self.panel_id}', "
            f"type='{self.reading_type}', "
            f"value={self.value} {self.unit}, "
            f"timestamp='{self.timestamp}')"
        )


class SensorReadingCreator(ABC):
    """
    Creator abstracto del patrón Factory Method.
    Declara el método de fábrica que las subclases concretas deben implementar.
    """

    @abstractmethod
    def factory_method(self, panel_id: str, value: float) -> SensorReadingProduct:
        """
        Método de fábrica abstracto que crea y retorna un SensorReadingProduct.
        Cada subclase define el tipo específico de lectura a crear.
        """
        ...

    def create_and_log(self, panel_id: str, value: float) -> SensorReadingProduct:
        """
        Llama al factory_method para crear la lectura y la registra con el SystemLogger.
        Este es el método principal que deben usar los clientes.
        """
        # Delega la creación al método de fábrica de la subclase concreta
        reading = self.factory_method(panel_id, value)

        # Registra la lectura creada usando el logger global del sistema
        logger = SystemLogger.get_instance()
        logger.log_info(
            f"Lectura creada — Panel: {reading.panel_id} | "
            f"Tipo: {reading.reading_type} | "
            f"Valor: {reading.value} {reading.unit} | "
            f"Timestamp: {reading.timestamp}"
        )

        return reading

    @staticmethod
    def _current_timestamp() -> str:
        """Genera un timestamp en formato ISO 8601 para la lectura actual."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
