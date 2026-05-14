import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    WS_BASE_URL: str = os.getenv("WS_BASE_URL", "ws://localhost:8000")

    APP_NAME: str = "EcoVolt"
    APP_TITLE: str = "EcoVolt - Sistema de Energia Solar Inteligente"
    PRIMARY_COLOR: str = "#2C6E49"
    SECONDARY_COLOR: str = "#F4A300"
    ACCENT_COLOR: str = "#F05D23"
    BACKGROUND_COLOR: str = "#F6F1DE"
    SURFACE_COLOR: str = "#FFFDF7"
    TEXT_PRIMARY: str = "#17301F"
    TEXT_SECONDARY: str = "#5D6D63"
    SUCCESS_COLOR: str = "#2E8B57"
    WARNING_COLOR: str = "#D9822B"
    ERROR_COLOR: str = "#C44536"

    @property
    def api_url(self) -> str:
        return f"{self.API_BASE_URL}{self.API_V1_STR}"

    @property
    def ws_url(self) -> str:
        return f"{self.WS_BASE_URL}{self.API_V1_STR}"

    @property
    def navigation_items(self) -> list[dict]:
        # Mantiene la navegacion declarativa y facil de reutilizar en Jinja.
        return [
            {"label": "Dashboard", "href": "/dashboard", "key": "dashboard"},
            {"label": "Paneles", "href": "/paneles", "key": "paneles"},
            {"label": "Baterias", "href": "/baterias", "key": "baterias"},
            {"label": "Cargas", "href": "/cargas", "key": "cargas"},
            {"label": "Alertas", "href": "/alertas", "key": "alertas"},
        ]


settings = Settings()
