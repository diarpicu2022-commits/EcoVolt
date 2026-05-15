"""
Interfaz abstracta del State Pattern para el contexto de Batería.

Define el contrato que todos los estados concretos de batería deben cumplir,
permitiendo que el contexto (Battery) delegue su comportamiento al estado actual
sin necesidad de condicionales if/else para las transiciones.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Importación diferida para evitar dependencia circular entre Battery y BatteryState
if TYPE_CHECKING:
    from ....domain.entities.battery import Battery


class BatteryState(ABC):
    """
    Clase abstracta que representa un estado posible de una batería en el sistema EcoVolt.

    Cada estado concreto encapsula el comportamiento específico de la batería
    cuando se encuentra en dicho estado (cargando, descargando, llena, baja).
    El contexto Battery delega las operaciones de carga y descarga al estado activo.
    """

    @abstractmethod
    def handle_charge(self, battery_context: "Battery") -> str:
        """
        Gestiona la operación de carga sobre la batería según el estado actual.

        :param battery_context: Referencia a la batería que actúa como contexto.
        :return: Mensaje descriptivo del resultado de la operación.
        """
        ...

    @abstractmethod
    def handle_discharge(self, battery_context: "Battery") -> str:
        """
        Gestiona la operación de descarga sobre la batería según el estado actual.

        :param battery_context: Referencia a la batería que actúa como contexto.
        :return: Mensaje descriptivo del resultado de la operación.
        """
        ...

    @abstractmethod
    def get_status(self) -> str:
        """
        Retorna la etiqueta legible del estado actual de la batería.

        :return: Cadena con el nombre del estado (p. ej. 'Cargando', 'Batería Baja').
        """
        ...

    def get_status_label(self) -> str:
        # Mantiene compatibilidad con el nombre anterior sin romper el contrato nuevo.
        return self.get_status()
