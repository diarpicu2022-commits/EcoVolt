"""
Array estático de capacidad fija para los slots de paneles solares en EcoVolt.
La capacidad máxima de 20 refleja la restricción física de la instalación:
el inversor soporta hasta 20 strings de paneles simultáneamente.
"""

from typing import Optional


MAX_PANEL_SLOTS: int = 20


class SolarPanelStaticArray:
    """
    Array estático de 20 slots para identificadores de paneles solares.
    La capacidad fija simula la restricción hardware del inversor, que no
    puede gestionar más de MAX_PANEL_SLOTS paneles en paralelo.
    Los slots vacíos se representan con None.
    """

    def __init__(self) -> None:
        # Pre-asigna exactamente 20 posiciones; None indica slot sin panel
        self.__panel_slots: list[Optional[str]] = [None] * MAX_PANEL_SLOTS
        # Rastrea cuántos slots están ocupados para validar capacidad
        self.__occupied_slots: int = 0

    def get(self, slot_index: int) -> Optional[str]:
        """
        Retorna el panel_id en el slot indicado, o None si está vacío.
        Lanza IndexError si el índice está fuera del rango 0-19.
        """
        self.__validate_index(slot_index)
        return self.__panel_slots[slot_index]

    def set(self, slot_index: int, panel_id: str) -> None:
        """
        Asigna un panel_id a un slot específico.
        Si el slot estaba vacío, incrementa el contador de ocupados.
        Lanza IndexError si el índice está fuera del rango 0-19.
        """
        self.__validate_index(slot_index)
        if self.__panel_slots[slot_index] is None:
            self.__occupied_slots += 1
        self.__panel_slots[slot_index] = panel_id

    def insert_at(self, slot_index: int, panel_id: str) -> None:
        """
        Inserta un panel en el slot indicado desplazando los paneles
        posteriores una posición a la derecha.
        Lanza IndexError si el array ya está lleno o el índice es inválido.
        """
        self.__validate_index(slot_index)
        if self.__occupied_slots >= MAX_PANEL_SLOTS:
            raise OverflowError(f"El array de paneles ya está lleno ({MAX_PANEL_SLOTS} slots ocupados).")
        # Desplaza hacia la derecha desde el último elemento hasta slot_index
        for shift_index in range(MAX_PANEL_SLOTS - 1, slot_index, -1):
            self.__panel_slots[shift_index] = self.__panel_slots[shift_index - 1]
        self.__panel_slots[slot_index] = panel_id
        self.__occupied_slots += 1

    def insertAt(self, slot_index: int, panel_id: str) -> None:
        # Mantiene compatibilidad con el contrato camelCase del brief.
        self.insert_at(slot_index, panel_id)

    def append(self, panel_id: str) -> None:
        """
        Agrega un panel en el primer slot vacío disponible.
        Lanza OverflowError si todos los slots están ocupados.
        """
        if self.__occupied_slots >= MAX_PANEL_SLOTS:
            raise OverflowError(f"El array de paneles está lleno; no se puede agregar '{panel_id}'.")
        for slot_index in range(MAX_PANEL_SLOTS):
            if self.__panel_slots[slot_index] is None:
                self.__panel_slots[slot_index] = panel_id
                self.__occupied_slots += 1
                return

    def delete_at(self, slot_index: int) -> Optional[str]:
        """
        Elimina el panel en el slot indicado y desplaza los siguientes
        una posición a la izquierda para mantener la continuidad.
        Retorna el panel_id eliminado, o None si el slot ya estaba vacío.
        """
        self.__validate_index(slot_index)
        removed_panel_id = self.__panel_slots[slot_index]
        if removed_panel_id is not None:
            # Desplaza hacia la izquierda para llenar el hueco
            for shift_index in range(slot_index, MAX_PANEL_SLOTS - 1):
                self.__panel_slots[shift_index] = self.__panel_slots[shift_index + 1]
            self.__panel_slots[MAX_PANEL_SLOTS - 1] = None
            self.__occupied_slots -= 1
        return removed_panel_id

    def deleteAt(self, slot_index: int) -> Optional[str]:
        return self.delete_at(slot_index)

    def delete_value(self, panel_id: str) -> bool:
        """
        Busca y elimina la primera ocurrencia del panel_id especificado.
        Retorna True si se encontró y eliminó, False si no existía.
        """
        slot_index = self.find_index(panel_id)
        if slot_index == -1:
            return False
        self.delete_at(slot_index)
        return True

    def deleteValue(self, panel_id: str) -> bool:
        return self.delete_value(panel_id)

    def find_index(self, panel_id: str) -> int:
        """
        Retorna el índice del primer slot que contiene el panel_id buscado.
        Retorna -1 si el panel no está registrado en ningún slot.
        """
        for slot_index in range(MAX_PANEL_SLOTS):
            if self.__panel_slots[slot_index] == panel_id:
                return slot_index
        return -1

    def findIndex(self, panel_id: str) -> int:
        return self.find_index(panel_id)

    def contains(self, panel_id: str) -> bool:
        """
        Indica si el panel_id está registrado en algún slot del array.
        """
        return self.find_index(panel_id) != -1

    def sort_ascending(self) -> None:
        """
        Ordena los paneles alfabéticamente de menor a mayor.
        Los slots None se mueven al final para mantener las IDs juntas.
        Usa el sort nativo de Python (Timsort O(n log n)).
        """
        # Separa paneles reales de slots vacíos para ordenar solo los reales
        active_panel_ids = [pid for pid in self.__panel_slots if pid is not None]
        active_panel_ids.sort()
        # Reconstruye el array con los paneles ordenados seguidos de None
        for slot_index in range(MAX_PANEL_SLOTS):
            if slot_index < len(active_panel_ids):
                self.__panel_slots[slot_index] = active_panel_ids[slot_index]
            else:
                self.__panel_slots[slot_index] = None

    def sortAscending(self) -> None:
        self.sort_ascending()

    def sort_descending(self) -> None:
        """
        Ordena los paneles alfabéticamente de mayor a menor.
        Los slots None se mueven al final igual que en sort_ascending.
        """
        active_panel_ids = [pid for pid in self.__panel_slots if pid is not None]
        active_panel_ids.sort(reverse=True)
        for slot_index in range(MAX_PANEL_SLOTS):
            if slot_index < len(active_panel_ids):
                self.__panel_slots[slot_index] = active_panel_ids[slot_index]
            else:
                self.__panel_slots[slot_index] = None

    def sortDescending(self) -> None:
        self.sort_descending()

    def __validate_index(self, slot_index: int) -> None:
        """
        Valida que el índice esté dentro del rango permitido del array estático.
        Lanza IndexError descriptivo para facilitar depuración.
        """
        if not (0 <= slot_index < MAX_PANEL_SLOTS):
            raise IndexError(
                f"Índice de slot {slot_index} fuera de rango. "
                f"El array estático tiene {MAX_PANEL_SLOTS} slots (0-{MAX_PANEL_SLOTS - 1})."
            )

    def get_all_slots(self) -> list[Optional[str]]:
        """
        Retorna una copia del array completo incluyendo slots None.
        """
        return list(self.__panel_slots)

    def occupied_count(self) -> int:
        return self.__occupied_slots

    def capacity(self) -> int:
        return MAX_PANEL_SLOTS

    def is_full(self) -> bool:
        return self.__occupied_slots >= MAX_PANEL_SLOTS

    def __repr__(self) -> str:
        return (
            f"SolarPanelStaticArray(capacity={MAX_PANEL_SLOTS}, "
            f"occupied={self.__occupied_slots})"
        )
