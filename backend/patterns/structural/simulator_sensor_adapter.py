"""
Patrón Adapter — Adapter simulador para pruebas y desarrollo.

SimulatorSensorAdapter implementa ISensorPort generando datos realistas
sin necesidad de hardware físico. Se usa durante el desarrollo, pruebas
unitarias, demos y entornos donde no hay sensores disponibles. El dominio
lo utiliza exactamente igual que SerialSensorAdapter gracias a ISensorPort.
"""

import sys
import os
import random

# Insertar la raíz del backend en el path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from domain.interfaces.sensor_port import ISensorPort


class SimulatorSensorAdapter(ISensorPort):
    """
    Adapter simulador que genera lecturas de sensor realistas para EcoVolt.

    Implementa ISensorPort sin hardware real. Usa random con semilla derivada
    del panel_id para que el mismo panel siempre produzca lecturas dentro de
    un rango estable y reproducible, mientras añade jitter para simular las
    variaciones naturales de un panel solar real.

    Rangos de simulación basados en paneles fotovoltaicos residenciales/comerciales:
    - Voltaje: 18.0 V (poca luz) a 42.0 V (irradiancia máxima)
    - Corriente: 0.5 A (amanecer/ocaso) a 8.5 A (plena irradiancia)
    - Temperatura: 25.0 °C (temperatura ambiente) a 65.0 °C (panel bajo sol directo)
    """

    # Límites del rango de voltaje simulado en voltios (V)
    __VOLTAGE_MIN_V: float = 18.0
    __VOLTAGE_MAX_V: float = 42.0

    # Límites del rango de corriente simulada en amperes (A)
    __CURRENT_MIN_A: float = 0.5
    __CURRENT_MAX_A: float = 8.5

    # Límites del rango de temperatura simulada en grados Celsius (°C)
    __TEMPERATURE_MIN_C: float = 25.0
    __TEMPERATURE_MAX_C: float = 65.0

    # Amplitud del jitter aleatorio para cada magnitud (variación natural)
    __VOLTAGE_JITTER_V: float = 1.5
    __CURRENT_JITTER_A: float = 0.3
    __TEMPERATURE_JITTER_C: float = 2.0

    def __init__(self) -> None:
        """
        Inicializa el simulador.
        No requiere parámetros de hardware ni abre ningún recurso externo.
        """
        # El simulador siempre está listo — no hay conexión real que gestionar
        self.__is_simulator_active: bool = True

    # -----------------------------------------------------------------------
    # Implementación del contrato ISensorPort
    # -----------------------------------------------------------------------

    def read_voltage(self, panel_id: str) -> float:
        """
        Simula la lectura de voltaje del panel solar especificado en voltios (V).

        Usa una semilla derivada del panel_id para que el mismo panel siempre
        tenga un voltaje base estable, con jitter aleatorio para simular
        fluctuaciones de irradiancia solar. El offset de semilla (+ 1) garantiza
        que cada magnitud tenga una secuencia independiente.

        :param panel_id: Identificador del panel cuyo voltaje se quiere leer.
        :return: Voltaje simulado en voltios (V).
        """
        # Semilla reproducible por panel para voltaje — base estable por dispositivo
        random.seed(hash(panel_id) % 1000 + 1)
        base_voltage = random.uniform(self.__VOLTAGE_MIN_V, self.__VOLTAGE_MAX_V)

        # Restablecer semilla aleatoria para el jitter — variación natural
        random.seed(None)
        jitter = random.uniform(-self.__VOLTAGE_JITTER_V, self.__VOLTAGE_JITTER_V)

        simulated_voltage = base_voltage + jitter
        # Asegurar que el valor simulado permanezca dentro de los límites físicos
        return round(max(self.__VOLTAGE_MIN_V, min(self.__VOLTAGE_MAX_V, simulated_voltage)), 3)

    def read_current(self, panel_id: str) -> float:
        """
        Simula la lectura de corriente del panel solar especificado en amperes (A).

        Usa offset de semilla + 2 para que la corriente sea independiente del
        voltaje aunque compartan el mismo panel_id como base.

        :param panel_id: Identificador del panel cuya corriente se quiere leer.
        :return: Corriente simulada en amperes (A).
        """
        # Semilla reproducible por panel para corriente — offset diferente al voltaje
        random.seed(hash(panel_id) % 1000 + 2)
        base_current = random.uniform(self.__CURRENT_MIN_A, self.__CURRENT_MAX_A)

        # Jitter para simular variaciones de carga y sombreado parcial
        random.seed(None)
        jitter = random.uniform(-self.__CURRENT_JITTER_A, self.__CURRENT_JITTER_A)

        simulated_current = base_current + jitter
        return round(max(self.__CURRENT_MIN_A, min(self.__CURRENT_MAX_A, simulated_current)), 3)

    def read_temperature(self, panel_id: str) -> float:
        """
        Simula la lectura de temperatura de la célula fotovoltaica en grados Celsius (°C).

        Usa offset de semilla + 3 para independencia entre magnitudes del mismo panel.
        La temperatura alta reduce la eficiencia — este dato es crítico para alertas.

        :param panel_id: Identificador del panel cuya temperatura se quiere leer.
        :return: Temperatura simulada en grados Celsius (°C).
        """
        # Semilla reproducible por panel para temperatura — offset único
        random.seed(hash(panel_id) % 1000 + 3)
        base_temperature = random.uniform(self.__TEMPERATURE_MIN_C, self.__TEMPERATURE_MAX_C)

        # Jitter para simular cambios por viento, nubes o variaciones de irradiancia
        random.seed(None)
        jitter = random.uniform(-self.__TEMPERATURE_JITTER_C, self.__TEMPERATURE_JITTER_C)

        simulated_temperature = base_temperature + jitter
        return round(
            max(self.__TEMPERATURE_MIN_C, min(self.__TEMPERATURE_MAX_C, simulated_temperature)),
            3
        )

    def is_connected(self) -> bool:
        """
        Indica si el simulador está activo y listo para generar lecturas.

        Siempre retorna True — un simulador no puede perder la conexión.
        Este comportamiento es correcto para entornos de prueba donde se
        necesita un sensor que nunca falle por razones de conectividad.

        :return: Siempre True mientras el simulador esté activo.
        """
        return self.__is_simulator_active

    def deactivate(self) -> None:
        """
        Desactiva el simulador para probar el comportamiento del sistema
        cuando is_connected() retorna False sin necesidad de hardware real.
        """
        self.__is_simulator_active = False

    def activate(self) -> None:
        """Reactiva el simulador después de haberlo desactivado con deactivate()."""
        self.__is_simulator_active = True

    def __repr__(self) -> str:
        estado = "activo" if self.__is_simulator_active else "inactivo"
        return f"SimulatorSensorAdapter(estado={estado})"
