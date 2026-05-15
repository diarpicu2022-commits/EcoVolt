"""
Lista doblemente enlazada para el historial navegable de lecturas energéticas
del sistema solar EcoVolt. Permite moverse tanto hacia adelante como hacia
atrás en el tiempo, facilitando la auditoría y comparación de producción
energética entre períodos.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional


class HistoricalReading:
    """
    Registro histórico de energía producida por un panel solar en un
    período específico. Se usa para análisis retrospectivo de rendimiento.
    """

    def __init__(
        self,
        panel_id: str,
        energy_kwh: float,
        recorded_at: datetime | None = None,
    ) -> None:
        self.__panel_id = panel_id
        self.__energy_kwh = energy_kwh   # Energía producida en kWh
        # El momento de registro es crucial para el ordenamiento cronológico
        self.__recorded_at = recorded_at if recorded_at else datetime.now()

    @property
    def panel_id(self) -> str:
        return self.__panel_id

    @property
    def energy_kwh(self) -> float:
        return self.__energy_kwh

    @property
    def recorded_at(self) -> datetime:
        return self.__recorded_at

    def __repr__(self) -> str:
        return (
            f"HistoricalReading(panel_id={self.__panel_id!r}, "
            f"energy={self.__energy_kwh} kWh, "
            f"recorded_at={self.__recorded_at.isoformat()})"
        )


class ReadingHistoryNode:
    """
    Nodo de la lista doblemente enlazada. Mantiene referencias tanto al
    nodo anterior como al siguiente, habilitando navegación bidireccional
    por el historial de producción energética.
    """

    def __init__(self, historical_reading: HistoricalReading) -> None:
        # Enlace hacia el registro más antiguo (navegación hacia el pasado)
        self.__prev_node: Optional[ReadingHistoryNode] = None
        self.__historical_reading: HistoricalReading = historical_reading
        # Enlace hacia el registro más reciente (navegación hacia el futuro)
        self.__next_node: Optional[ReadingHistoryNode] = None

    @property
    def prev_node(self) -> Optional[ReadingHistoryNode]:
        return self.__prev_node

    @prev_node.setter
    def prev_node(self, node: Optional[ReadingHistoryNode]) -> None:
        self.__prev_node = node

    @property
    def historical_reading(self) -> HistoricalReading:
        return self.__historical_reading

    @property
    def next_node(self) -> Optional[ReadingHistoryNode]:
        return self.__next_node

    @next_node.setter
    def next_node(self, node: Optional[ReadingHistoryNode]) -> None:
        self.__next_node = node

    def __repr__(self) -> str:
        return f"ReadingHistoryNode(data={self.__historical_reading})"


class ReadingHistoryDoublyList:
    """
    Lista doblemente enlazada para almacenar y navegar el historial
    de lecturas energéticas del sistema EcoVolt. La navegación bidireccional
    permite comparar producción actual con registros anteriores sin recargar
    todos los datos desde la base de datos.
    """

    def __init__(self) -> None:
        self.__head_node: Optional[ReadingHistoryNode] = None
        self.__tail_node: Optional[ReadingHistoryNode] = None
        self.__record_count: int = 0

    def add_first(self, historical_reading: HistoricalReading) -> None:
        """
        Inserta un registro histórico al inicio de la lista en O(1).
        Útil para insertar el registro más antiguo al construir el historial.
        """
        new_node = ReadingHistoryNode(historical_reading)
        if self.__head_node is None:
            self.__head_node = new_node
            self.__tail_node = new_node
        else:
            # El nuevo nodo apunta al head actual antes de convertirse en head
            new_node.next_node = self.__head_node
            self.__head_node.prev_node = new_node
            self.__head_node = new_node
        self.__record_count += 1

    def add_last(self, historical_reading: HistoricalReading) -> None:
        """
        Inserta un registro histórico al final de la lista en O(1).
        Es la operación natural para agregar lecturas cronológicamente.
        """
        new_node = ReadingHistoryNode(historical_reading)
        if self.__tail_node is None:
            self.__head_node = new_node
            self.__tail_node = new_node
        else:
            # El nuevo nodo enlaza al tail actual como su predecesor
            new_node.prev_node = self.__tail_node
            self.__tail_node.next_node = new_node
            self.__tail_node = new_node
        self.__record_count += 1

    def remove_first(self) -> HistoricalReading:
        """
        Elimina y retorna el primer registro histórico (más antiguo).
        Lanza IndexError si el historial está vacío.
        """
        if self.__head_node is None:
            raise IndexError("El historial de lecturas está vacío.")
        removed_reading = self.__head_node.historical_reading
        self.__head_node = self.__head_node.next_node
        if self.__head_node is not None:
            # El nuevo head no tiene predecesor
            self.__head_node.prev_node = None
        else:
            # La lista quedó vacía; tail también se limpia
            self.__tail_node = None
        self.__record_count -= 1
        return removed_reading

    def remove_last(self) -> HistoricalReading:
        """
        Elimina y retorna el último registro histórico (más reciente).
        O(1) gracias al puntero tail y al enlace prev de la lista doble.
        """
        if self.__tail_node is None:
            raise IndexError("El historial de lecturas está vacío.")
        removed_reading = self.__tail_node.historical_reading
        self.__tail_node = self.__tail_node.prev_node
        if self.__tail_node is not None:
            # El nuevo tail no tiene sucesor
            self.__tail_node.next_node = None
        else:
            # La lista quedó vacía
            self.__head_node = None
        self.__record_count -= 1
        return removed_reading

    def traverse_forward(self) -> list[HistoricalReading]:
        """
        Recorre la lista de head a tail (orden cronológico ascendente).
        Retorna los registros del más antiguo al más reciente.
        """
        readings: list[HistoricalReading] = []
        current_node = self.__head_node
        while current_node is not None:
            readings.append(current_node.historical_reading)
            current_node = current_node.next_node
        return readings

    def traverse_backward(self) -> list[HistoricalReading]:
        """
        Recorre la lista de tail a head (orden cronológico descendente).
        Retorna los registros del más reciente al más antiguo.
        Solo es posible gracias al enlace prev de la lista doble.
        """
        readings: list[HistoricalReading] = []
        current_node = self.__tail_node
        while current_node is not None:
            readings.append(current_node.historical_reading)
            current_node = current_node.prev_node
        return readings

    def find(self, panel_id: str) -> Optional[HistoricalReading]:
        """
        Busca y retorna el primer registro histórico del panel especificado.
        Traversal O(n) desde el head hacia adelante.
        """
        current_node = self.__head_node
        while current_node is not None:
            if current_node.historical_reading.panel_id == panel_id:
                return current_node.historical_reading
            current_node = current_node.next_node
        return None

    def is_empty(self) -> bool:
        return self.__head_node is None

    def size(self) -> int:
        return self.__record_count

    def __repr__(self) -> str:
        return f"ReadingHistoryDoublyList(records={self.__record_count})"
