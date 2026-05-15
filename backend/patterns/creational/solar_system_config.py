"""
Patrón Singleton: Configuración global única del sistema solar EcoVolt.
Centraliza todos los parámetros de configuración del sistema en una sola instancia.
"""

from typing import Optional


class SolarSystemConfig:
    """
    Configuración global única del sistema de energía solar EcoVolt.
    Implementa el patrón Singleton para garantizar que todos los módulos
    compartan la misma configuración.
    """

    # Variable de clase que almacena la única instancia
    _instance: Optional['SolarSystemConfig'] = None
    # Bandera para evitar reinicialización del __init__
    _initialized: bool = False

    def __new__(cls) -> 'SolarSystemConfig':
        """Verifica si la instancia ya existe antes de crear una nueva."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Inicializa la configuración solo una vez, aunque se llame múltiples veces."""
        if self._initialized:
            return
        # Voltaje máximo permitido para los paneles solares (Voltios)
        self.__max_panel_voltage: float = 50.0
        # Voltaje mínimo permitido para los paneles solares (Voltios)
        self.__min_panel_voltage: float = 0.5
        # Temperatura máxima permitida para los paneles (grados Celsius)
        self.__max_temperature_celsius: float = 75.0
        # Umbral de batería baja en porcentaje
        self.__battery_low_threshold_percent: float = 20.0
        # Intervalo de sondeo de sensores en segundos
        self.__sensor_polling_interval_seconds: int = 5
        # Indica si se usa simulador (True) o hardware real (False)
        self.__use_simulator: bool = True
        # Puerto serial para comunicación con hardware real
        self.__serial_port: str = "COM3"
        self._initialized = True

    @classmethod
    def get_instance(cls) -> 'SolarSystemConfig':
        """Retorna la única instancia de SolarSystemConfig, creándola si no existe."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # --- Getters y setters con validación para max_panel_voltage ---

    @property
    def max_panel_voltage(self) -> float:
        """Retorna el voltaje máximo permitido para los paneles solares."""
        return self.__max_panel_voltage

    @max_panel_voltage.setter
    def max_panel_voltage(self, voltage: float) -> None:
        """Establece el voltaje máximo con validación de rango."""
        if voltage <= 0:
            raise ValueError("El voltaje máximo del panel debe ser mayor que 0.")
        if voltage <= self.__min_panel_voltage:
            raise ValueError("El voltaje máximo debe ser mayor que el voltaje mínimo.")
        self.__max_panel_voltage = voltage

    # --- Getters y setters con validación para min_panel_voltage ---

    @property
    def min_panel_voltage(self) -> float:
        """Retorna el voltaje mínimo permitido para los paneles solares."""
        return self.__min_panel_voltage

    @min_panel_voltage.setter
    def min_panel_voltage(self, voltage: float) -> None:
        """Establece el voltaje mínimo con validación de rango."""
        if voltage < 0:
            raise ValueError("El voltaje mínimo del panel no puede ser negativo.")
        if voltage >= self.__max_panel_voltage:
            raise ValueError("El voltaje mínimo debe ser menor que el voltaje máximo.")
        self.__min_panel_voltage = voltage

    # --- Getters y setters con validación para max_temperature_celsius ---

    @property
    def max_temperature_celsius(self) -> float:
        """Retorna la temperatura máxima permitida en grados Celsius."""
        return self.__max_temperature_celsius

    @max_temperature_celsius.setter
    def max_temperature_celsius(self, temperature: float) -> None:
        """Establece la temperatura máxima con validación de rango."""
        if temperature <= 0:
            raise ValueError("La temperatura máxima debe ser mayor que 0°C.")
        if temperature > 200:
            raise ValueError("La temperatura máxima no puede superar los 200°C.")
        self.__max_temperature_celsius = temperature

    # --- Getters y setters con validación para battery_low_threshold_percent ---

    @property
    def battery_low_threshold_percent(self) -> float:
        """Retorna el umbral de batería baja en porcentaje."""
        return self.__battery_low_threshold_percent

    @battery_low_threshold_percent.setter
    def battery_low_threshold_percent(self, threshold: float) -> None:
        """Establece el umbral de batería baja con validación de rango."""
        if not (0.0 <= threshold <= 100.0):
            raise ValueError("El umbral de batería baja debe estar entre 0 y 100%.")
        self.__battery_low_threshold_percent = threshold

    # --- Getters y setters con validación para sensor_polling_interval_seconds ---

    @property
    def sensor_polling_interval_seconds(self) -> int:
        """Retorna el intervalo de sondeo de sensores en segundos."""
        return self.__sensor_polling_interval_seconds

    @sensor_polling_interval_seconds.setter
    def sensor_polling_interval_seconds(self, interval: int) -> None:
        """Establece el intervalo de sondeo con validación de rango."""
        if not isinstance(interval, int) or interval < 1:
            raise ValueError("El intervalo de sondeo debe ser un entero positivo mayor o igual a 1.")
        self.__sensor_polling_interval_seconds = interval

    # --- Getters y setters con validación para use_simulator ---

    @property
    def use_simulator(self) -> bool:
        """Retorna True si se usa el simulador, False si se usa hardware real."""
        return self.__use_simulator

    @use_simulator.setter
    def use_simulator(self, enabled: bool) -> None:
        """Activa o desactiva el modo simulador."""
        if not isinstance(enabled, bool):
            raise ValueError("El parámetro use_simulator debe ser un valor booleano.")
        self.__use_simulator = enabled

    # --- Getters y setters con validación para serial_port ---

    @property
    def serial_port(self) -> str:
        """Retorna el puerto serial configurado para comunicación con hardware."""
        return self.__serial_port

    @serial_port.setter
    def serial_port(self, port: str) -> None:
        """Establece el puerto serial con validación básica de formato."""
        if not port or not isinstance(port, str):
            raise ValueError("El puerto serial no puede estar vacío.")
        self.__serial_port = port

    def __repr__(self) -> str:
        """Representación legible de la configuración actual del sistema."""
        return (
            f"SolarSystemConfig("
            f"max_panel_voltage={self.__max_panel_voltage}V, "
            f"min_panel_voltage={self.__min_panel_voltage}V, "
            f"max_temperature={self.__max_temperature_celsius}°C, "
            f"battery_low_threshold={self.__battery_low_threshold_percent}%, "
            f"polling_interval={self.__sensor_polling_interval_seconds}s, "
            f"use_simulator={self.__use_simulator}, "
            f"serial_port='{self.__serial_port}')"
        )
