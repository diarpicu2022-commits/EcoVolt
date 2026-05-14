"""
Energy service: fetches readings, devices and statistics from the API.
"""
import httpx
from config.settings import settings
from services.auth_service import auth_service


class EnergyService:
    """Handles all energy-related API calls."""

    # ------------------------------------------------------------------ #
    #  Devices                                                             #
    # ------------------------------------------------------------------ #

    async def get_devices(self) -> list[dict]:
        """Return the list of devices registered to the current user."""
        url = f"{settings.api_url}/devices"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=auth_service.auth_headers, timeout=10
                )
            if response.status_code == 200:
                return response.json()
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        return []

    async def toggle_device(self, device_id: int, status: str) -> bool:
        """Toggle a device on/off. Returns True on success."""
        url = f"{settings.api_url}/devices/{device_id}/status"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url,
                    json={"status": status},
                    headers=auth_service.auth_headers,
                    timeout=10,
                )
            return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False

    # ------------------------------------------------------------------ #
    #  Readings                                                            #
    # ------------------------------------------------------------------ #

    async def get_latest_reading(self, device_id: int) -> dict | None:
        """Return the most recent energy reading for a device."""
        url = f"{settings.api_url}/readings/{device_id}/latest"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=auth_service.auth_headers, timeout=10
                )
            if response.status_code == 200:
                return response.json()
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        return None

    async def get_readings_history(
        self, device_id: int, limit: int = 20
    ) -> list[dict]:
        """Return the last *limit* readings for a device."""
        url = f"{settings.api_url}/readings/{device_id}?limit={limit}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=auth_service.auth_headers, timeout=10
                )
            if response.status_code == 200:
                return response.json()
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        return []

    # ------------------------------------------------------------------ #
    #  Statistics                                                          #
    # ------------------------------------------------------------------ #

    async def get_statistics(self) -> dict:
        """Return aggregated energy statistics for the dashboard."""
        url = f"{settings.api_url}/statistics"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=auth_service.auth_headers, timeout=10
                )
            if response.status_code == 200:
                return response.json()
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        # Fallback demo data so the UI is always usable
        return {
            "total_power_kw": 0.0,
            "battery_level_pct": 0.0,
            "solar_generation_kw": 0.0,
            "daily_savings_usd": 0.0,
        }

    # ------------------------------------------------------------------ #
    #  Alerts                                                              #
    # ------------------------------------------------------------------ #

    async def get_alerts(self, limit: int = 5) -> list[dict]:
        """Return the latest *limit* system alerts."""
        url = f"{settings.api_url}/alerts?limit={limit}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=auth_service.auth_headers, timeout=10
                )
            if response.status_code == 200:
                return response.json()
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        return []


# Singleton instance
energy_service = EnergyService()
