"""
Entidad de dominio que representa una alerta del sistema EcoVolt.

Las alertas son notificaciones generadas automáticamente cuando el sistema
detecta condiciones anormales: sobrecalentamiento de paneles, nivel crítico
de batería, fallos de conexión, o generación por debajo de umbrales esperados.
Permiten al operador del sistema tomar acciones correctivas oportunas.
"""
from datetime import datetime


class EnergyAlert:
    """
    Representa una alerta o notificación del sistema de monitoreo EcoVolt.

    Las alertas tienen un ciclo de vida: se crean cuando el sistema detecta
    una condición anormal y se resuelven cuando el problema es atendido.
    Cada alerta registra su origen (componente que la generó), tipo, severidad
    y timestamp de creación para facilitar la auditoría y el diagnóstico.

    Tipos de alerta definidos en el dominio:
    - SOBRECALENTAMIENTO: temperatura de panel superior a 75°C
    - BATERIA_BAJA: nivel de carga de batería inferior al 20%
    - FALLO_PANEL: panel solar en estado de fallo detectado
    - GENERACION_BAJA: producción solar por debajo del umbral esperado
    - SOBRECARGA: consumo de cargas supera la capacidad de generación

    Niveles de severidad:
    - CRITICA: requiere acción inmediata para prevenir daño físico
    - ADVERTENCIA: condición que debe monitorearse y atenderse pronto
    - INFORMATIVA: notificación de cambio de estado sin riesgo inmediato
    """

    def __init__(
        self,
        alert_id: str,
        source_component_id: str,
        alert_type: str,
        severity: str,
        message: str,
        created_at: str | None = None,
    ) -> None:
        """
        Inicializa una nueva alerta del sistema EcoVolt.

        :param alert_id: Identificador único de la alerta (p. ej. 'ALERT-2024-001').
        :param source_component_id: ID del componente que originó la alerta.
        :param alert_type: Tipo de alerta (p. ej. 'SOBRECALENTAMIENTO', 'BATERIA_BAJA').
        :param severity: Nivel de severidad ('CRITICA', 'ADVERTENCIA', 'INFORMATIVA').
        :param message: Descripción detallada del problema detectado.
        :param created_at: Timestamp de creación ISO 8601. Si es None, usa la hora actual.
        :raises ValueError: Si la severidad no es una de las tres válidas.
        """
        # Severidades válidas en el dominio EcoVolt — otras serían errores de programación
        valid_severities = {"CRITICA", "ADVERTENCIA", "INFORMATIVA"}
        if severity not in valid_severities:
            raise ValueError(
                f"Severidad inválida: '{severity}'. "
                f"Debe ser una de: {', '.join(sorted(valid_severities))}"
            )

        # Todos los campos son privados para preservar la inmutabilidad de las alertas
        self.__alert_id: str = alert_id
        self.__source_component_id: str = source_component_id
        self.__alert_type: str = alert_type
        self.__severity: str = severity
        self.__message: str = message

        # Si no se proporciona timestamp, se usa el momento actual del sistema
        self.__created_at: str = created_at if created_at else datetime.now().isoformat()

        # Las alertas nacen sin resolver — se resuelven cuando el problema se atiende
        self.__is_resolved: bool = False

    # -------------------------------------------------------------------------
    # Properties de solo lectura — las alertas son inmutables una vez creadas
    # -------------------------------------------------------------------------

    @property
    def alert_id(self) -> str:
        """Identificador único e inmutable de la alerta."""
        return self.__alert_id

    @property
    def source_component_id(self) -> str:
        """ID del componente EcoVolt que originó esta alerta."""
        return self.__source_component_id

    @property
    def alert_type(self) -> str:
        """Tipo de condición anormal detectada (p. ej. 'SOBRECALENTAMIENTO')."""
        return self.__alert_type

    @property
    def severity(self) -> str:
        """Nivel de urgencia de la alerta: 'CRITICA', 'ADVERTENCIA' o 'INFORMATIVA'."""
        return self.__severity

    @property
    def message(self) -> str:
        """Descripción detallada del problema detectado por el sistema."""
        return self.__message

    @property
    def created_at(self) -> str:
        """Timestamp ISO 8601 del momento en que se generó la alerta."""
        return self.__created_at

    @property
    def is_resolved(self) -> bool:
        """Indica si el problema que originó esta alerta ya fue atendido y resuelto."""
        return self.__is_resolved

    # -------------------------------------------------------------------------
    # Métodos de operación de la alerta
    # -------------------------------------------------------------------------

    def resolve(self) -> None:
        """
        Marca la alerta como resuelta una vez que el operador ha atendido el problema.

        Una alerta resuelta permanece en el historial para auditoría y análisis
        de patrones de fallo. No se elimina del sistema, solo cambia su estado.
        Esta operación es idempotente: resolver una alerta ya resuelta no produce error.
        """
        # Permitir resolución idempotente — el operador puede confirmar múltiples veces
        self.__is_resolved = True

    def to_dict(self) -> dict:
        """
        Serializa todos los atributos de la alerta a un diccionario.

        El diccionario resultante es compatible con la API REST y la capa
        de persistencia para el historial de alertas del sistema EcoVolt.

        :return: Diccionario con todos los campos de la alerta.
        """
        return {
            "alert_id": self.__alert_id,
            "source_component_id": self.__source_component_id,
            "alert_type": self.__alert_type,
            "severity": self.__severity,
            "message": self.__message,
            "created_at": self.__created_at,
            "is_resolved": self.__is_resolved,
        }
