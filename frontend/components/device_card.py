"""
DeviceCard: displays a single IoT device with its status and a toggle switch.
"""
import flet as ft
from config.settings import settings
from typing import Callable


class DeviceCard(ft.UserControl):
    """
    Card representing an IoT device (panel, inverter, battery, etc.).

    Args:
        device_id:       Unique identifier from the backend.
        name:            Human-readable device name.
        mac_address:     Device MAC address.
        status:          'online' | 'offline'.
        on_toggle:       Async callback(device_id, new_status) called on switch.
    """

    def __init__(
        self,
        device_id: int,
        name: str,
        mac_address: str,
        status: str,
        on_toggle: Callable = None,
    ):
        super().__init__()
        self.device_id = device_id
        self.name = name
        self.mac_address = mac_address
        self.status = status
        self.on_toggle = on_toggle

        self._switch_ref = ft.Ref[ft.Switch]()
        self._status_ref = ft.Ref[ft.Text]()
        self._dot_ref = ft.Ref[ft.Container]()

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _is_online(self) -> bool:
        return self.status == "online"

    def _status_color(self) -> str:
        return settings.SUCCESS_COLOR if self._is_online() else settings.ERROR_COLOR

    def _status_label(self) -> str:
        return "En línea" if self._is_online() else "Desconectado"

    # ------------------------------------------------------------------ #
    #  Event handlers                                                      #
    # ------------------------------------------------------------------ #

    async def _handle_toggle(self, e: ft.ControlEvent) -> None:
        new_status = "online" if e.control.value else "offline"
        self.status = new_status

        # Update visual indicators immediately
        self._status_ref.current.value = self._status_label()
        self._dot_ref.current.bgcolor = self._status_color()
        self.update()

        if self.on_toggle:
            await self.on_toggle(self.device_id, new_status)

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=settings.CARD_COLOR,
            border_radius=14,
            padding=ft.padding.all(16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.colors.with_opacity(0.07, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.Container(
                                bgcolor=ft.colors.with_opacity(
                                    0.1, settings.PRIMARY_COLOR
                                ),
                                border_radius=10,
                                padding=ft.padding.all(10),
                                content=ft.Icon(
                                    name=ft.icons.DEVICES,
                                    color=settings.PRIMARY_COLOR,
                                    size=24,
                                ),
                            ),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        value=self.name,
                                        size=15,
                                        weight=ft.FontWeight.W_600,
                                        color=settings.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        value=self.mac_address,
                                        size=11,
                                        color=settings.TEXT_SECONDARY,
                                    ),
                                    ft.Row(
                                        spacing=6,
                                        controls=[
                                            ft.Container(
                                                ref=self._dot_ref,
                                                width=8,
                                                height=8,
                                                border_radius=4,
                                                bgcolor=self._status_color(),
                                            ),
                                            ft.Text(
                                                ref=self._status_ref,
                                                value=self._status_label(),
                                                size=12,
                                                color=self._status_color(),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Switch(
                        ref=self._switch_ref,
                        value=self._is_online(),
                        active_color=settings.PRIMARY_COLOR,
                        on_change=self._handle_toggle,
                    ),
                ],
            ),
        )
