"""
LoginView: authentication screen with login and registration forms.
"""
import flet as ft
from config.settings import settings
from services.auth_service import auth_service
from typing import Callable


class LoginView(ft.UserControl):
    """
    Full-screen login / register view.

    Args:
        on_login_success: Callback invoked after a successful authentication.
    """

    def __init__(self, on_login_success: Callable = None):
        super().__init__()
        self.on_login_success = on_login_success
        self._show_register = False

        # Form field references
        self._email_ref = ft.Ref[ft.TextField]()
        self._password_ref = ft.Ref[ft.TextField]()
        self._confirm_ref = ft.Ref[ft.TextField]()
        self._message_ref = ft.Ref[ft.Text]()
        self._loading_ref = ft.Ref[ft.ProgressRing]()
        self._form_ref = ft.Ref[ft.Column]()
        self._title_ref = ft.Ref[ft.Text]()
        self._submit_ref = ft.Ref[ft.ElevatedButton]()
        self._toggle_ref = ft.Ref[ft.TextButton]()

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _set_loading(self, loading: bool) -> None:
        self._loading_ref.current.visible = loading
        self._submit_ref.current.disabled = loading
        self.update()

    def _show_message(self, text: str, is_error: bool = True) -> None:
        self._message_ref.current.value = text
        self._message_ref.current.color = (
            settings.ERROR_COLOR if is_error else settings.SUCCESS_COLOR
        )
        self._message_ref.current.visible = True
        self.update()

    def _clear_message(self) -> None:
        self._message_ref.current.visible = False
        self.update()

    # ------------------------------------------------------------------ #
    #  Event handlers                                                      #
    # ------------------------------------------------------------------ #

    async def _handle_submit(self, _: ft.ControlEvent) -> None:
        email = self._email_ref.current.value.strip()
        password = self._password_ref.current.value

        if not email or not password:
            self._show_message("Por favor completa todos los campos")
            return

        self._clear_message()
        self._set_loading(True)

        if self._show_register:
            confirm = self._confirm_ref.current.value
            if password != confirm:
                self._set_loading(False)
                self._show_message("Las contraseñas no coinciden")
                return
            result = await auth_service.register(email, password)
            if result["success"]:
                self._show_message(result["message"], is_error=False)
                self._toggle_form(None)  # Switch back to login
            else:
                self._show_message(result["message"])
        else:
            result = await auth_service.login(email, password)
            if result["success"]:
                if self.on_login_success:
                    self.on_login_success()
            else:
                self._show_message(result["message"])

        self._set_loading(False)

    def _toggle_form(self, _) -> None:
        self._show_register = not self._show_register
        self._email_ref.current.value = ""
        self._password_ref.current.value = ""
        self._clear_message()

        if self._show_register:
            self._title_ref.current.value = "Crear cuenta"
            self._submit_ref.current.text = "Registrarse"
            self._toggle_ref.current.text = "¿Ya tienes cuenta? Inicia sesión"
            self._confirm_ref.current.visible = True
        else:
            self._title_ref.current.value = "Iniciar sesión"
            self._submit_ref.current.text = "Ingresar"
            self._toggle_ref.current.text = "¿No tienes cuenta? Regístrate"
            self._confirm_ref.current.visible = False

        self.update()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=settings.BACKGROUND_COLOR,
            content=ft.Row(
                expand=True,
                controls=[
                    # Left panel – branding
                    ft.Container(
                        expand=1,
                        bgcolor=settings.PRIMARY_COLOR,
                        padding=ft.padding.all(40),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.Icon(
                                    name=ft.icons.SOLAR_POWER,
                                    color=settings.SECONDARY_COLOR,
                                    size=80,
                                ),
                                ft.Text(
                                    value="EcoVolt",
                                    size=40,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.WHITE,
                                ),
                                ft.Text(
                                    value="Sistema de Energía Solar Inteligente",
                                    size=16,
                                    color=ft.colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Divider(color=ft.colors.WHITE24, height=30),
                                *[
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Icon(icon, color=settings.SECONDARY_COLOR, size=20),
                                            ft.Text(label, color=ft.colors.WHITE70, size=14),
                                        ],
                                    )
                                    for icon, label in [
                                        (ft.icons.BOLT, "Monitoreo en tiempo real"),
                                        (ft.icons.BATTERY_CHARGING_FULL, "Control de baterías"),
                                        (ft.icons.DEVICES, "Gestión de dispositivos IoT"),
                                        (ft.icons.SAVINGS, "Ahorro energético"),
                                    ]
                                ],
                            ],
                        ),
                    ),
                    # Right panel – form
                    ft.Container(
                        expand=1,
                        padding=ft.padding.all(60),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.Text(
                                    ref=self._title_ref,
                                    value="Iniciar sesión",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=settings.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    value="Bienvenido de nuevo",
                                    size=14,
                                    color=settings.TEXT_SECONDARY,
                                ),
                                ft.TextField(
                                    ref=self._email_ref,
                                    label="Correo electrónico",
                                    prefix_icon=ft.icons.EMAIL,
                                    keyboard_type=ft.KeyboardType.EMAIL,
                                    border_radius=10,
                                    focused_border_color=settings.PRIMARY_COLOR,
                                    width=360,
                                ),
                                ft.TextField(
                                    ref=self._password_ref,
                                    label="Contraseña",
                                    prefix_icon=ft.icons.LOCK,
                                    password=True,
                                    can_reveal_password=True,
                                    border_radius=10,
                                    focused_border_color=settings.PRIMARY_COLOR,
                                    width=360,
                                ),
                                ft.TextField(
                                    ref=self._confirm_ref,
                                    label="Confirmar contraseña",
                                    prefix_icon=ft.icons.LOCK_OUTLINE,
                                    password=True,
                                    can_reveal_password=True,
                                    border_radius=10,
                                    focused_border_color=settings.PRIMARY_COLOR,
                                    width=360,
                                    visible=False,
                                ),
                                ft.Text(
                                    ref=self._message_ref,
                                    value="",
                                    size=13,
                                    visible=False,
                                ),
                                ft.ProgressRing(
                                    ref=self._loading_ref,
                                    visible=False,
                                    color=settings.PRIMARY_COLOR,
                                    width=30,
                                    height=30,
                                ),
                                ft.ElevatedButton(
                                    ref=self._submit_ref,
                                    text="Ingresar",
                                    width=360,
                                    height=48,
                                    bgcolor=settings.PRIMARY_COLOR,
                                    color=ft.colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=self._handle_submit,
                                ),
                                ft.TextButton(
                                    ref=self._toggle_ref,
                                    text="¿No tienes cuenta? Regístrate",
                                    style=ft.ButtonStyle(
                                        color=settings.PRIMARY_COLOR
                                    ),
                                    on_click=self._toggle_form,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
