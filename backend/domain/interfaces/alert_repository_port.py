"""
Interfaz de repositorio para la persistencia de alertas del sistema EcoVolt.

Define el contrato que deben cumplir los adaptadores de persistencia de alertas,
siguiendo el patrón Repository del DDD y el principio de Inversión de Dependencias.

Las alertas tienen un flujo de vida específico: se crean (no resueltas), se
consultan para monitoreo activo y se resuelven cuando el operador atiende el problema.
Este repositorio expone operaciones especializadas para gestionar ese ciclo de vida.
"""
from abc import ABC, abstractmethod


class IAlertRepository(ABC):
    """
    Interfaz de repositorio para el acceso y persistencia de alertas EcoVolt.

    Especializada para el ciclo de vida de alertas: creación, consulta por estado
    y resolución. Las alertas resueltas se conservan en el historial para análisis
    de patrones de fallo y auditoría del sistema.

    Implementaciones esperadas:
    - PostgresAlertRepository: persistencia en base de datos relacional
    - MongoAlertRepository: persistencia en base de datos documental
    - InMemoryAlertRepository: almacenamiento en memoria para pruebas
    """

    @abstractmethod
    def save(self, alert_dict: dict) -> None:
        """
        Persiste una nueva alerta en el almacenamiento.

        Las alertas son inmutables una vez creadas (excepto el campo is_resolved),
        por lo que este método solo se usa para inserción, no para actualización
        de contenido.

        :param alert_dict: Diccionario con todos los campos de la alerta
                           (resultado de EnergyAlert.to_dict()).
        :raises RepositoryError: Si ocurre un error de conexión o escritura.
        """
        ...

    @abstractmethod
    def find_all_unresolved(self) -> list[dict]:
        """
        Retorna todas las alertas que aún no han sido resueltas.

        Este es el método principal para el panel de monitoreo del sistema:
        permite al operador ver todas las condiciones anormales activas
        que requieren atención, ordenadas por severidad y timestamp.

        :return: Lista de diccionarios con alertas no resueltas.
                 Lista vacía si no hay alertas pendientes.
        :raises RepositoryError: Si ocurre un error de conexión o lectura.
        """
        ...

    @abstractmethod
    def resolve(self, alert_id: str) -> None:
        """
        Marca una alerta como resuelta en el almacenamiento.

        Actualiza el campo is_resolved a True en el registro persistido.
        La operación es idempotente: resolver una alerta ya resuelta no produce error.

        :param alert_id: Identificador único de la alerta a resolver.
        :raises RepositoryError: Si ocurre un error de conexión o escritura.
        :raises AlertNotFoundError: Si alert_id no corresponde a ninguna alerta existente.
        """
        ...

    @abstractmethod
    def find_all(self) -> list[dict]:
        """
        Retorna todas las alertas del sistema, tanto resueltas como pendientes.

        Utilizado para la vista de historial completo de alertas, análisis de
        patrones de fallo recurrente y reportes de mantenimiento preventivo.

        :return: Lista de diccionarios con todas las alertas del sistema.
                 Lista vacía si no hay alertas registradas.
        :raises RepositoryError: Si ocurre un error de conexión o lectura.
        """
        ...
