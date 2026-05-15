"""
Interfaz de puerto para sensores físicos del sistema EcoVolt.

Define el contrato (Target) del patrón Adapter que permite al dominio
comunicarse con cualquier hardware sensor sin depender de implementaciones
concretas. Sigue el principio de Inversión de Dependencias (DIP) del dominio hexagonal.

En la arquitectura hexagonal (Ports & Adapters), este puerto es un puerto
de entrada secundario (driven port) que el dominio usa para obtener lecturas
del mundo físico. Los adaptadores concretos implementan esta interfaz para
cada marca o protocolo de sensor (Modbus RTU, I2C, SPI, MQTT, etc.).
"""
from abc import ABC, abstractmethod


class ISensorPort(ABC):
    """
    Interfaz (puerto) para la comunicación con sensores de paneles solares.

    Target del patrón Adapter — el dominio solo conoce esta interfaz, nunca
    las clases concretas del hardware sensor. Permite sustituir sensores
    físicos por simuladores en pruebas sin modificar el código de dominio.

    Implementaciones esperadas en la capa de infraestructura:
    - ModbusRtuSensorAdapter: sensores industriales con protocolo Modbus
    - I2CSensorAdapter: sensores electrónicos de bajo nivel (p. ej. INA226)
    - MqttSensorAdapter: sensores IoT que publican en broker MQTT
    - SimulatedSensorAdapter: simulador para pruebas unitarias y de integración
    """

    @abstractmethod
    def read_voltage(self, panel_id: str) -> float:
        """
        Lee el voltaje actual del panel solar especificado.

        El adaptador concreto traduce esta llamada al protocolo específico
        del hardware sensor (p. ej. lectura de registro Modbus 40001).

        :param panel_id: Identificador del panel del que se quiere leer el voltaje.
        :return: Voltaje medido en voltios (V).
        :raises ConnectionError: Si el sensor no está disponible.
        :raises ValueError: Si panel_id no corresponde a ningún sensor registrado.
        """
        ...

    @abstractmethod
    def read_current(self, panel_id: str) -> float:
        """
        Lee la corriente actual generada por el panel solar especificado.

        La corriente se mide típicamente con un sensor de efecto Hall o
        una resistencia de derivación calibrada conectada al adaptador.

        :param panel_id: Identificador del panel del que se quiere leer la corriente.
        :return: Corriente medida en amperios (A).
        :raises ConnectionError: Si el sensor no está disponible.
        :raises ValueError: Si panel_id no corresponde a ningún sensor registrado.
        """
        ...

    @abstractmethod
    def read_temperature(self, panel_id: str) -> float:
        """
        Lee la temperatura actual de la célula fotovoltaica del panel especificado.

        La temperatura de la célula afecta directamente la eficiencia: por cada
        grado Celsius sobre 25°C, los paneles de silicio cristalino pierden
        aproximadamente 0.4-0.5% de eficiencia.

        :param panel_id: Identificador del panel del que se quiere leer la temperatura.
        :return: Temperatura de la célula medida en grados Celsius (°C).
        :raises ConnectionError: Si el sensor no está disponible.
        :raises ValueError: Si panel_id no corresponde a ningún sensor registrado.
        """
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Verifica si el sensor está físicamente conectado y respondiendo.

        Permite al sistema detectar fallos de comunicación con el hardware
        antes de intentar leer datos, evitando valores erróneos o excepciones
        no controladas en el flujo principal de monitoreo.

        :return: True si el sensor responde correctamente, False en caso contrario.
        """
        ...
