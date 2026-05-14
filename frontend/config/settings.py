"""
Application settings loaded from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central configuration class for the EcoVolt frontend application."""

    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    WS_BASE_URL: str = os.getenv("WS_BASE_URL", "ws://localhost:8000")

    # App appearance
    APP_NAME: str = "EcoVolt"
    APP_TITLE: str = "EcoVolt - Sistema de Energía Solar Inteligente"
    PRIMARY_COLOR: str = "#2E7D32"       # dark green
    SECONDARY_COLOR: str = "#F9A825"     # solar yellow
    BACKGROUND_COLOR: str = "#F5F5F5"
    CARD_COLOR: str = "#FFFFFF"
    TEXT_PRIMARY: str = "#212121"
    TEXT_SECONDARY: str = "#757575"
    SUCCESS_COLOR: str = "#43A047"
    WARNING_COLOR: str = "#FB8C00"
    ERROR_COLOR: str = "#E53935"

    @property
    def api_url(self) -> str:
        return f"{self.API_BASE_URL}{self.API_V1_STR}"

    @property
    def ws_url(self) -> str:
        return f"{self.WS_BASE_URL}{self.API_V1_STR}"


settings = Settings()
