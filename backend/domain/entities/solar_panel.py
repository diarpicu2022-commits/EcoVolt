"""
Clase abstracta de Nivel 2 que representa un panel solar genérico en EcoVolt.

Extiende EnergyComponent con los atributos de medición eléctrica y térmica
propios de los paneles fotovoltaicos, e integra el State Pattern para gestionar
las transiciones operativas sin condicionales if/else.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from .energy_component import EnergyComponent

# Importación diferida: PanelState referencia a SolarPanel, evitamos ciclo
if TYPE_CHECKING:
    from ...patterns.behavioral.states.panel_state import PanelState


class SolarPanel(EnergyComponent):
    """
    Nivel 2 de la jerarquía — Clase abstracta para paneles fotovoltaicos.

    Modela los atributos comunes de cualquier tecnología de panel solar
    (monocristalino, policristalino, película delgada): área activa, potencia
    de pico, lecturas en tiempo real de voltaje, corriente y temperatura.

    Integra el State Pattern para que el comportamiento ante nuevas lecturas
    de sensores sea delegado al estado activo del panel, permitiendo transiciones
    limpias entre Activo → En Espera → Con Fallo → En Mantenimiento sin if/else.

    Los campos de medición son PROTEGIDOS (_campo) para que las subclases concretas
    puedan acceder a ellos directamente en sus cálculos de generación.
    """

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        panel_id: str,
        surface_area_m2: float,
        peak_power_watts: float,
        initial_voltage: float = 0.0,
        initial_current_amps: float = 0.0,
        initial_temperature_celsius: float = 25.0,
    ) -> None:
        """
        Inicializa el panel solar con sus parámetros físicos y eléctricos.

        :param component_id: ID del componente base (herencia de EnergyComponent).
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param panel_id: Identificador específico del panel (p. ej. 'MONO-001').
        :param surface_area_m2: Área superficial activa del panel en metros cuadrados.
        :param peak_power_watts: Potencia máxima en condiciones estándar (STC) en vatios.
        :param initial_voltage: Voltaje inicial de operación en voltios.
        :param initial_current_amps: Corriente inicial de operación en amperios.
        :param initial_temperature_celsius: Temperatura inicial de la célula en grados Celsius.
        """
        # Inicializa los campos de identidad del componente base
        super().__init__(component_id, installation_location, installation_date)

        # Campos protegidos: accesibles por subclases para cálculos de generación
        self._panel_id: str = panel_id
        self._surface_area_m2: float = surface_area_m2
        self._peak_power_watts: float = peak_power_watts
        self._current_voltage: float = initial_voltage
        self._current_current_amps: float = initial_current_amps
        self._current_temperature_celsius: float = initial_temperature_celsius

        # Campo privado con name-mangling: el estado solo se cambia mediante set_state()
        # Se inicializa como StandbyPanelState porque el panel arranca sin irradiación
        from ...patterns.behavioral.states.standby_panel_state import StandbyPanelState
        self.__panel_state: Any = StandbyPanelState()

    # -------------------------------------------------------------------------
    # Properties de solo lectura para los atributos del panel
    # -------------------------------------------------------------------------

    @property
    def panel_id(self) -> str:
        """Identificador único del panel dentro del sistema EcoVolt."""
        return self._panel_id

    @property
    def surface_area_m2(self) -> float:
        """Área superficial activa del panel en metros cuadrados."""
        return self._surface_area_m2

    @property
    def peak_power_watts(self) -> float:
        """Potencia de pico del panel en condiciones estándar de prueba (STC) en vatios."""
        return self._peak_power_watts

    @property
    def current_voltage(self) -> float:
        """Voltaje instantáneo medido en los terminales del panel (en voltios)."""
        return self._current_voltage

    @property
    def current_current_amps(self) -> float:
        """Corriente instantánea medida en el panel (en amperios)."""
        return self._current_current_amps

    @property
    def current_temperature_celsius(self) -> float:
        """Temperatura actual de la célula fotovoltaica (en grados Celsius)."""
        return self._current_temperature_celsius

    # -------------------------------------------------------------------------
    # Métodos de operación del panel
    # -------------------------------------------------------------------------

    def update_reading(
        self,
        voltage: float,
        current: float,
        temperature: float,
    ) -> None:
        """
        Actualiza las lecturas eléctricas y térmicas del panel desde los sensores.

        Después de actualizar los valores, se debe llamar a handle_reading()
        para que el estado activo evalúe si corresponde una transición.

        :param voltage: Nuevo voltaje medido en voltios.
        :param current: Nueva corriente medida en amperios.
        :param temperature: Nueva temperatura de la célula en grados Celsius.
        """
        # Actualizar mediciones antes de que el estado las evalúe
        self._current_voltage = voltage
        self._current_current_amps = current
        self._current_temperature_celsius = temperature

    def get_current_power_watts(self) -> float:
        """
        Calcula la potencia instantánea generada por el panel.

        Ley de Ohm aplicada: P = V × I (voltaje por corriente).
        No incluye el factor de eficiencia; ese ajuste lo aplica generate().

        :return: Potencia instantánea en vatios.
        """
        # Fórmula eléctrica básica: potencia = voltaje × corriente
        return self._current_voltage * self._current_current_amps

    def set_state(self, new_state: "PanelState") -> None:
        """
        Cambia el estado operativo del panel (usado por los estados concretos).

        Este método es llamado por los estados durante las transiciones,
        implementando el mecanismo central del State Pattern.

        :param new_state: Nueva instancia de PanelState que reemplaza al estado actual.
        """
        # El cambio de estado es controlado por el propio estado actual, no por el panel
        self.__panel_state = new_state

    def handle_reading(self) -> str:
        """
        Delega el procesamiento de la lectura actual al estado activo del panel.

        Aplica el principio de delegación del State Pattern: el panel no decide
        cómo comportarse, sino que lo delega al objeto de estado que lo encapsula.

        :return: Mensaje descriptivo del procesamiento según el estado actual.
        """
        # Delegación completa al estado actual — sin if/else para determinar comportamiento
        return self.__panel_state.handle_reading(self)

    # -------------------------------------------------------------------------
    # Implementación concreta del método heredado de EnergyComponent
    # -------------------------------------------------------------------------

    def get_component_info(self) -> str:
        """
        Retorna información extendida del panel incluyendo datos técnicos.

        Sobreescribe el método de EnergyComponent para incluir información
        específica del panel solar (ID de panel, área, potencia de pico).

        :return: Cadena con información de identidad y especificaciones técnicas.
        """
        base_info = super().get_component_info()
        return (
            f"{base_info} | "
            f"Panel ID: {self._panel_id} | "
            f"Área: {self._surface_area_m2}m² | "
            f"Pico: {self._peak_power_watts}W | "
            f"Estado: {self.__panel_state.get_status()}"
        )

    # -------------------------------------------------------------------------
    # Métodos abstractos — deben implementarse en cada tecnología de panel
    # -------------------------------------------------------------------------

    @abstractmethod
    def generate(self) -> float:
        """Retorna la energía generada aplicando la eficiencia de la tecnología."""
        ...

    @abstractmethod
    def get_status(self) -> str:
        """Retorna el estado operativo detallado del panel con lecturas actuales."""
        ...

    @abstractmethod
    def get_efficiency(self) -> float:
        """Retorna la eficiencia de conversión fotovoltaica de la tecnología."""
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        """Serializa todos los atributos del panel a un diccionario."""
        ...
