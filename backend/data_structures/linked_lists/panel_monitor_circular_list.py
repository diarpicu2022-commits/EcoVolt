"""
Lista circular doblemente enlazada para el monitoreo round-robin de paneles
solares en EcoVolt. La estructura circular permite rotar indefinidamente
entre todos los paneles sin reiniciar el recorrido, simulando el polling
continuo que realiza el sistema de supervisión.
"""

from __future__ import annotations
from typing import Optional


class PanelMonitorNode:
    """
    Nodo de la lista circular doblemente enlazada. Almacena el identificador
    de un panel solar y mantiene referencias al nodo anterior y siguiente,
    formando un ciclo cerrado para el monitoreo continuo round-robin.
    """

    def __init__(self, panel_id: str) -> None:
        # Enlace hacia el panel anterior en el ciclo de monitoreo
        self.__prev_node: Optional[PanelMonitorNode] = None
        self.__panel_id: str = panel_id
        # Enlace hacia el próximo panel en el ciclo de monitoreo
        self.__next_node: Optional[PanelMonitorNode] = None

    @property
    def prev_node(self) -> Optional[PanelMonitorNode]:
        return self.__prev_node

    @prev_node.setter
    def prev_node(self, node: Optional[PanelMonitorNode]) -> None:
        self.__prev_node = node

    @property
    def panel_id(self) -> str:
        return self.__panel_id

    @property
    def next_node(self) -> Optional[PanelMonitorNode]:
        return self.__next_node

    @next_node.setter
    def next_node(self, node: Optional[PanelMonitorNode]) -> None:
        self.__next_node = node

    def __repr__(self) -> str:
        return f"PanelMonitorNode(panel_id={self.__panel_id!r})"


class PanelMonitorCircularList:
    """
    Lista circular doblemente enlazada para el sistema de monitoreo
    round-robin de paneles solares. Cada llamada a get_next_panel()
    avanza el cursor al siguiente panel del ciclo, garantizando que
    todos los paneles reciban atención equitativa del sistema de supervisión.

    Invariante de circularidad:
    - tail.next_node == head
    - head.prev_node == tail
    """

    def __init__(self) -> None:
        self.__head_node: Optional[PanelMonitorNode] = None
        self.__tail_node: Optional[PanelMonitorNode] = None
        # Cursor que rastrea el panel actualmente en turno de monitoreo
        self.__current_monitor_node: Optional[PanelMonitorNode] = None
        self.__panel_count: int = 0

    def insert_at_beginning(self, panel_id: str) -> None:
        """
        Inserta un panel al inicio del ciclo de monitoreo.
        El nuevo panel será el primero en ser monitoreado en la próxima ronda.
        """
        new_node = PanelMonitorNode(panel_id)
        if self.__head_node is None:
            # El único nodo se enlaza consigo mismo para mantener circularidad
            new_node.next_node = new_node
            new_node.prev_node = new_node
            self.__head_node = new_node
            self.__tail_node = new_node
            self.__current_monitor_node = new_node
        else:
            # Insertar antes del head actual manteniendo el ciclo cerrado
            new_node.next_node = self.__head_node
            new_node.prev_node = self.__tail_node
            self.__head_node.prev_node = new_node
            self.__tail_node.next_node = new_node  # type: ignore[union-attr]
            self.__head_node = new_node
        self.__panel_count += 1

    def insert_at_end(self, panel_id: str) -> None:
        """
        Inserta un panel al final del ciclo de monitoreo.
        El nuevo panel será el último en ser monitoreado antes de reiniciar.
        """
        new_node = PanelMonitorNode(panel_id)
        if self.__tail_node is None:
            # Lista vacía: el único nodo forma el ciclo consigo mismo
            new_node.next_node = new_node
            new_node.prev_node = new_node
            self.__head_node = new_node
            self.__tail_node = new_node
            self.__current_monitor_node = new_node
        else:
            # Insertar después del tail actual manteniendo el ciclo cerrado
            new_node.prev_node = self.__tail_node
            new_node.next_node = self.__head_node
            self.__tail_node.next_node = new_node
            self.__head_node.prev_node = new_node  # type: ignore[union-attr]
            self.__tail_node = new_node
        self.__panel_count += 1

    def delete(self, panel_id: str) -> bool:
        """
        Elimina el panel especificado del ciclo de monitoreo.
        Retorna True si se encontró y eliminó, False si no existe.
        Si el cursor apuntaba al panel eliminado, avanza al siguiente.
        """
        if self.__head_node is None:
            return False

        current_node = self.__head_node
        # Recorre el ciclo buscando el panel a eliminar
        for _ in range(self.__panel_count):
            if current_node.panel_id == panel_id:
                if self.__panel_count == 1:
                    # El único panel: vaciar la lista completamente
                    self.__head_node = None
                    self.__tail_node = None
                    self.__current_monitor_node = None
                else:
                    # Reconectar los vecinos para mantener la circularidad
                    prev_panel_node = current_node.prev_node
                    next_panel_node = current_node.next_node
                    prev_panel_node.next_node = next_panel_node  # type: ignore[union-attr]
                    next_panel_node.prev_node = prev_panel_node  # type: ignore[union-attr]

                    # Actualizar head o tail si el nodo eliminado era uno de ellos
                    if current_node is self.__head_node:
                        self.__head_node = next_panel_node
                    if current_node is self.__tail_node:
                        self.__tail_node = prev_panel_node

                    # Si el cursor apuntaba al nodo eliminado, moverlo al siguiente
                    if current_node is self.__current_monitor_node:
                        self.__current_monitor_node = next_panel_node

                self.__panel_count -= 1
                return True
            current_node = current_node.next_node  # type: ignore[assignment]

        return False

    def get_next_panel(self) -> str:
        """
        Avanza el cursor al siguiente panel en el ciclo y retorna su ID.
        Esta operación implementa el polling round-robin: cada llamada
        devuelve un panel distinto, rotando indefinidamente por la lista.
        """
        if self.__current_monitor_node is None:
            raise IndexError("No hay paneles registrados para monitorear.")
        panel_id = self.__current_monitor_node.panel_id
        # Avanza el cursor al siguiente panel del ciclo
        self.__current_monitor_node = self.__current_monitor_node.next_node
        return panel_id

    def print_list(self) -> list[str]:
        """
        Retorna todos los panel_ids en orden de monitoreo (desde head).
        Útil para inspeccionar el estado actual del ciclo de supervisión.
        """
        panel_ids: list[str] = []
        if self.__head_node is None:
            return panel_ids

        current_node = self.__head_node
        # Recorre exactamente panel_count nodos para no entrar en loop infinito
        for _ in range(self.__panel_count):
            panel_ids.append(current_node.panel_id)
            current_node = current_node.next_node  # type: ignore[assignment]
        return panel_ids

    def is_empty(self) -> bool:
        return self.__head_node is None

    def size(self) -> int:
        return self.__panel_count

    def __repr__(self) -> str:
        return f"PanelMonitorCircularList(panels={self.__panel_count})"
