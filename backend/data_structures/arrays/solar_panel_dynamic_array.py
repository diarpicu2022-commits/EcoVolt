"""
Array dinámico de paneles solares con algoritmos de ordenamiento implementados
desde cero para el sistema EcoVolt. A diferencia del array estático, este
crece según la demanda, permitiendo instalar más paneles sin límite previo.
Los algoritmos QuickSort, MergeSort y HeapSort se implementan para fines
educativos y de evaluación de rendimiento en distintos escenarios de uso.
"""

from typing import Optional


class SolarPanelDynamicArray:
    """
    Array dinámico de identificadores de paneles solares.
    Implementa QuickSort para ordenamiento ascendente (óptimo en promedio),
    MergeSort invertido para descendente (garantía O(n log n) en peor caso),
    y HeapSort como alternativa in-place eficiente en memoria.
    """

    def __init__(self) -> None:
        # La lista Python gestiona el crecimiento dinámico automáticamente
        self.__panel_ids: list[str] = []

    # ------------------------------------------------------------------ #
    #  Operaciones CRUD                                                    #
    # ------------------------------------------------------------------ #

    def get(self, panel_index: int) -> str:
        """
        Retorna el panel_id en la posición indicada.
        Lanza IndexError si el índice está fuera del rango actual.
        """
        self.__validate_index(panel_index)
        return self.__panel_ids[panel_index]

    def set(self, panel_index: int, panel_id: str) -> None:
        """
        Reemplaza el panel_id en la posición indicada.
        """
        self.__validate_index(panel_index)
        self.__panel_ids[panel_index] = panel_id

    def insert_at(self, panel_index: int, panel_id: str) -> None:
        """
        Inserta un panel en la posición indicada, desplazando los siguientes.
        Acepta índice igual al tamaño actual para insertar al final.
        """
        if not (0 <= panel_index <= len(self.__panel_ids)):
            raise IndexError(f"Índice {panel_index} fuera de rango para inserción.")
        self.__panel_ids.insert(panel_index, panel_id)

    def append(self, panel_id: str) -> None:
        """
        Agrega un panel al final del array en O(1) amortizado.
        """
        self.__panel_ids.append(panel_id)

    def delete_at(self, panel_index: int) -> str:
        """
        Elimina y retorna el panel en la posición indicada.
        """
        self.__validate_index(panel_index)
        return self.__panel_ids.pop(panel_index)

    def delete_value(self, panel_id: str) -> bool:
        """
        Busca y elimina la primera ocurrencia del panel_id especificado.
        Retorna True si se encontró y eliminó.
        """
        panel_index = self.find_index(panel_id)
        if panel_index == -1:
            return False
        self.__panel_ids.pop(panel_index)
        return True

    def find_index(self, panel_id: str) -> int:
        """
        Retorna el índice de la primera ocurrencia del panel_id.
        Retorna -1 si no se encuentra.
        """
        for idx, stored_panel_id in enumerate(self.__panel_ids):
            if stored_panel_id == panel_id:
                return idx
        return -1

    def contains(self, panel_id: str) -> bool:
        return self.find_index(panel_id) != -1

    # ------------------------------------------------------------------ #
    #  Algoritmos de ordenamiento privados                                 #
    # ------------------------------------------------------------------ #

    def __quicksort(self, panel_arr: list[str], low: int, high: int) -> None:
        """
        QuickSort in-place recursivo.
        Elige el último elemento como pivot para simplicidad de implementación.
        Caso promedio O(n log n); peor caso O(n²) con datos ya ordenados.
        Se usa para sort_ascending porque en datos de paneles solares (IDs
        distribuidas aleatoriamente) el caso promedio domina.
        """
        if low < high:
            pivot_position = self.__partition(panel_arr, low, high)
            # Ordena recursivamente los sub-arrays izquierdo y derecho
            self.__quicksort(panel_arr, low, pivot_position - 1)
            self.__quicksort(panel_arr, pivot_position + 1, high)

    def __partition(self, panel_arr: list[str], low: int, high: int) -> int:
        """
        Particiona el sub-array en torno al pivot (último elemento).
        Mueve elementos menores al pivot a su izquierda y mayores a su derecha.
        """
        pivot_panel_id = panel_arr[high]
        # i apunta al último elemento menor que el pivot encontrado
        smaller_than_pivot_idx = low - 1
        for scan_idx in range(low, high):
            if panel_arr[scan_idx] <= pivot_panel_id:
                smaller_than_pivot_idx += 1
                panel_arr[smaller_than_pivot_idx], panel_arr[scan_idx] = (
                    panel_arr[scan_idx],
                    panel_arr[smaller_than_pivot_idx],
                )
        # Coloca el pivot en su posición definitiva
        panel_arr[smaller_than_pivot_idx + 1], panel_arr[high] = (
            panel_arr[high],
            panel_arr[smaller_than_pivot_idx + 1],
        )
        return smaller_than_pivot_idx + 1

    def __mergesort(self, panel_arr: list[str]) -> list[str]:
        """
        MergeSort que retorna una nueva lista ordenada ascendentemente.
        Garantía O(n log n) en todos los casos; usa memoria O(n) adicional.
        Se invierte el resultado para obtener orden descendente en sort_descending.
        """
        if len(panel_arr) <= 1:
            return panel_arr

        # Divide el array en dos mitades iguales
        mid_idx = len(panel_arr) // 2
        left_half = self.__mergesort(panel_arr[:mid_idx])
        right_half = self.__mergesort(panel_arr[mid_idx:])

        return self.__merge_sorted_halves(left_half, right_half)

    def __merge_sorted_halves(
        self, left_panels: list[str], right_panels: list[str]
    ) -> list[str]:
        """
        Combina dos listas ya ordenadas en una sola lista ordenada.
        Compara elemento a elemento eligiendo el menor de cada mitad.
        """
        merged_panels: list[str] = []
        left_cursor = 0
        right_cursor = 0

        while left_cursor < len(left_panels) and right_cursor < len(right_panels):
            if left_panels[left_cursor] <= right_panels[right_cursor]:
                merged_panels.append(left_panels[left_cursor])
                left_cursor += 1
            else:
                merged_panels.append(right_panels[right_cursor])
                right_cursor += 1

        # Agrega los elementos restantes de la mitad que no se agotó
        merged_panels.extend(left_panels[left_cursor:])
        merged_panels.extend(right_panels[right_cursor:])
        return merged_panels

    def __heapsort(self, panel_arr: list[str]) -> None:
        """
        HeapSort in-place que ordena panel_arr ascendentemente.
        O(n log n) garantizado y O(1) memoria adicional.
        Útil cuando la memoria es limitada en el controlador del sistema solar.
        """
        arr_length = len(panel_arr)

        # Fase 1: Construye el max-heap desde abajo hacia arriba
        # Solo los nodos internos (no hojas) necesitan heapificarse
        for root_idx in range(arr_length // 2 - 1, -1, -1):
            self.__heapify(panel_arr, arr_length, root_idx)

        # Fase 2: Extrae el máximo repetidamente, colocándolo al final
        for sorted_boundary in range(arr_length - 1, 0, -1):
            # El máximo (raíz del heap) va al final del segmento no ordenado
            panel_arr[0], panel_arr[sorted_boundary] = (
                panel_arr[sorted_boundary],
                panel_arr[0],
            )
            # Restaura la propiedad heap en el sub-array reducido
            self.__heapify(panel_arr, sorted_boundary, 0)

    def __heapify(self, panel_arr: list[str], heap_size: int, root_idx: int) -> None:
        """
        Mantiene la propiedad de max-heap en el sub-árbol con raíz en root_idx.
        El nodo más grande entre raíz, hijo izquierdo y derecho sube a la raíz.
        """
        largest_idx = root_idx
        left_child_idx = 2 * root_idx + 1
        right_child_idx = 2 * root_idx + 2

        # Compara con hijo izquierdo si existe dentro del heap
        if left_child_idx < heap_size and panel_arr[left_child_idx] > panel_arr[largest_idx]:
            largest_idx = left_child_idx

        # Compara con hijo derecho si existe dentro del heap
        if right_child_idx < heap_size and panel_arr[right_child_idx] > panel_arr[largest_idx]:
            largest_idx = right_child_idx

        # Si la raíz no es el mayor, intercambia y propaga hacia abajo
        if largest_idx != root_idx:
            panel_arr[root_idx], panel_arr[largest_idx] = (
                panel_arr[largest_idx],
                panel_arr[root_idx],
            )
            self.__heapify(panel_arr, heap_size, largest_idx)

    # ------------------------------------------------------------------ #
    #  Métodos públicos de ordenamiento                                    #
    # ------------------------------------------------------------------ #

    def sort_ascending(self) -> None:
        """
        Ordena los paneles alfabéticamente ascendente usando QuickSort.
        QuickSort es preferido por su rendimiento promedio superior
        con datos de IDs de paneles distribuidos aleatoriamente.
        """
        if len(self.__panel_ids) > 1:
            self.__quicksort(self.__panel_ids, 0, len(self.__panel_ids) - 1)

    def sort_descending(self) -> None:
        """
        Ordena los paneles alfabéticamente descendente usando MergeSort invertido.
        MergeSort garantiza O(n log n) en el peor caso, importante cuando
        se reportan rankings de producción donde el orden es crítico.
        """
        if len(self.__panel_ids) > 1:
            sorted_panel_ids = self.__mergesort(list(self.__panel_ids))
            # Invertir el resultado ascendente de MergeSort para obtener descendente
            self.__panel_ids = sorted_panel_ids[::-1]

    def sort_with_heapsort(self) -> None:
        """
        Ordena los paneles ascendente usando HeapSort.
        Opción preferible cuando la memoria adicional disponible es mínima
        en el microcontrolador del sistema de monitoreo solar.
        """
        if len(self.__panel_ids) > 1:
            self.__heapsort(self.__panel_ids)

    def __validate_index(self, panel_index: int) -> None:
        if not (0 <= panel_index < len(self.__panel_ids)):
            raise IndexError(
                f"Índice {panel_index} fuera de rango. "
                f"El array dinámico contiene {len(self.__panel_ids)} paneles."
            )

    def size(self) -> int:
        return len(self.__panel_ids)

    def is_empty(self) -> bool:
        return len(self.__panel_ids) == 0

    def get_all(self) -> list[str]:
        return list(self.__panel_ids)

    def __repr__(self) -> str:
        return f"SolarPanelDynamicArray(size={len(self.__panel_ids)})"
