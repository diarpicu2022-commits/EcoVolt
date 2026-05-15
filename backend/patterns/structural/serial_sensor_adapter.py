"""
Patrón Adapter — Adapter concreto para hardware serial Arduino/RPi.

SerialSensorAdapter adapta la API incompatible de SerialHardwareAdaptee al
contrato ISensorPort que exige el dominio EcoVolt. Convierte unidades de medida
(mV→V, mA→A), mapea nombres de métodos y gestiona el ciclo de vida de la conexión
serial. El dominio nunca conoce los detalles del hardware subyacente.
"""

import sys
import os

# Insertar la raíz del backend en el path para permitir imports absolutos
# independientemente del directorio de trabajo desde el que se ejecute
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from domain.interfaces.sensor_port import ISensorPort
from patterns.structural.serial_hardware_adaptee import SerialHardwareAdaptee


class SerialSensorAdapter(ISensorPort):
    """
    Adapter que traduce la API serial incompatible al contrato ISensorPort.

    Envuelve a SerialHardwareAdaptee y realiza tres adaptaciones principales:
    1. Conversión de unidades: milivolts → voltios, miliamperes → amperes.
    2. Mapeo de nombres: fetch_voltage_mv → read_voltage, fetch_celsius → read_temperature.
    3. Conversión de estado: check_device_status() str → is_connected() bool.

    El dominio EcoVolt puede usar esta clase exactamente igual que
    SimulatorSensorAdapter u otro adaptador futuro gracias a ISensorPort.
    """

    def __init__(self, port_name: str = "COM3", baud_rate: int = 9600) -> None:
        """
        Inicializa el adaptador creando el adaptee serial interno.

        Abre la conexión serial en el constructor para que el adaptador esté
        listo para usar inmediatamente tras la instanciación.

        :param port_name: Puerto serial del sistema operativo (p. ej. 'COM3', '/dev/ttyUSB0').
        :param baud_rate: Velocidad de transmisión en baudios (p. ej. 9600, 115200).
        """
        # El adaptee es privado — el dominio nunca debe acceder a él directamente
        self.__serial_adaptee: SerialHardwareAdaptee = SerialHardwareAdaptee(
            port_name=port_name,
            baud_rate=baud_rate
        )
        # Abrir la conexión serial al construir el adaptador
        connection_opened = self.__serial_adaptee.open_serial_connection()
        if not connection_opened:
            print(
                f"[SerialSensorAdapter] Advertencia: no se pudo abrir el puerto "
                f"'{port_name}'. El sistema operará en modo degradado."
            )

    # -----------------------------------------------------------------------
    # Implementación del contrato ISensorPort — métodos del dominio
    # -----------------------------------------------------------------------

    def read_voltage(self, panel_id: str) -> float:
        """
        Lee el voltaje del panel solar en voltios (V).

        Adapta fetch_voltage_mv() que retorna milivolts: divide por 1000
        para convertir a la unidad requerida por ISensorPort.

        :param panel_id: Identificador del panel del que se quiere leer el voltaje.
        :return: Voltaje medido en voltios (V).
        """
        # Conversión de unidades: milivolts → voltios (÷ 1000)
        voltage_in_millivolts = self.__serial_adaptee.fetch_voltage_mv(panel_id)
        return voltage_in_millivolts / 1000.0

    def read_current(self, panel_id: str) -> float:
        """
        Lee la corriente del panel solar en amperes (A).

        Adapta fetch_amperage_ma() que retorna miliamperes: divide por 1000
        para convertir a la unidad requerida por ISensorPort.

        :param panel_id: Identificador del panel del que se quiere leer la corriente.
        :return: Corriente medida en amperes (A).
        """
        # Conversión de unidades: miliamperes → amperes (÷ 1000)
        current_in_milliamps = self.__serial_adaptee.fetch_amperage_ma(panel_id)
        return current_in_milliamps / 1000.0

    def read_temperature(self, panel_id: str) -> float:
        """
        Lee la temperatura de la célula fotovoltaica en grados Celsius (°C).

        Adapta fetch_celsius() — la unidad es la misma pero el nombre del método
        es diferente, por lo que aun así se requiere adaptación de interfaz.

        :param panel_id: Identificador del panel del que se quiere leer la temperatura.
        :return: Temperatura medida en grados Celsius (°C).
        """
        # Mapeo de nombre: fetch_celsius → read_temperature (misma unidad)
        return self.__serial_adaptee.fetch_celsius(panel_id)

    def is_connected(self) -> bool:
        """
        Verifica si el sensor serial está conectado y operativo.

        Adapta check_device_status() que retorna 'OK'/'ERROR' (str) al bool
        requerido por ISensorPort. La conversión es: status == 'OK' → True.

        :return: True si el dispositivo responde con 'OK', False en caso contrario.
        """
        # Conversión de tipo: str ('OK'/'ERROR') → bool
        device_status: str = self.__serial_adaptee.check_device_status()
        return device_status == "OK"

    def __del__(self) -> None:
        """
        Cierra la conexión serial al destruir el adaptador para liberar el puerto.
        Evita que el puerto quede bloqueado si el adaptador sale de scope.
        """
        try:
            self.__serial_adaptee.close_serial_connection()
        except Exception:
            # Ignorar errores de limpieza en el destructor
            pass

    def __repr__(self) -> str:
        estado = "conectado" if self.is_connected() else "desconectado"
        return (
            f"SerialSensorAdapter("
            f"port='{self.__serial_adaptee.port_name}', "
            f"baud={self.__serial_adaptee.baud_rate}, "
            f"estado={estado})"
        )
