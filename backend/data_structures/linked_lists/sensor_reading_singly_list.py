"""
Lista simplemente enlazada de lecturas de sensores del sistema solar EcoVolt.
Solo permite traversal hacia adelante (forward), lo que es suficiente para
procesar flujos de datos de sensores en tiempo real donde no se necesita
retroceder en el historial.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SensorReading:
    """
    Encapsula una medición completa tomada por los sensores físicos
    instalados en un panel solar en un instante de tiempo determinado.
    """

    def __init__(
        self,
        panel_id: str,
        voltage: float,
        current: float,
        power: float,
        temperature: float,
        reading_timestamp: datetime | None = None,
    ) -> None:
        self.__panel_id = panel_id
        self.__voltage = voltage           # Voltios (V)
        self.__current = current           # Amperios (A)
        self.__power = power               # Vatios (W)
        self.__temperature = temperature   # Grados Celsius (°C)
        # Registra el momento exacto de la medición para auditoría
        self.__reading_timestamp = reading_timestamp if reading_timestamp else datetime.now()

    @property
    def panel_id(self) -> str:
        return self.__panel_id

    @property
    def voltage(self) -> float:
        return self.__voltage

    @property
    def current(self) -> float:
        return self.__current

    @property
    def power(self) -> float:
        return self.__power

    @property
    def temperature(self) -> float:
        return self.__temperature

    @property
    def reading_timestamp(self) -> datetime:
        return self.__reading_timestamp

    def __repr__(self) -> str:
        return (
            f"SensorReading(panel_id={self.__panel_id!r}, "
            f"voltage={self.__voltage}V, current={self.__current}A, "
            f"power={self.__power}W, temp={self.__temperature}°C)"
        )


class SensorReadingNode:
    """
    Nodo de la lista simplemente enlazada que contiene una lectura de sensor
    y un puntero al siguiente nodo. El puntero 'next' solo apunta hacia adelante.
    """

    def __init__(self, sensor_reading: SensorReading) -> None:
        self.__sensor_reading: SensorReading = sensor_reading
        # Solo existe enlace hacia adelante; retroceder no está soportado
        self.__next_node: Optional[SensorReadingNode] = None

    @property
    def sensor_reading(self) -> SensorReading:
        return self.__sensor_reading

    @property
    def next_node(self) -> Optional[SensorReadingNode]:
        return self.__next_node

    @next_node.setter
    def next_node(self, node: Optional[SensorReadingNode]) -> None:
        self.__next_node = node

    def __repr__(self) -> str:
        return f"SensorReadingNode(data={self.__sensor_reading})"


class SensorReadingSinglyList:
    """
    Lista simplemente enlazada para almacenar lecturas de sensores solares.
    Permite inserción eficiente al inicio (O(1)) y recorrido secuencial
    para analizar el flujo continuo de datos de paneles fotovoltaicos.
    """

    def __init__(self) -> None:
        self.__head_node: Optional[SensorReadingNode] = None
        self.__tail_node: Optional[SensorReadingNode] = None
        self.__reading_count: int = 0

    def add_first(self, sensor_reading: SensorReading) -> None:
        """
        Inserta una lectura al inicio de la lista en O(1).
        Se usa cuando la lectura más reciente debe procesarse primero.
        """
        new_node = SensorReadingNode(sensor_reading)
        if self.__head_node is None:
            # Lista vacía: head y tail apuntan al único nodo
            self.__head_node = new_node
            self.__tail_node = new_node
        else:
            # El nuevo nodo apunta al antiguo head antes de reemplazarlo
            new_node.next_node = self.__head_node
            self.__head_node = new_node
        self.__reading_count += 1

    def add_last(self, sensor_reading: SensorReading) -> None:
        """
        Inserta una lectura al final de la lista en O(1) gracias al puntero tail.
        Es la operación natural para encolar lecturas cronológicamente.
        """
        new_node = SensorReadingNode(sensor_reading)
        if self.__tail_node is None:
            # Lista vacía: ambos extremos apuntan al nuevo nodo
            self.__head_node = new_node
            self.__tail_node = new_node
        else:
            # El tail actual enlaza hacia el nuevo nodo antes de actualizarse
            self.__tail_node.next_node = new_node
            self.__tail_node = new_node
        self.__reading_count += 1

    def remove_first(self) -> SensorReading:
        """
        Elimina y retorna la lectura al inicio de la lista.
        Lanza IndexError si la lista está vacía.
        """
        if self.__head_node is None:
            raise IndexError("La lista de lecturas de sensor está vacía.")
        removed_reading = self.__head_node.sensor_reading
        self.__head_node = self.__head_node.next_node
        # Si la lista quedó vacía, tail también debe limpiarse
        if self.__head_node is None:
            self.__tail_node = None
        self.__reading_count -= 1
        return removed_reading

    def remove_last(self) -> SensorReading:
        """
        Elimina y retorna la lectura al final de la lista.
        Requiere traversal O(n) porque es lista simplemente enlazada.
        """
        if self.__head_node is None:
            raise IndexError("La lista de lecturas de sensor está vacía.")

        # Caso especial: solo hay un nodo
        if self.__head_node is self.__tail_node:
            removed_reading = self.__head_node.sensor_reading
            self.__head_node = None
            self.__tail_node = None
            self.__reading_count -= 1
            return removed_reading

        # Recorre hasta el penúltimo nodo para actualizar tail
        current_node = self.__head_node
        while current_node.next_node is not self.__tail_node:
            current_node = current_node.next_node  # type: ignore[assignment]

        removed_reading = self.__tail_node.sensor_reading  # type: ignore[union-attr]
        current_node.next_node = None
        self.__tail_node = current_node
        self.__reading_count -= 1
        return removed_reading

    def find(self, panel_id: str) -> Optional[SensorReading]:
        """
        Busca y retorna la primera lectura correspondiente al panel indicado.
        Traversal O(n) necesario porque la lista no está indexada.
        """
        current_node = self.__head_node
        while current_node is not None:
            if current_node.sensor_reading.panel_id == panel_id:
                return current_node.sensor_reading
            current_node = current_node.next_node
        # Retorna None si ningún nodo pertenece al panel buscado
        return None

    def traverse(self) -> list[SensorReading]:
        """
        Recorre toda la lista y retorna todas las lecturas como lista Python.
        Útil para exportar datos o calcular estadísticas sobre todos los paneles.
        """
        sensor_readings: list[SensorReading] = []
        current_node = self.__head_node
        while current_node is not None:
            sensor_readings.append(current_node.sensor_reading)
            current_node = current_node.next_node
        return sensor_readings

    def is_empty(self) -> bool:
        return self.__head_node is None

    def size(self) -> int:
        return self.__reading_count

    def __repr__(self) -> str:
        return f"SensorReadingSinglyList(readings={self.__reading_count})"
