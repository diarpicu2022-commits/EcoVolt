"""
Implementación concreta de panel solar de película delgada para EcoVolt.

Los paneles de película delgada depositan capas muy finas de material fotovoltaico
(CdTe, CIGS o silicio amorfo) sobre sustratos como vidrio o plástico flexible.
Tienen la menor eficiencia (~13%) pero son más económicos y funcionan mejor
en condiciones de alta temperatura y luz difusa.
"""
from domain.entities.solar_panel import SolarPanel


class ThinFilmPanel(SolarPanel):
    """
    Nivel 3 — Panel solar de película delgada de eficiencia reducida.

    Características técnicas:
    - Eficiencia de conversión: 13% (0.13) — la más baja de las tres tecnologías
    - Menor degradación por temperatura que los paneles de silicio cristalino
    - Mejor rendimiento en condiciones de luz difusa o nublada
    - Proceso de fabricación más barato por el menor uso de material semiconductor
    - Adecuados para grandes superficies donde el espacio no es limitante

    El 13% de eficiencia significa que de cada 100W de irradiación solar incidente,
    se convierten solo 13W en electricidad utilizable, requiriendo mayor área
    para igualar la producción de paneles cristalinos.
    """

    # Constante de eficiencia de la tecnología de película delgada
    THIN_FILM_EFFICIENCY: float = 0.13

    # Potencia de pico representativa para esta tecnología en STC
    TYPICAL_PEAK_POWER_WATTS: float = 200.0

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
        panel_id: str,
        surface_area_m2: float = 2.50,  # Área mayor para compensar menor eficiencia
        peak_power_watts: float = TYPICAL_PEAK_POWER_WATTS,
        initial_voltage: float = 0.0,
        initial_current_amps: float = 0.0,
        initial_temperature_celsius: float = 25.0,
    ) -> None:
        """
        Inicializa el panel de película delgada con sus parámetros físicos.

        :param component_id: ID del componente base.
        :param installation_location: Ubicación de instalación.
        :param installation_date: Fecha de instalación ISO 8601.
        :param panel_id: Identificador del panel (p. ej. 'THIN-001').
        :param surface_area_m2: Área activa en metros cuadrados (mayor por menor eficiencia).
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
        Calcula la potencia generada por el panel de película delgada.

        Aplica la eficiencia del 13% a la potencia bruta (V × I).
        Aunque la eficiencia es menor, estos paneles mantienen mejor su
        rendimiento en climas cálidos gracias a su menor coeficiente de temperatura.

        :return: Potencia eléctrica neta generada en vatios.
        """
        # Potencia neta = V × I × eficiencia de película delgada
        return self._current_voltage * self._current_current_amps * self.THIN_FILM_EFFICIENCY

    def get_status(self) -> str:
        """
        Retorna el estado operativo del panel de película delgada con lecturas actuales.

        :return: Cadena con ID, voltaje, corriente y temperatura del panel.
        """
        return (
            f"Panel Película Delgada {self._panel_id}: "
            f"{self._current_voltage:.2f}V "
            f"{self._current_current_amps:.2f}A "
            f"{self._current_temperature_celsius:.1f}°C"
        )

    def get_efficiency(self) -> float:
        """
        Retorna la eficiencia de conversión fotovoltaica de la película delgada.

        :return: 0.13 — eficiencia del 13%, la más baja pero con ventajas térmicas.
        """
        return self.THIN_FILM_EFFICIENCY

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos del panel de película delgada a un diccionario.

        :return: Diccionario con todos los campos del panel compatible con la API REST.
        """
        return {
            # Campos de identidad heredados de EnergyComponent
            "component_id": self.component_id,
            "installation_location": self.installation_location,
            "installation_date": self.installation_date,
            # Campos específicos del panel solar
            "panel_id": self._panel_id,
            "panel_type": "thin_film",
            "surface_area_m2": self._surface_area_m2,
            "peak_power_watts": self._peak_power_watts,
            "efficiency": self.THIN_FILM_EFFICIENCY,
            # Lecturas en tiempo real del sensor
            "current_voltage": self._current_voltage,
            "current_current_amps": self._current_current_amps,
            "current_temperature_celsius": self._current_temperature_celsius,
            # Métricas calculadas
            "current_power_watts": self.get_current_power_watts(),
            "generated_power_watts": self.generate(),
            "status": self.get_status(),
        }
