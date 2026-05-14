"""
Array de strings para mensajes de alerta del sistema solar EcoVolt.
Los mensajes de alerta siguen el formato: '[SEVERITY] descripción del evento'.
Por ejemplo: '[CRITICAL] Voltaje panel PV-003 fuera de rango: 58V'.
El array permite filtrar por severidad para que los operadores atiendan
primero las alertas más críticas del sistema fotovoltaico.
"""


class AlertMessageStringArray:
    """
    Array dinámico de mensajes de alerta del sistema solar EcoVolt.
    Los mensajes se ordenan alfabéticamente o se filtran por severidad
    (CRITICAL, WARNING, INFO) para gestionar la cola de atención del operador.
    Convención de formato esperada: '[SEVERITY] descripción del problema'.
    """

    def __init__(self) -> None:
        self.__alert_messages: list[str] = []

    def get(self, message_index: int) -> str:
        """
        Retorna el mensaje de alerta en la posición indicada.
        Lanza IndexError si el índice está fuera del rango actual.
        """
        self.__validate_index(message_index)
        return self.__alert_messages[message_index]

    def set(self, message_index: int, alert_message: str) -> None:
        """
        Reemplaza el mensaje en la posición indicada.
        Se usa para actualizar el estado de una alerta existente.
        """
        self.__validate_index(message_index)
        self.__alert_messages[message_index] = alert_message

    def insert_at(self, message_index: int, alert_message: str) -> None:
        """
        Inserta un mensaje de alerta en la posición indicada,
        desplazando los mensajes siguientes una posición a la derecha.
        """
        if not (0 <= message_index <= len(self.__alert_messages)):
            raise IndexError(f"Índice {message_index} fuera de rango para inserción.")
        self.__alert_messages.insert(message_index, alert_message)

    def append(self, alert_message: str) -> None:
        """
        Agrega un nuevo mensaje de alerta al final del array.
        Es la operación principal al detectar un evento en el sistema solar.
        """
        self.__alert_messages.append(alert_message)

    def delete_at(self, message_index: int) -> str:
        """
        Elimina y retorna el mensaje en la posición indicada.
        Se usa al confirmar que una alerta fue atendida por el operador.
        """
        self.__validate_index(message_index)
        return self.__alert_messages.pop(message_index)

    def delete_value(self, alert_message: str) -> bool:
        """
        Busca y elimina la primera ocurrencia exacta del mensaje especificado.
        Retorna True si se encontró y eliminó el mensaje.
        """
        message_index = self.find_index(alert_message)
        if message_index == -1:
            return False
        self.__alert_messages.pop(message_index)
        return True

    def find_index(self, alert_message: str) -> int:
        """
        Retorna el índice de la primera ocurrencia exacta del mensaje.
        Retorna -1 si el mensaje no está registrado en el array.
        """
        for idx, stored_message in enumerate(self.__alert_messages):
            if stored_message == alert_message:
                return idx
        return -1

    def contains(self, alert_message: str) -> bool:
        """
        Indica si el mensaje de alerta exacto existe en el array.
        """
        return self.find_index(alert_message) != -1

    def sort_ascending(self) -> None:
        """
        Ordena los mensajes de alerta alfabéticamente de A a Z.
        Permite agrupar alertas del mismo tipo o panel para revisión masiva.
        """
        self.__alert_messages.sort()

    def sort_descending(self) -> None:
        """
        Ordena los mensajes de alerta alfabéticamente de Z a A.
        Útil para priorizar alertas cuya severidad empieza con letras altas
        según la convención del sistema (e.g., 'WARNING' antes que 'INFO').
        """
        self.__alert_messages.sort(reverse=True)

    def filter_by_severity(self, severity: str) -> list[str]:
        """
        Retorna todos los mensajes que contienen la severidad especificada.
        La búsqueda es insensible a mayúsculas/minúsculas para mayor robustez.
        Ejemplo: filter_by_severity('CRITICAL') retorna todos los mensajes
        que contienen 'CRITICAL' en cualquier parte del texto.
        """
        severity_upper = severity.upper()
        return [
            message
            for message in self.__alert_messages
            if severity_upper in message.upper()
        ]

    def __validate_index(self, message_index: int) -> None:
        if not (0 <= message_index < len(self.__alert_messages)):
            raise IndexError(
                f"Índice {message_index} fuera de rango. "
                f"El array contiene {len(self.__alert_messages)} mensajes."
            )

    def size(self) -> int:
        return len(self.__alert_messages)

    def is_empty(self) -> bool:
        return len(self.__alert_messages) == 0

    def get_all_messages(self) -> list[str]:
        """
        Retorna una copia de todos los mensajes de alerta almacenados.
        """
        return list(self.__alert_messages)

    def clear(self) -> None:
        """
        Elimina todos los mensajes de alerta.
        Se usa al iniciar un nuevo ciclo de monitoreo del sistema solar.
        """
        self.__alert_messages.clear()

    def __repr__(self) -> str:
        return f"AlertMessageStringArray(messages={len(self.__alert_messages)})"
