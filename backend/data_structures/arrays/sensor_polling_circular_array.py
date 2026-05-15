"""
Buffer circular para las últimas N lecturas de sensores en EcoVolt.
El array circular evita copiar datos al llenarse: simplemente sobreescribe
el valor más antiguo con el más reciente, manteniendo siempre las N
lecturas más recientes en memoria de tamaño fijo. Ideal para el análisis
de tendencias en tiempo real de voltaje, corriente o temperatura.
"""


class SensorPollingCircularArray:
    """
    Buffer circular de capacidad fija para almacenar las últimas N lecturas
    de un sensor solar. Cuando el buffer está lleno, el índice de escritura
    avanza con módulo, sobreescribiendo automáticamente la lectura más antigua.
    Esto garantiza que el buffer siempre contiene las N lecturas más recientes
    sin necesidad de desplazar o reasignar memoria.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(
                f"La capacidad del buffer circular debe ser mayor a cero, se recibió: {capacity}."
            )
        self.__capacity: int = capacity
        # Inicializa el buffer con None para distinguir slots vacíos de lecturas reales
        self.__sensor_readings: list[float | None] = [None] * capacity
        # write_index apunta siempre al próximo slot donde se escribirá
        self.__write_index: int = 0
        self.__stored_reading_count: int = 0

    def add_reading(self, sensor_value: float) -> None:
        """
        Agrega una nueva lectura al buffer.
        Si el buffer está lleno, sobreescribe la lectura más antigua
        usando el avance modular del índice de escritura.
        """
        self.__sensor_readings[self.__write_index] = sensor_value
        # El avance modular garantiza que el índice nunca excede la capacidad
        self.__write_index = (self.__write_index + 1) % self.__capacity
        # Solo incrementa el contador mientras no se haya llenado el buffer
        if self.__stored_reading_count < self.__capacity:
            self.__stored_reading_count += 1

    def get(self, reading_index: int) -> float:
        """
        Retorna la lectura en la posición indicada del buffer.
        El índice 0 corresponde a la lectura más antigua almacenada.
        Lanza IndexError si el índice está fuera del rango de lecturas actuales.
        """
        if not (0 <= reading_index < self.__stored_reading_count):
            raise IndexError(
                f"Índice {reading_index} fuera de rango. "
                f"El buffer tiene {self.__stored_reading_count} lecturas disponibles."
            )
        # Calcula la posición real en el array circular
        # Si el buffer no está lleno, la posición más antigua es 0
        # Si está lleno, la posición más antigua es write_index (ya fue sobreescrita)
        if self.__stored_reading_count < self.__capacity:
            real_position = reading_index
        else:
            real_position = (self.__write_index + reading_index) % self.__capacity

        stored_value = self.__sensor_readings[real_position]
        if stored_value is None:
            raise ValueError(f"Slot {real_position} del buffer circular está vacío.")
        return stored_value

    def is_full(self) -> bool:
        """
        Indica si el buffer ha alcanzado su capacidad máxima.
        Cuando está lleno, las nuevas lecturas sobreescriben las más antiguas.
        """
        return self.__stored_reading_count == self.__capacity

    def is_empty(self) -> bool:
        """
        Indica si no se ha registrado ninguna lectura aún.
        """
        return self.__stored_reading_count == 0

    def size(self) -> int:
        """
        Cantidad de lecturas actualmente almacenadas en el buffer.
        """
        return self.__stored_reading_count

    def get_all_readings(self) -> list[float]:
        """
        Retorna todas las lecturas almacenadas en orden cronológico
        (de la más antigua a la más reciente).
        Útil para calcular promedios móviles o detectar tendencias en sensores.
        """
        if self.__stored_reading_count == 0:
            return []

        ordered_readings: list[float] = []
        if self.__stored_reading_count < self.__capacity:
            # Buffer no lleno: las lecturas van de 0 a stored_count - 1
            for slot_idx in range(self.__stored_reading_count):
                reading = self.__sensor_readings[slot_idx]
                if reading is not None:
                    ordered_readings.append(reading)
        else:
            # Buffer lleno: la lectura más antigua está en write_index
            for offset in range(self.__capacity):
                slot_idx = (self.__write_index + offset) % self.__capacity
                reading = self.__sensor_readings[slot_idx]
                if reading is not None:
                    ordered_readings.append(reading)
        return ordered_readings

    def clear(self) -> None:
        """
        Reinicia el buffer eliminando todas las lecturas.
        Se usa al recalibrar un sensor o reiniciar el ciclo de muestreo.
        """
        self.__sensor_readings = [None] * self.__capacity
        self.__write_index = 0
        self.__stored_reading_count = 0

    @property
    def capacity(self) -> int:
        return self.__capacity

    def __repr__(self) -> str:
        return (
            f"SensorPollingCircularArray("
            f"capacity={self.__capacity}, "
            f"stored={self.__stored_reading_count}, "
            f"full={self.is_full()})"
        )
