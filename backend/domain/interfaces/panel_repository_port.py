"""
Interfaz de repositorio para la persistencia de paneles solares en EcoVolt.

Define el contrato que deben cumplir los adaptadores de persistencia de paneles,
siguiendo el patrón Repository del DDD (Domain-Driven Design) y el principio
de Inversión de Dependencias para mantener el dominio independiente del motor
de base de datos utilizado (PostgreSQL, MongoDB, SQLite, etc.).

En la arquitectura hexagonal, este es un puerto de salida (driven port) que
el dominio usa para persistir y recuperar el estado de los paneles solares.
"""
from abc import ABC, abstractmethod


class IPanelRepository(ABC):
    """
    Interfaz de repositorio para el acceso a datos de paneles solares.

    Abstrae completamente la tecnología de persistencia del dominio.
    Las implementaciones concretas en la capa de infraestructura manejan
    la traducción entre el modelo de dominio (dict) y el esquema de base de datos.

    Implementaciones esperadas:
    - PostgresPanelRepository: persistencia en base de datos relacional
    - MongoPanelRepository: persistencia en base de datos documental
    - InMemoryPanelRepository: almacenamiento en memoria para pruebas
    - JsonFilePanelRepository: persistencia en archivos JSON para prototipado
    """

    @abstractmethod
    def save(self, panel_dict: dict) -> None:
        """
        Persiste el estado de un panel solar en el almacenamiento.

        Si el panel ya existe (mismo panel_id), actualiza sus datos.
        Si es nuevo, lo inserta como un nuevo registro.
        La operación es upsert (insert or update).

        :param panel_dict: Diccionario con todos los campos del panel
                           (resultado de SolarPanel.to_dict()).
        :raises RepositoryError: Si ocurre un error de conexión o escritura.
        """
        ...

    @abstractmethod
    def find_by_id(self, panel_id: str) -> dict | None:
        """
        Busca y retorna el estado de un panel solar por su identificador.

        :param panel_id: Identificador único del panel a buscar.
        :return: Diccionario con los datos del panel si existe, None si no se encuentra.
        :raises RepositoryError: Si ocurre un error de conexión o lectura.
        """
        ...

    @abstractmethod
    def find_all(self) -> list[dict]:
        """
        Retorna todos los paneles solares registrados en el sistema.

        :return: Lista de diccionarios con los datos de cada panel.
                 Lista vacía si no hay paneles registrados.
        :raises RepositoryError: Si ocurre un error de conexión o lectura.
        """
        ...

    @abstractmethod
    def delete(self, panel_id: str) -> None:
        """
        Elimina un panel solar del almacenamiento por su identificador.

        La operación es idempotente: eliminar un panel que no existe
        no debe lanzar excepción (silently ignored).

        :param panel_id: Identificador único del panel a eliminar.
        :raises RepositoryError: Si ocurre un error de conexión o escritura.
        """
        ...
