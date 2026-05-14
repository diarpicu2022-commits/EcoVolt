"""
Authentication service: handles login, logout and token storage.
"""
import httpx
from config.settings import settings


class AuthService:
    """Manages user authentication against the EcoVolt API."""

    def __init__(self):
        self._token: str | None = None
        self._user_email: str | None = None

    # ------------------------------------------------------------------ #
    #  Properties                                                          #
    # ------------------------------------------------------------------ #

    @property
    def token(self) -> str | None:
        return self._token

    @property
    def user_email(self) -> str | None:
        return self._user_email

    @property
    def is_authenticated(self) -> bool:
        return self._token is not None

    @property
    def auth_headers(self) -> dict:
        if not self._token:
            return {}
        return {"Authorization": f"Bearer {self._token}"}

    # ------------------------------------------------------------------ #
    #  Public methods                                                      #
    # ------------------------------------------------------------------ #

    async def login(self, email: str, password: str) -> dict:
        """
        Authenticate the user and store the JWT token.

        Returns:
            dict with keys 'success' (bool) and 'message' (str).
        """
        url = f"{settings.api_url}/auth/login"
        data = {"username": email, "password": password}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, timeout=10)

            if response.status_code == 200:
                payload = response.json()
                self._token = payload.get("access_token")
                self._user_email = email
                return {"success": True, "message": "Inicio de sesión exitoso"}

            if response.status_code == 401:
                return {"success": False, "message": "Correo o contraseña incorrectos"}

            return {"success": False, "message": f"Error del servidor ({response.status_code})"}

        except httpx.ConnectError:
            return {"success": False, "message": "No se pudo conectar al servidor"}
        except httpx.TimeoutException:
            return {"success": False, "message": "El servidor tardó demasiado en responder"}

    async def register(self, email: str, password: str) -> dict:
        """
        Register a new user account.

        Returns:
            dict with keys 'success' (bool) and 'message' (str).
        """
        url = f"{settings.api_url}/auth/register"
        payload = {"email": email, "password": password}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10)

            if response.status_code in (200, 201):
                return {"success": True, "message": "Cuenta creada exitosamente"}

            if response.status_code == 400:
                return {"success": False, "message": "El correo ya está registrado"}

            return {"success": False, "message": f"Error al registrar ({response.status_code})"}

        except httpx.ConnectError:
            return {"success": False, "message": "No se pudo conectar al servidor"}
        except httpx.TimeoutException:
            return {"success": False, "message": "El servidor tardó demasiado en responder"}

    def logout(self) -> None:
        """Clear the stored token and user information."""
        self._token = None
        self._user_email = None


# Singleton instance shared across the application
auth_service = AuthService()
