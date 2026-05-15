"""
Implementación concreta de panel solar policristalino para EcoVolt.

Los paneles policristalinos están fabricados con fragmentos de silicio fundido
que forman múltiples estructuras cristalinas, resultando en un proceso de
fabricación más económico pero con menor eficiencia que el monocristalino (~17%).
Son la opción de equilibrio costo/rendimiento más popular en instalaciones EcoVolt.
"""
from domain.entities.solar_panel import SolarPanel


class PolycrystallinePanel(SolarPanel):
    """
    Nivel 3 — Panel solar policristalino de eficiencia media.

    Características técnicas:
    - Eficiencia de conversión: 17% (0.17) — equilibrio entre costo y rendimiento
    - Reconocibles por su color azul con reflejos cristalinos irregulares
    - Fabricación más económica que monocristalino por menor pureza del silicio
    - Mayor sensibilidad a altas temperaturas comparado con monocristalino

    El 17% de eficiencia significa que de cada 100W de irradiación solar que inciden
    sobre el panel, se convierten 17W en electricidad utilizable.
    """

    # Constante de eficiencia de la tecnología policristalina
    POLYCRYSTALLINE_EFFICIENCY: float = 0.17

    # Potencia de pico representativa para esta tecnología en STC
    TYPICAL_PEAK_POWER_WATTS: float = 300.0

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        panel_id: str,
        surface_area_m2: float = 1.94,  # Área típica de panel de 300W policristalino
        peak_power_watts: float = TYPICAL_PEAK_POWER_WATTS,
        initial_voltage: float = 0.0,
        initial_current_amps: float = 0.0,
        initial_temperature_celsius: float = 25.0,
    ) -> None:
        """
        Inicializa el panel policristalino con sus parámetros físicos.

        :param component_id: ID del componente base.
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param panel_id: Identificador del panel (p. ej. 'POLY-001').
        :param surface_area_m2: Área activa en metros cuadrados.
        :param peak_power_watts: Potencia máxima en STC.
        :param initial_voltage: Voltaje inicial de operación en voltios.
        :param initial_current_amps: Corriente inicial de operación en amperios.
        :param initial_temperature_celsius: Temperatura inicial de la célula en °C.
        """
        super().__init__(
            component_id=component_id,
            installation_location=installation_location,
            installation_date=installation_date,
            panel_id=panel_id,
            surface_area_m2=surface_area_m2,
            peak_power_watts=peak_power_watts,
            initial_voltage=initial_voltage,
            initial_current_amps=initial_current_amps,
            initial_temperature_celsius=initial_temperature_celsius,
        )

    # -------------------------------------------------------------------------
    # Implementación de métodos abstractos de EnergyComponent y SolarPanel
    # -------------------------------------------------------------------------

    def generate(self) -> float:
        """
        Calcula la potencia generada por el panel policristalino.

        Aplica la eficiencia del 17% a la potencia bruta (V × I).
        La menor eficiencia respecto al monocristalino se debe a las
        fronteras entre cristales que actúan como barreras para los electrones.

        :return: Potencia eléctrica neta generada en vatios.
        """
        # Potencia neta = V × I × eficiencia del policristalino
        return self._current_voltage * self._current_current_amps * self.POLYCRYSTALLINE_EFFICIENCY

    def get_status(self) -> str:
        """
        Retorna el estado operativo del panel policristalino con lecturas actuales.

        :return: Cadena con ID, voltaje, corriente y temperatura del panel.
        """
        return (
            f"Panel Policristalino {self._panel_id}: "
            f"{self._current_voltage:.2f}V "
            f"{self._current_current_amps:.2f}A "
            f"{self._current_temperature_celsius:.1f}°C"
        )

    def get_efficiency(self) -> float:
        """
        Retorna la eficiencia de conversión fotovoltaica del policristalino.

        :return: 0.17 — eficiencia del 17%, menor que el monocristalino.
        """
        return self.POLYCRYSTALLINE_EFFICIENCY

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos del panel policristalino a un diccionario.

        :return: Diccionario con todos los campos del panel compatible con la API REST.
        """
        return {
            # Campos de identidad heredados de EnergyComponent
            "component_id": self.component_id,
            "installation_location": self.installation_location,
            "installation_date": self.installation_date,
            # Campos específicos del panel solar
            "panel_id": self._panel_id,
            "panel_type": "polycrystalline",
            "surface_area_m2": self._surface_area_m2,
            "peak_power_watts": self._peak_power_watts,
            "efficiency": self.POLYCRYSTALLINE_EFFICIENCY,
            # Lecturas en tiempo real del sensor
            "current_voltage": self._current_voltage,
            "current_current_amps": self._current_current_amps,
            "current_temperature_celsius": self._current_temperature_celsius,
            # Métricas calculadas
            "current_power_watts": self.get_current_power_watts(),
            "generated_power_watts": self.generate(),
            "status": self.get_status(),
        }
