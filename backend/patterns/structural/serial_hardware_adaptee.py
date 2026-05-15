"""
Patrón Adapter — Adaptee (API incompatible del hardware serial).

Representa la API de bajo nivel de un dispositivo serial Arduino/Raspberry Pi
que no cumple con la interfaz ISensorPort del dominio. Sus nombres de métodos
y unidades de medida son distintos a los requeridos por el sistema EcoVolt.
El adaptador SerialSensorAdapter traducirá esta API al contrato ISensorPort.
"""

import random


class SerialHardwareAdaptee:
    """
    API incompatible de un dispositivo serial Arduino/RPi para EcoVolt.

    Sus métodos tienen nombres diferentes a ISensorPort, retorna milivolts y
    miliamps en lugar de volts y amperes, y maneja la conexión como sesión
    open/close en lugar de un simple is_connected(). El adaptador es quien
    realiza las conversiones de unidades y el mapeo de métodos.

    Si pyserial no está instalado, todos los métodos simulan valores realistas
    para permitir desarrollo y pruebas sin hardware físico.
    """

    def __init__(self, port_name: str = "COM3", baud_rate: int = 9600) -> None:
        """
        Inicializa el adaptee con parámetros de conexión serial.

        :param port_name: Puerto serial del sistema operativo (p. ej. 'COM3', '/dev/ttyUSB0').
        :param baud_rate: Velocidad de transmisión en baudios (p. ej. 9600, 115200).
        """
        # Puerto serial del sistema operativo donde está conectado el Arduino/RPi
        self.__port_name: str = port_name
        # Velocidad de transmisión serial en baudios
        self.__baud_rate: int = baud_rate
        # Indica si la conexión serial está actualmente abierta
        self.__is_open: bool = False
        # Referencia al objeto de puerto serial (pyserial) o None si no disponible
        self.__serial_connection = None

        # Intentar importar pyserial — si no está disponible, se opera en modo simulado
        try:
            import serial  # noqa: F401
            self.__pyserial_available: bool = True
        except ImportError:
            self.__pyserial_available: bool = False

    # -----------------------------------------------------------------------
    # API incompatible del hardware serial (distinta a ISensorPort)
    # -----------------------------------------------------------------------

    def open_serial_connection(self) -> bool:
        """
        Abre la conexión serial con el dispositivo Arduino/RPi.

        Este método no existe en ISensorPort — la incompatibilidad es intencional
        para demostrar el problema que resuelve el patrón Adapter.

        :return: True si la conexión se abrió exitosamente, False si falló.
        """
        if self.__pyserial_available:
            try:
                import serial
                self.__serial_connection = serial.Serial(
                    port=self.__port_name,
                    baudrate=self.__baud_rate,
                    timeout=1.0
                )
                self.__is_open = self.__serial_connection.is_open
                return self.__is_open
            except Exception as error:
                # No se pudo abrir el puerto físico — registrar el motivo
                print(f"[SerialHardwareAdaptee] No se pudo abrir {self.__port_name}: {error}")
                self.__is_open = False
                return False
        else:
            # Modo simulado: fingir que la conexión siempre se abre exitosamente
            self.__is_open = True
            return True

    def close_serial_connection(self) -> None:
        """
        Cierra la sesión serial con el dispositivo.

        También ausente en ISensorPort — el adaptador se encarga de llamar
        a este método en el momento apropiado del ciclo de vida.
        """
        if self.__pyserial_available and self.__serial_connection is not None:
            try:
                self.__serial_connection.close()
            except Exception:
                pass
        self.__is_open = False
        self.__serial_connection = None

    def fetch_voltage_mv(self, device_id: str) -> float:
        """
        Lee el voltaje del dispositivo especificado en MILIvolts (mV).

        La unidad es incompatible con ISensorPort que usa voltios (V).
        El adaptador deberá dividir este resultado por 1000 para convertir.

        :param device_id: Identificador del dispositivo sensor en el bus serial.
        :return: Voltaje medido en milivolts (mV).
        """
        if self.__pyserial_available and self.__serial_connection is not None:
            # En hardware real enviaríamos un comando y leeríamos la respuesta
            raw_response = self.__query_device(device_id, command="GET_V")
            return float(raw_response)
        else:
            # Simulación: valores entre 18 000 mV y 42 000 mV según device_id
            random.seed(hash(device_id) % 1000 + 1)
            base_voltage_mv = random.uniform(18000.0, 42000.0)
            # Agregar variación aleatoria para simular fluctuaciones reales
            random.seed(None)
            jitter = random.uniform(-500.0, 500.0)
            return round(base_voltage_mv + jitter, 2)

    def fetch_amperage_ma(self, device_id: str) -> float:
        """
        Lee la corriente del dispositivo especificado en MILIamperes (mA).

        La unidad es incompatible con ISensorPort que usa amperes (A).
        El adaptador deberá dividir este resultado por 1000 para convertir.

        :param device_id: Identificador del dispositivo sensor en el bus serial.
        :return: Corriente medida en miliamperes (mA).
        """
        if self.__pyserial_available and self.__serial_connection is not None:
            raw_response = self.__query_device(device_id, command="GET_A")
            return float(raw_response)
        else:
            # Simulación: valores entre 500 mA y 8 500 mA según device_id
            random.seed(hash(device_id) % 1000 + 2)
            base_current_ma = random.uniform(500.0, 8500.0)
            random.seed(None)
            jitter = random.uniform(-200.0, 200.0)
            return round(base_current_ma + jitter, 2)

    def fetch_celsius(self, device_id: str) -> float:
        """
        Lee la temperatura del dispositivo especificado en grados Celsius.

        Este método comparte la unidad con ISensorPort.read_temperature() pero
        tiene un nombre diferente — incompatibilidad de interfaz que el adaptador resuelve.

        :param device_id: Identificador del dispositivo sensor en el bus serial.
        :return: Temperatura medida en grados Celsius (°C).
        """
        if self.__pyserial_available and self.__serial_connection is not None:
            raw_response = self.__query_device(device_id, command="GET_T")
            return float(raw_response)
        else:
            # Simulación: valores entre 25.0 °C y 65.0 °C según device_id
            random.seed(hash(device_id) % 1000 + 3)
            base_temperature = random.uniform(25.0, 65.0)
            random.seed(None)
            jitter = random.uniform(-2.0, 2.0)
            return round(base_temperature + jitter, 2)

    def check_device_status(self) -> str:
        """
        Verifica el estado del dispositivo serial.

        Retorna una cadena de estado propia del protocolo del dispositivo.
        ISensorPort usa is_connected() que retorna bool — nuevamente incompatible.

        :return: 'OK' si el dispositivo responde correctamente, 'ERROR' si hay fallo.
        """
        if self.__pyserial_available and self.__serial_connection is not None:
            try:
                # En hardware real enviaríamos un ping y esperaríamos 'OK'
                raw_response = self.__query_device("SYSTEM", command="PING")
                return "OK" if raw_response.strip() == "PONG" else "ERROR"
            except Exception:
                return "ERROR"
        else:
            # Modo simulado: siempre reportar estado OK
            return "OK" if self.__is_open else "ERROR"

    # -----------------------------------------------------------------------
    # Métodos privados de comunicación serial de bajo nivel
    # -----------------------------------------------------------------------

    def __query_device(self, device_id: str, command: str) -> str:
        """
        Envía un comando al dispositivo serial y espera la respuesta.

        Protocolo propio del hardware: envía 'COMMAND:DEVICE_ID\\n' y
        lee la respuesta hasta encontrar el salto de línea.

        :param device_id: ID del dispositivo destino en el bus serial.
        :param command: Comando a enviar según el protocolo del firmware.
        :return: Cadena de respuesta del dispositivo sin saltos de línea.
        """
        if self.__serial_connection is None:
            raise ConnectionError(f"La conexión serial en {self.__port_name} no está abierta.")
        raw_payload = f"{command}:{device_id}\n".encode("ascii")
        self.__serial_connection.write(raw_payload)
        raw_response = self.__serial_connection.readline().decode("ascii").strip()
        return raw_response

    # -----------------------------------------------------------------------
    # Propiedades de solo lectura para inspección del estado de conexión
    # -----------------------------------------------------------------------

    @property
    def port_name(self) -> str:
        """Nombre del puerto serial configurado para este adaptee."""
        return self.__port_name

    @property
    def baud_rate(self) -> int:
        """Velocidad de transmisión en baudios configurada para este adaptee."""
        return self.__baud_rate

    @property
    def is_open(self) -> bool:
        """Indica si la conexión serial está actualmente abierta."""
        return self.__is_open

    def __repr__(self) -> str:
        estado = "abierta" if self.__is_open else "cerrada"
        return (
            f"SerialHardwareAdaptee("
            f"port='{self.__port_name}', "
            f"baud={self.__baud_rate}, "
            f"conexion={estado})"
        )
