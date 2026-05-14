"""
WebSocket service: maintains a real-time connection to the backend
and dispatches incoming messages to registered listeners.
"""
import asyncio
import json
from typing import Callable
import websockets
from config.settings import settings
from services.auth_service import auth_service


class WebSocketService:
    """Manages the persistent WebSocket connection for live sensor data."""

    def __init__(self):
        self._connection = None
        self._listeners: list[Callable[[dict], None]] = []
        self._running: bool = False

    # ------------------------------------------------------------------ #
    #  Listener management                                                 #
    # ------------------------------------------------------------------ #

    def add_listener(self, callback: Callable[[dict], None]) -> None:
        """Register a callback that receives every incoming message."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[dict], None]) -> None:
        """Unregister a previously added callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    # ------------------------------------------------------------------ #
    #  Connection lifecycle                                                #
    # ------------------------------------------------------------------ #

    async def connect(self) -> None:
        """Open the WebSocket connection and start listening."""
        if self._running:
            return

        token = auth_service.token
        if not token:
            return

        url = f"{settings.ws_url}/ws?token={token}"
        self._running = True

        try:
            async with websockets.connect(url) as ws:
                self._connection = ws
                await self._listen(ws)
        except (websockets.exceptions.WebSocketException, OSError):
            pass
        finally:
            self._running = False
            self._connection = None

    async def _listen(self, ws) -> None:
        """Internal loop that reads messages and notifies listeners."""
        async for raw_message in ws:
            try:
                data = json.loads(raw_message)
                for listener in self._listeners:
                    listener(data)
            except json.JSONDecodeError:
                pass

    async def disconnect(self) -> None:
        """Close the WebSocket connection gracefully."""
        self._running = False
        if self._connection:
            await self._connection.close()
            self._connection = None

    def start_background(self) -> None:
        """Launch the WebSocket listener as a background asyncio task."""
        asyncio.create_task(self.connect())


# Singleton instance
ws_service = WebSocketService()
