"""
Pila LIFO para deshacer y rehacer configuraciones del sistema solar EcoVolt.
Implementa el patrón Command con capacidad de undo/redo sobre ajustes
de paneles, inversores y umbrales de alerta.
"""

from typing import TypeVar, Generic, Optional

# T representa cualquier tipo de comando de configuración solar
T = TypeVar("T")


class ConfigurationCommandStack(Generic[T]):
    """
    Pila genérica LIFO para gestionar el historial de comandos de configuración
    del sistema solar. Permite revertir o rehacer cambios en parámetros
    como voltaje nominal, umbral de alerta y modo de operación del inversor.
    """

    def __init__(self) -> None:
        # Lista interna que actúa como pila; el último elemento es el tope
        self.__command_history: list[T] = []

    def push(self, configuration_command: T) -> None:
        """
        Agrega un comando de configuración al tope de la pila.
        Se usa al aplicar un nuevo ajuste para poder revertirlo después.
        """
        self.__command_history.append(configuration_command)

    def pop(self) -> T:
        """
        Elimina y retorna el comando en el tope de la pila (undo).
        Lanza IndexError si la pila está vacía para evitar estados inválidos.
        """
        if self.is_empty():
            raise IndexError("La pila de comandos de configuración está vacía; no hay nada que deshacer.")
        # El último elemento es siempre el comando más reciente
        return self.__command_history.pop()

    def peek(self) -> T:
        """
        Retorna el comando en el tope sin eliminarlo.
        Útil para previsualizar qué configuración se deshará.
        """
        if self.is_empty():
            raise IndexError("La pila de comandos de configuración está vacía; no hay nada que inspeccionar.")
        return self.__command_history[-1]

    def top(self) -> Optional[T]:
        """
        Retorna el tope de la pila o None si está vacía.
        Versión segura de peek() que no lanza excepción.
        """
        if self.is_empty():
            return None
        return self.__command_history[-1]

    def is_empty(self) -> bool:
        """
        Indica si no hay comandos pendientes de deshacer.
        """
        return len(self.__command_history) == 0

    def size(self) -> int:
        """
        Cantidad de comandos almacenados en la pila.
        """
        return len(self.__command_history)

    def clear(self) -> None:
        """
        Vacía el historial de comandos.
        Se usa al restablecer la configuración de fábrica del sistema.
        """
        self.__command_history.clear()

    def __repr__(self) -> str:
        return f"ConfigurationCommandStack(size={self.size()}, top={self.top()})"
