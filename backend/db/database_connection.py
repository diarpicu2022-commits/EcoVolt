"""
Patrón Singleton: Conexión única a la base de datos SQLite del sistema EcoVolt.
Garantiza que toda la aplicación use una sola conexión activa a la base de datos.
"""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    Singleton para la conexión a la base de datos SQLite del sistema EcoVolt.
    Centraliza el acceso a datos y evita múltiples conexiones simultáneas innecesarias.
    """

    # Variable de clase que almacena la única instancia
    _instance: Optional['DatabaseConnection'] = None
    # Bandera para evitar reinicialización del __init__
    _initialized: bool = False

    def __new__(cls) -> 'DatabaseConnection':
        """Verifica si la instancia ya existe antes de crear una nueva."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Inicializa los campos privados solo una vez."""
        if self._initialized:
            return
        # Objeto de conexión SQLite; None hasta que se llame a connect()
        self.__connection: sqlite3.Connection | None = None
        # Ruta al archivo de base de datos SQLite
        self.__db_path: str = ""
        self._initialized = True

    @classmethod
    def get_instance(cls) -> 'DatabaseConnection':
        """Retorna la única instancia de DatabaseConnection, creándola si no existe."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def connect(self, db_path: str = "ecovolt.db") -> None:
        """
        Crea la conexión a la base de datos SQLite.
        Si ya existe una conexión activa, no abre una nueva.
        """
        if self.__connection is not None:
            return
        self.__db_path = db_path
        # Habilita el acceso por nombre de columna en los resultados
        self.__connection = sqlite3.connect(self.__db_path)
        self.__connection.row_factory = sqlite3.Row

    def get_connection(self) -> sqlite3.Connection:
        """
        Retorna la conexión activa a la base de datos.
        Lanza RuntimeError si no se ha establecido conexión previamente.
        """
        if self.__connection is None:
            raise RuntimeError(
                "No hay una conexión activa. Llama a connect() antes de usar get_connection()."
            )
        return self.__connection

    def close(self) -> None:
        """Cierra la conexión activa a la base de datos y libera recursos."""
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        """
        Ejecuta una consulta SELECT y retorna los resultados como lista de diccionarios.
        Cada fila del resultado se convierte en un diccionario con nombres de columna.
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        # Convierte cada fila sqlite3.Row a diccionario estándar de Python
        return [dict(row) for row in rows]

    def execute_update(self, query: str, params: tuple = ()) -> None:
        """
        Ejecuta una sentencia INSERT, UPDATE o DELETE y confirma la transacción.
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()

    @property
    def db_path(self) -> str:
        """Retorna la ruta del archivo de base de datos activo."""
        return self.__db_path

    @property
    def is_connected(self) -> bool:
        """Indica si hay una conexión activa a la base de datos."""
        return self.__connection is not None
