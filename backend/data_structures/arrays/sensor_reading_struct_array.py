"""
Array de estructuras (registros) de lecturas de sensor para EcoVolt.
Almacena objetos completos SensorReadingRecord en lugar de primitivos,
permitiendo operaciones de búsqueda y ordenamiento multi-campo sobre
el conjunto completo de mediciones de los paneles solares.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SensorReadingRecord:
    """
    Registro completo de una medición de sensor de panel solar.
    Usa dataclass para reducir boilerplate manteniendo la semántica
    de estructura de datos del dominio energético.
    Todos los campos usan nombres de dominio solar para claridad.
    """

    __panel_id: str
    __voltage: float       # Voltios (V)
    __current: float       # Amperios (A)
    __power: float         # Vatios (W) = voltage × current
    __temperature: float   # Grados Celsius (°C) del panel
    __reading_timestamp: datetime

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
        self.__voltage = voltage
        self.__current = current
        self.__power = power
        self.__temperature = temperature
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
            f"SensorReadingRecord(panel_id={self.__panel_id!r}, "
            f"power={self.__power}W, "
            f"timestamp={self.__reading_timestamp.isoformat()})"
        )


class SensorReadingStructArray:
    """
    Array dinámico de objetos SensorReadingRecord del sistema EcoVolt.
    Soporta ordenamiento por timestamp (ascendente) para análisis cronológico
    y por potencia descendente para identificar los paneles más productivos.
    """

    def __init__(self) -> None:
        self.__reading_records: list[SensorReadingRecord] = []

    def get(self, record_index: int) -> SensorReadingRecord:
        """
        Retorna el registro en la posición indicada.
        Lanza IndexError si el índice está fuera del rango actual.
        """
        self.__validate_index(record_index)
        return self.__reading_records[record_index]

    def set(self, record_index: int, reading_record: SensorReadingRecord) -> None:
        """
        Reemplaza el registro en la posición indicada.
        """
        self.__validate_index(record_index)
        self.__reading_records[record_index] = reading_record

    def insert_at(self, record_index: int, reading_record: SensorReadingRecord) -> None:
        """
        Inserta un registro en la posición indicada, desplazando los siguientes.
        Acepta índice igual al tamaño para inserción al final.
        """
        if not (0 <= record_index <= len(self.__reading_records)):
            raise IndexError(f"Índice {record_index} fuera de rango para inserción.")
        self.__reading_records.insert(record_index, reading_record)

    def append(self, reading_record: SensorReadingRecord) -> None:
        """
        Agrega un registro al final del array en O(1) amortizado.
        """
        self.__reading_records.append(reading_record)

    def delete_at(self, record_index: int) -> SensorReadingRecord:
        """
        Elimina y retorna el registro en la posición indicada.
        """
        self.__validate_index(record_index)
        return self.__reading_records.pop(record_index)

    def delete_value(self, panel_id: str) -> bool:
        """
        Busca y elimina el primer registro correspondiente al panel indicado.
        Retorna True si se encontró y eliminó.
        """
        record_index = self.find_index(panel_id)
        if record_index == -1:
            return False
        self.__reading_records.pop(record_index)
        return True

    def find_index(self, panel_id: str) -> int:
        """
        Retorna el índice del primer registro del panel especificado.
        Retorna -1 si no existe ningún registro de ese panel.
        """
        for idx, record in enumerate(self.__reading_records):
            if record.panel_id == panel_id:
                return idx
        return -1

    def contains(self, panel_id: str) -> bool:
        return self.find_index(panel_id) != -1

    def sort_ascending(self) -> None:
        """
        Ordena los registros por timestamp ascendente (más antiguo primero).
        Permite reconstruir la secuencia cronológica de lecturas del sistema.
        """
        self.__reading_records.sort(key=lambda record: record.reading_timestamp)

    def sort_descending(self) -> None:
        """
        Ordena los registros por potencia descendente (mayor potencia primero).
        Permite identificar rápidamente los paneles con mayor generación.
        """
        self.__reading_records.sort(key=lambda record: record.power, reverse=True)

    def __validate_index(self, record_index: int) -> None:
        if not (0 <= record_index < len(self.__reading_records)):
            raise IndexError(
                f"Índice {record_index} fuera de rango. "
                f"El array contiene {len(self.__reading_records)} registros."
            )

    def size(self) -> int:
        return len(self.__reading_records)

    def is_empty(self) -> bool:
        return len(self.__reading_records) == 0

    def get_all(self) -> list[SensorReadingRecord]:
        return list(self.__reading_records)

    def __repr__(self) -> str:
        return f"SensorReadingStructArray(records={len(self.__reading_records)})"
