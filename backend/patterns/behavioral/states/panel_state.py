"""
Interfaz abstracta del State Pattern para el contexto de Panel Solar.

Define el contrato que todos los estados concretos de panel deben cumplir,
permitiendo que el contexto (SolarPanel) delegue el procesamiento de lecturas
al estado activo sin necesidad de condicionales if/else para las transiciones.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Importación diferida para evitar dependencia circular entre SolarPanel y PanelState
if TYPE_CHECKING:
    from domain.entities.solar_panel import SolarPanel


class PanelState(ABC):
    """
    Clase abstracta que representa un estado posible de un panel solar en EcoVolt.

    Cada estado concreto encapsula cómo el panel reacciona a nuevas lecturas de
    sensores (voltaje, corriente, temperatura). El contexto SolarPanel delega
    el manejo de lecturas al estado activo.
    """

    @abstractmethod
    def handle_reading(self, panel_context: "SolarPanel") -> str:
        """
        Procesa la lectura actual del panel según el estado en que se encuentra.

        Puede provocar una transición de estado si las lecturas superan umbrales
        (p. ej. temperatura > 75°C → FaultyPanelState).

        :param panel_context: Referencia al panel solar que actúa como contexto.
        :return: Mensaje descriptivo del resultado del procesamiento.
        """
        ...

    @abstractmethod
    def get_status_label(self) -> str:
        """
        Retorna la etiqueta legible del estado actual del panel.

        :return: Cadena con el nombre del estado (p. ej. 'Activo', 'En Espera').
        """
        ...
