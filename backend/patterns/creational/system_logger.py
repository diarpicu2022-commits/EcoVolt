"""
Patrón Singleton: Logger global único del sistema EcoVolt.
Garantiza una sola instancia de registro a lo largo de toda la aplicación.
"""

from datetime import datetime
from typing import Optional


class SystemLogger:
    """
    Logger global único para el sistema de energía solar EcoVolt.
    Implementa el patrón Singleton para garantizar una única instancia.
    """

    # Variable de clase que almacena la única instancia
    _instance: Optional['SystemLogger'] = None
    # Bandera para evitar reinicialización del __init__
    _initialized: bool = False

    def __new__(cls) -> 'SystemLogger':
        """Verifica si la instancia ya existe antes de crear una nueva."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Inicializa el logger solo una vez, aunque se llame múltiples veces."""
        if self._initialized:
            return
        # Lista privada que almacena todas las entradas de log
        self.__log_entries: list[str] = []
        # Ruta privada del archivo de log
        self.__log_file_path: str = "ecovolt_system.log"
        self._initialized = True

    @classmethod
    def get_instance(cls) -> 'SystemLogger':
        """Retorna la única instancia del SystemLogger, creándola si no existe."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __format_entry(self, level: str, message: str) -> str:
        """Formatea una entrada de log con timestamp y nivel."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {level}: {message}"

    def log_info(self, message: str) -> None:
        """Registra un mensaje de nivel INFO."""
        entry = self.__format_entry("INFO", message)
        self.__log_entries.append(entry)
        print(entry)

    def log_warning(self, message: str) -> None:
        """Registra un mensaje de nivel WARNING."""
        entry = self.__format_entry("WARNING", message)
        self.__log_entries.append(entry)
        print(entry)

    def log_error(self, message: str) -> None:
        """Registra un mensaje de nivel ERROR."""
        entry = self.__format_entry("ERROR", message)
        self.__log_entries.append(entry)
        print(entry)

    def get_all_entries(self) -> list[str]:
        """Retorna todas las entradas de log registradas."""
        return list(self.__log_entries)

    def clear_logs(self) -> None:
        """Elimina todas las entradas de log del registro."""
        self.__log_entries.clear()

    @property
    def log_file_path(self) -> str:
        """Retorna la ruta del archivo de log."""
        return self.__log_file_path

    @log_file_path.setter
    def log_file_path(self, path: str) -> None:
        """Establece la ruta del archivo de log."""
        if not path or not isinstance(path, str):
            raise ValueError("La ruta del archivo de log no puede estar vacía.")
        self.__log_file_path = path
