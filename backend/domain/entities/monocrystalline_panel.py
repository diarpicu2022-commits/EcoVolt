"""
Implementación concreta de panel solar monocristalino para EcoVolt.

Los paneles monocristalinos son fabricados con silicio de grado electrónico
de alta pureza en una sola estructura cristalina, lo que les proporciona
la mayor eficiencia de conversión fotovoltaica disponible comercialmente (~22%).
Son la opción premium del sistema EcoVolt para instalaciones con espacio limitado.
"""
from domain.entities.solar_panel import SolarPanel


class MonocrystallinePanel(SolarPanel):
    """
    Nivel 3 — Panel solar monocristalino de alta eficiencia.

    Características técnicas:
    - Eficiencia de conversión: 22% (0.22) — la más alta de las tres tecnologías
    - Potencia de pico típica: 400W en condiciones estándar (STC: 1000 W/m², 25°C)
    - Reconocibles por su color negro uniforme y esquinas redondeadas
    - Mejor rendimiento en condiciones de baja luminosidad respecto a policristalinos

    La eficiencia del 22% significa que de cada 100W de irradiación solar que inciden
    sobre el panel, se convierten 22W en electricidad utilizable.
    """

    # Constante de eficiencia de la tecnología monocristalina
    MONOCRYSTALLINE_EFFICIENCY: float = 0.22

    # Potencia de pico representativa para esta tecnología en STC
    TYPICAL_PEAK_POWER_WATTS: float = 400.0

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        panel_id: str,
        surface_area_m2: float = 1.96,  # Área típica de panel de 400W
        peak_power_watts: float = TYPICAL_PEAK_POWER_WATTS,
        initial_voltage: float = 0.0,
        initial_current_amps: float = 0.0,
        initial_temperature_celsius: float = 25.0,
    ) -> None:
        """
        Inicializa el panel monocristalino con sus parámetros físicos.

        :param component_id: ID del componente base.
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param panel_id: Identificador del panel (p. ej. 'MONO-001').
        :param surface_area_m2: Área activa en metros cuadrados (por defecto 1.96m²).
        :param peak_power_watts: Potencia máxima en STC (por defecto 400W).
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
        Calcula la potencia generada por el panel monocristalino.

        Aplica la eficiencia del 22% a la potencia bruta calculada
        como voltaje × corriente (potencia eléctrica instantánea).

        La eficiencia ya incluye las pérdidas por reflexión, recombinación
        de portadores y resistencias internas del panel.

        :return: Potencia eléctrica neta generada en vatios.
        """
        # Potencia neta = V × I × factor de eficiencia de conversión fotovoltaica
        return self._current_voltage * self._current_current_amps * self.MONOCRYSTALLINE_EFFICIENCY

    def get_status(self) -> str:
        """
        Retorna el estado operativo del panel con sus lecturas actuales.

        Formato diseñado para ser legible en dashboards y logs del sistema.

        :return: Cadena con ID, voltaje, corriente y temperatura del panel.
        """
        return (
            f"Panel Monocristalino {self._panel_id}: "
            f"{self._current_voltage:.2f}V "
            f"{self._current_current_amps:.2f}A "
            f"{self._current_temperature_celsius:.1f}°C"
        )

    def get_efficiency(self) -> float:
        """
        Retorna la eficiencia de conversión fotovoltaica del monocristalino.

        :return: 0.22 — eficiencia del 22%, la más alta de las tecnologías disponibles.
        """
        return self.MONOCRYSTALLINE_EFFICIENCY

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos del panel monocristalino a un diccionario.

        El diccionario resultante es compatible con la API REST y la capa
        de persistencia del sistema EcoVolt.

        :return: Diccionario con todos los campos del panel.
        """
        return {
            # Campos de identidad heredados de EnergyComponent
            "component_id": self.component_id,
            "installation_location": self.installation_location,
            "installation_date": self.installation_date,
            # Campos específicos del panel solar
            "panel_id": self._panel_id,
            "panel_type": "monocrystalline",
            "surface_area_m2": self._surface_area_m2,
            "peak_power_watts": self._peak_power_watts,
            "efficiency": self.MONOCRYSTALLINE_EFFICIENCY,
            # Lecturas en tiempo real del sensor
            "current_voltage": self._current_voltage,
            "current_current_amps": self._current_current_amps,
            "current_temperature_celsius": self._current_temperature_celsius,
            # Métricas calculadas
            "current_power_watts": self.get_current_power_watts(),
            "generated_power_watts": self.generate(),
            "status": self.get_status(),
        }
