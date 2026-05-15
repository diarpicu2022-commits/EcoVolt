"""
Clase abstracta base de la jerarquía de componentes energéticos de EcoVolt.

Define el contrato común que todos los componentes del sistema fotovoltaico
deben cumplir: paneles solares, baterías e inversores. Establece los campos
de identidad y ubicación, y declara las operaciones fundamentales del dominio.
"""
from abc import ABC, abstractmethod


class EnergyComponent(ABC):
    """
    Nivel 1 de la jerarquía de dominio — Clase abstracta base de EcoVolt.

    Representa cualquier componente físico del sistema de energía solar que
    puede generar, almacenar o transformar energía eléctrica. Todos los
    componentes comparten un identificador único, una ubicación de instalación
    y una fecha de puesta en servicio.

    Los campos de identidad son privados con name-mangling de Python (__campo)
    para encapsular los datos de infraestructura y exponerlos solo a través
    de properties de solo lectura.
    """

    def __init__(
        self,
        component_id: str,
        installation_location: str,
        installation_date: str,
    ) -> None:
        """
        Inicializa los campos de identidad del componente energético.

        :param component_id: Identificador único del componente (p. ej. 'PANEL-001').
        :param installation_location: Descripción de la ubicación física de instalación.
        :param installation_date: Fecha de instalación en formato ISO 8601 (AAAA-MM-DD).
        """
        # Campos privados con doble guion bajo: solo accesibles mediante properties
        self.__component_id: str = component_id
        self.__installation_location: str = installation_location
        self.__installation_date: str = installation_date

    # -------------------------------------------------------------------------
    # Properties de solo lectura — evitan mutación directa de identidad
    # -------------------------------------------------------------------------

    @property
    def component_id(self) -> str:
        """Identificador único e inmutable del componente en el sistema."""
        return self.__component_id

    @property
    def installation_location(self) -> str:
        """Ubicación física donde el componente fue instalado."""
        return self.__installation_location

    @property
    def installation_date(self) -> str:
        """Fecha de instalación del componente en formato ISO 8601."""
        return self.__installation_date

    # -------------------------------------------------------------------------
    # Métodos abstractos — contrato obligatorio para toda subclase concreta
    # -------------------------------------------------------------------------

    @abstractmethod
    def generate(self) -> float:
        """
        Calcula y retorna la energía generada o disponible en el componente.

        Para paneles solares: retorna watts generados según lecturas actuales.
        Para baterías: retorna kWh disponibles según nivel de carga.

        :return: Energía generada o disponible (en watts o kWh según el componente).
        """
        ...

    @abstractmethod
    def get_status(self) -> str:
        """
        Retorna una descripción legible del estado operativo actual del componente.

        :return: Cadena con el estado actual (incluye lecturas relevantes según tipo).
        """
        ...

    @abstractmethod
    def get_efficiency(self) -> float:
        """
        Retorna la eficiencia de conversión energética del componente.

        :return: Eficiencia como fracción decimal entre 0.0 y 1.0
                 (p. ej. 0.22 = 22% de eficiencia para panel monocristalino).
        """
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Serializa el estado completo del componente a un diccionario.

        Permite la persistencia en base de datos y la transferencia via API REST.

        :return: Diccionario con todos los campos del componente.
        """
        ...

    # -------------------------------------------------------------------------
    # Método concreto — implementación compartida por todas las subclases
    # -------------------------------------------------------------------------

    def get_component_info(self) -> str:
        """
        Retorna información básica de identificación del componente.

        Método concreto disponible para todas las subclases sin necesidad
        de reimplementación, ya que la información de identidad es común.

        :return: Cadena con el ID y la ubicación del componente.
        """
        return (
            f"Componente [{self.__component_id}] — "
            f"Ubicación: {self.__installation_location} — "
            f"Instalado: {self.__installation_date}"
        )
