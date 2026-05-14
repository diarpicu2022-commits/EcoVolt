"""
Array de referencias a objetos panel en EcoVolt.
Simula el concepto de array de punteros de lenguajes como C/C++:
almacena las referencias (identidades en memoria) de los objetos panel,
no copias de ellos. Esto permite que múltiples componentes del sistema
operen sobre el mismo objeto panel sin duplicar datos.
"""

from typing import Any, Optional


class PanelReferenceArray:
    """
    Array dinámico que almacena referencias (no copias) a objetos de panel solar.
    La operación contains() usa comparación de identidad (is) en lugar de
    igualdad (==) para verificar si exactamente el mismo objeto está almacenado,
    reflejando la semántica de punteros donde importa la dirección, no el valor.
    """

    def __init__(self) -> None:
        # Almacena referencias a objetos; Any permite cualquier tipo de panel
        self.__panel_references: list[Any] = []

    def get(self, reference_index: int) -> Any:
        """
        Retorna la referencia al objeto panel en la posición indicada.
        El objeto retornado es el mismo en memoria (no una copia).
        """
        self.__validate_index(reference_index)
        return self.__panel_references[reference_index]

    def set(self, reference_index: int, panel_object: Any) -> None:
        """
        Reemplaza la referencia en la posición indicada con un nuevo objeto panel.
        El objeto anterior sigue existiendo si hay otras referencias a él.
        """
        self.__validate_index(reference_index)
        self.__panel_references[reference_index] = panel_object

    def insert_at(self, reference_index: int, panel_object: Any) -> None:
        """
        Inserta una referencia a un panel en la posición indicada.
        Desplaza las referencias siguientes una posición a la derecha.
        """
        if not (0 <= reference_index <= len(self.__panel_references)):
            raise IndexError(f"Índice {reference_index} fuera de rango para inserción.")
        self.__panel_references.insert(reference_index, panel_object)

    def append(self, panel_object: Any) -> None:
        """
        Agrega una referencia al objeto panel al final del array.
        El objeto no se copia; solo se almacena su referencia en memoria.
        """
        self.__panel_references.append(panel_object)

    def delete_at(self, reference_index: int) -> Any:
        """
        Elimina y retorna la referencia en la posición indicada.
        El objeto panel sigue existiendo si hay otras referencias a él en el sistema.
        """
        self.__validate_index(reference_index)
        return self.__panel_references.pop(reference_index)

    def delete_value(self, panel_object: Any) -> bool:
        """
        Busca y elimina la primera referencia al objeto panel exacto especificado.
        Usa comparación de identidad (is) para encontrar el mismo objeto en memoria.
        Retorna True si se encontró y eliminó la referencia.
        """
        for ref_idx, stored_panel_ref in enumerate(self.__panel_references):
            # Comparación de identidad: verifica que sea el mismo objeto en memoria
            if stored_panel_ref is panel_object:
                self.__panel_references.pop(ref_idx)
                return True
        return False

    def find_index(self, panel_object: Any) -> int:
        """
        Retorna el índice de la primera referencia al objeto panel exacto.
        Usa identidad (is), no igualdad (==), para encontrar el puntero exacto.
        Retorna -1 si no se encuentra ninguna referencia al objeto.
        """
        for ref_idx, stored_panel_ref in enumerate(self.__panel_references):
            if stored_panel_ref is panel_object:
                return ref_idx
        return -1

    def contains(self, panel_object: Any) -> bool:
        """
        Verifica si el array contiene una referencia al objeto panel especificado.
        Usa comparación de identidad (is) para verificar si es el mismo objeto
        en memoria, no uno con los mismos valores (==).
        """
        return self.find_index(panel_object) != -1

    def __validate_index(self, reference_index: int) -> None:
        if not (0 <= reference_index < len(self.__panel_references)):
            raise IndexError(
                f"Índice {reference_index} fuera de rango. "
                f"El array contiene {len(self.__panel_references)} referencias."
            )

    def size(self) -> int:
        return len(self.__panel_references)

    def is_empty(self) -> bool:
        return len(self.__panel_references) == 0

    def get_all_references(self) -> list[Any]:
        """
        Retorna una lista con todas las referencias almacenadas.
        La lista es nueva, pero los objetos son los mismos en memoria.
        """
        return list(self.__panel_references)

    def __repr__(self) -> str:
        return f"PanelReferenceArray(references={len(self.__panel_references)})"
