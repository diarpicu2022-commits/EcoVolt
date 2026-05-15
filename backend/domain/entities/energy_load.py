"""
Entidad de dominio que representa una carga eléctrica consumidora en EcoVolt.

Una carga energética es cualquier dispositivo o equipo que consume electricidad
del sistema fotovoltaico: iluminación, equipos de refrigeración, sistemas de
bombeo, electrodomésticos, etc. Su gestión por niveles de prioridad permite
al sistema EcoVolt hacer shed de carga inteligente durante períodos de baja generación.
"""


class EnergyLoad:
    """
    Representa un dispositivo o sistema consumidor de energía en EcoVolt.

    No hereda de EnergyComponent porque una carga no genera, almacena ni
    transforma energía — solo la consume. Es una entidad independiente en
    el dominio con su propio ciclo de vida y lógica de gestión.

    Los niveles de prioridad determinan el orden de desconexión durante
    situaciones de escasez energética:
    - Nivel 1 (crítico): equipos médicos, servidores, iluminación de emergencia
    - Nivel 2 (importante): refrigeración, telecomunicaciones, seguridad
    - Nivel 3 (normal): electrodomésticos no esenciales, climatización de confort
    """

    def __init__(
        self,
        load_id: str,
        device_name: str,
        power_consumption_watts: float,
        priority_level: int = 3,
        is_active: bool = False,
    ) -> None:
        """
        Inicializa la carga energética con sus parámetros de consumo y prioridad.

        :param load_id: Identificador único de la carga (p. ej. 'LOAD-001').
        :param device_name: Nombre descriptivo del dispositivo (p. ej. 'Refrigerador industrial').
        :param power_consumption_watts: Potencia nominal de consumo en vatios.
        :param priority_level: Nivel de prioridad (1=crítico, 2=importante, 3=normal).
        :param is_active: Estado inicial de la carga (activa o inactiva).
        :raises ValueError: Si el nivel de prioridad no está entre 1 y 3.
        :raises ValueError: Si el consumo de potencia es negativo.
        """
        # Validar que el nivel de prioridad sea válido — fuera de rango indica error de configuración
        if priority_level not in (1, 2, 3):
            raise ValueError(
                f"Nivel de prioridad inválido: {priority_level}. "
                f"Debe ser 1 (crítico), 2 (importante) o 3 (normal)."
            )

        # Validar que el consumo sea un valor positivo — una carga no puede generar energía
        if power_consumption_watts < 0:
            raise ValueError(
                f"El consumo de potencia no puede ser negativo: {power_consumption_watts}W"
            )

        # Todos los campos son privados con doble guion bajo para proteger la integridad
        self.__load_id: str = load_id
        self.__device_name: str = device_name
        self.__power_consumption_watts: float = power_consumption_watts
        self.__priority_level: int = priority_level
        self.__is_active: bool = is_active

    # -------------------------------------------------------------------------
    # Properties — algunas con setters para los atributos modificables
    # -------------------------------------------------------------------------

    @property
    def load_id(self) -> str:
        """Identificador único e inmutable de la carga en el sistema."""
        return self.__load_id

    @property
    def device_name(self) -> str:
        """Nombre descriptivo del dispositivo o sistema consumidor."""
        return self.__device_name

    @device_name.setter
    def device_name(self, new_name: str) -> None:
        """
        Actualiza el nombre del dispositivo.

        :param new_name: Nuevo nombre descriptivo (no puede estar vacío).
        :raises ValueError: Si el nombre está vacío o es solo espacios.
        """
        if not new_name or not new_name.strip():
            raise ValueError("El nombre del dispositivo no puede estar vacío.")
        self.__device_name = new_name.strip()

    @property
    def power_consumption_watts(self) -> float:
        """Potencia nominal de consumo del dispositivo en vatios."""
        return self.__power_consumption_watts

    @power_consumption_watts.setter
    def power_consumption_watts(self, new_power: float) -> None:
        """
        Actualiza la potencia de consumo (p. ej. tras medición real con analizador).

        :param new_power: Nueva potencia de consumo en vatios (debe ser >= 0).
        :raises ValueError: Si la potencia es negativa.
        """
        if new_power < 0:
            raise ValueError(f"La potencia de consumo no puede ser negativa: {new_power}W")
        self.__power_consumption_watts = new_power

    @property
    def priority_level(self) -> int:
        """Nivel de prioridad de la carga (1=crítico, 2=importante, 3=normal)."""
        return self.__priority_level

    @priority_level.setter
    def priority_level(self, new_level: int) -> None:
        """
        Actualiza el nivel de prioridad de la carga.

        :param new_level: Nuevo nivel de prioridad (1, 2 o 3).
        :raises ValueError: Si el nivel no es 1, 2 o 3.
        """
        if new_level not in (1, 2, 3):
            raise ValueError(
                f"Nivel de prioridad inválido: {new_level}. Debe ser 1, 2 o 3."
            )
        self.__priority_level = new_level

    @property
    def is_active(self) -> bool:
        """Indica si la carga está actualmente conectada y consumiendo energía."""
        return self.__is_active

    # -------------------------------------------------------------------------
    # Métodos de operación de la carga
    # -------------------------------------------------------------------------

    def activate(self) -> None:
        """
        Conecta la carga al sistema eléctrico EcoVolt.

        Simula el cierre del contactor o relé que conecta el dispositivo
        al bus de distribución energética del sistema fotovoltaico.
        """
        # La activación siempre es permitida — el sistema decide si hay suficiente energía
        self.__is_active = True

    def deactivate(self) -> None:
        """
        Desconecta la carga del sistema eléctrico EcoVolt.

        Simula la apertura del contactor o relé. Las cargas de nivel 3
        son las primeras en desconectarse durante escasez energética.
        """
        self.__is_active = False

    def get_daily_consumption_kwh(self) -> float:
        """
        Calcula el consumo diario estimado de la carga si permanece activa 24 horas.

        Fórmula: consumo diario (kWh) = potencia (W) × tiempo (h) / 1000
        Esta métrica se usa para planificación energética y dimensionamiento del sistema.

        :return: Consumo diario estimado en kilovatios-hora (kWh/día).
        """
        # Conversión de vatios a kilovatios multiplicando por 24 horas de operación continua
        hours_per_day: float = 24.0
        return (self.__power_consumption_watts * hours_per_day) / 1000.0

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos de la carga a un diccionario.

        Incluye métricas calculadas para enriquecer la respuesta de la API REST.

        :return: Diccionario con todos los campos de la carga energética.
        """
        priority_labels: dict = {
            1: "Crítico",
            2: "Importante",
            3: "Normal"
        }

        return {
            "load_id": self.__load_id,
            "device_name": self.__device_name,
            "power_consumption_watts": self.__power_consumption_watts,
            "priority_level": self.__priority_level,
            "priority_label": priority_labels[self.__priority_level],
            "is_active": self.__is_active,
            # Métricas calculadas para facilitar la visualización en dashboards
            "daily_consumption_kwh": self.get_daily_consumption_kwh(),
            "current_power_draw_watts": (
                self.__power_consumption_watts if self.__is_active else 0.0
            ),
        }
