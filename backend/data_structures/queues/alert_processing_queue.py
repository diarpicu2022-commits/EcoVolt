"""
Cola FIFO para procesar alertas pendientes del sistema solar EcoVolt.
Las alertas se encolan en orden de llegada y se procesan por prioridad
temporal: la primera en llegar es la primera en atenderse.
"""

from collections import deque
from typing import TypeVar, Generic, Optional

# A representa cualquier tipo de alerta del sistema solar
A = TypeVar("A")


class AlertProcessingQueue(Generic[A]):
    """
    Cola genérica FIFO para gestionar alertas pendientes del sistema EcoVolt.
    Utiliza collections.deque internamente para garantizar O(1) en enqueue
    y dequeue, ya que las alertas deben procesarse sin demora.
    """

    def __init__(self) -> None:
        # deque permite agregar al final y quitar del frente en O(1)
        self.__pending_alerts: deque[A] = deque()

    def enqueue(self, alert_message: A) -> None:
        """
        Agrega una alerta al final de la cola.
        Las alertas más nuevas esperan detrás de las ya registradas.
        """
        self.__pending_alerts.append(alert_message)

    def dequeue(self) -> A:
        """
        Elimina y retorna la alerta más antigua (frente de la cola).
        Lanza IndexError si no hay alertas pendientes.
        """
        if self.is_empty():
            raise IndexError("No hay alertas pendientes en la cola de procesamiento.")
        # popleft() extrae desde el frente en O(1)
        return self.__pending_alerts.popleft()

    def front(self) -> A:
        """
        Retorna la alerta al frente sin eliminarla.
        Permite inspeccionar la próxima alerta a procesar sin consumirla.
        """
        if self.is_empty():
            raise IndexError("La cola de alertas está vacía; no hay frente disponible.")
        return self.__pending_alerts[0]

    def rear(self) -> A:
        """
        Retorna la alerta más reciente (al final de la cola) sin eliminarla.
        Útil para verificar la última alerta registrada.
        """
        if self.is_empty():
            raise IndexError("La cola de alertas está vacía; no hay elemento trasero.")
        return self.__pending_alerts[-1]

    def is_empty(self) -> bool:
        """
        Indica si no hay alertas pendientes de procesar.
        """
        return len(self.__pending_alerts) == 0

    def size(self) -> int:
        """
        Cantidad de alertas pendientes en la cola.
        """
        return len(self.__pending_alerts)

    def clear(self) -> None:
        """
        Descarta todas las alertas pendientes.
        Se usa al reiniciar el subsistema de alertas del sistema solar.
        """
        self.__pending_alerts.clear()

    def __repr__(self) -> str:
        return f"AlertProcessingQueue(pending={self.size()})"
