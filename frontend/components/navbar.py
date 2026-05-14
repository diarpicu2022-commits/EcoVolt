"""
Navbar: top application bar with title, user info and logout button.
"""
import flet as ft
from config.settings import settings
from typing import Callable


class Navbar(ft.UserControl):
    """
    Top navigation bar displayed on all authenticated screens.

    Args:
        user_email:   Email of the logged-in user.
        on_logout:    Callback invoked when the user clicks logout.
    """

    def __init__(self, user_email: str, on_logout: Callable = None):
        super().__init__()
        self.user_email = user_email
        self.on_logout = on_logout

    def _handle_logout(self, _: ft.ControlEvent) -> None:
        if self.on_logout:
            self.on_logout()

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=settings.PRIMARY_COLOR,
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Brand
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(
                                name=ft.icons.SOLAR_POWER,
                                color=settings.SECONDARY_COLOR,
                                size=28,
                            ),
                            ft.Text(
                                value=settings.APP_NAME,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                            ),
                        ],
                    ),
                    # User info + logout
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(
                                name=ft.icons.ACCOUNT_CIRCLE,
                                color=ft.colors.WHITE70,
                                size=20,
                            ),
                            ft.Text(
                                value=self.user_email,
                                size=13,
                                color=ft.colors.WHITE70,
                            ),
                            ft.IconButton(
                                icon=ft.icons.LOGOUT,
                                icon_color=ft.colors.WHITE70,
                                tooltip="Cerrar sesión",
                                on_click=self._handle_logout,
                            ),
                        ],
                    ),
                ],
            ),
        )
