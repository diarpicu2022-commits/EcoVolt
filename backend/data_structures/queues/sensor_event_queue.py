"""
Cola FIFO para eventos de lectura de sensores del sistema solar EcoVolt.
Los sensores de voltaje, corriente y temperatura generan eventos continuos
que deben procesarse en el orden exacto de llegada para mantener integridad
de los datos históricos de cada panel.
"""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Generic

# E representa cualquier tipo de evento de sensor solar
E = TypeVar("E")


@dataclass
class SensorEvent:
    """
    Representa un evento puntual de lectura de un sensor físico instalado
    en un panel solar. Cada evento captura un instante de medición.
    """

    __panel_id: str = field(default="")
    __reading_type: str = field(default="")   # 'voltage', 'current', 'temperature'
    __reading_value: float = field(default=0.0)
    __event_timestamp: datetime = field(default_factory=datetime.now)

    # Se usan propiedades porque dataclass con doble guion bajo requiere
    # inicialización explícita a través del constructor de la clase
    def __init__(
        self,
        panel_id: str,
        reading_type: str,
        reading_value: float,
        event_timestamp: datetime | None = None,
    ) -> None:
        self.__panel_id = panel_id
        self.__reading_type = reading_type
        self.__reading_value = reading_value
        # Si no se provee timestamp, se usa el momento exacto de creación
        self.__event_timestamp = event_timestamp if event_timestamp else datetime.now()

    @property
    def panel_id(self) -> str:
        return self.__panel_id

    @property
    def reading_type(self) -> str:
        return self.__reading_type

    @property
    def reading_value(self) -> float:
        return self.__reading_value

    @property
    def event_timestamp(self) -> datetime:
        return self.__event_timestamp

    def __repr__(self) -> str:
        return (
            f"SensorEvent(panel_id={self.__panel_id!r}, "
            f"reading_type={self.__reading_type!r}, "
            f"value={self.__reading_value}, "
            f"timestamp={self.__event_timestamp.isoformat()})"
        )


class SensorEventQueue(Generic[E]):
    """
    Cola genérica FIFO para eventos de sensores del sistema EcoVolt.
    Garantiza que las lecturas de voltaje, corriente y temperatura se
    procesen en el orden cronológico en que los sensores las generaron.
    Usa collections.deque para O(1) en ambos extremos.
    """

    def __init__(self) -> None:
        # deque eficiente para inserción al final y extracción al frente
        self.__sensor_events: deque[E] = deque()

    def enqueue(self, sensor_event: E) -> None:
        """
        Agrega un evento de sensor al final de la cola.
        Los eventos más recientes esperan detrás de los anteriores.
        """
        self.__sensor_events.append(sensor_event)

    def dequeue(self) -> E:
        """
        Elimina y retorna el evento de sensor más antiguo (frente).
        Lanza IndexError si la cola está vacía para evitar lecturas fantasma.
        """
        if self.is_empty():
            raise IndexError("No hay eventos de sensor en la cola.")
        return self.__sensor_events.popleft()

    def front(self) -> E:
        """
        Retorna el evento al frente sin eliminarlo.
        Permite inspeccionar el próximo evento a procesar.
        """
        if self.is_empty():
            raise IndexError("La cola de eventos de sensor está vacía.")
        return self.__sensor_events[0]

    def rear(self) -> E:
        """
        Retorna el evento más reciente (al final) sin eliminarlo.
        Útil para verificar el último evento registrado por un sensor.
        """
        if self.is_empty():
            raise IndexError("La cola de eventos de sensor está vacía.")
        return self.__sensor_events[-1]

    def is_empty(self) -> bool:
        """
        Indica si no hay eventos de sensor pendientes de procesar.
        """
        return len(self.__sensor_events) == 0

    def isEmpty(self) -> bool:
        return self.is_empty()

    def size(self) -> int:
        """
        Cantidad de eventos de sensor pendientes en la cola.
        """
        return len(self.__sensor_events)

    def clear(self) -> None:
        """
        Descarta todos los eventos pendientes.
        Se usa al reiniciar el pipeline de adquisición de datos de sensores.
        """
        self.__sensor_events.clear()

    def __repr__(self) -> str:
        return f"SensorEventQueue(pending_events={self.size()})"
