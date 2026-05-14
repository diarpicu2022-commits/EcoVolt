"""
DashboardView: main screen showing real-time energy metrics and device list.
"""
import asyncio
import flet as ft
from config.settings import settings
from services.energy_service import energy_service
from services.websocket_service import ws_service
from services.auth_service import auth_service
from components.metric_card import MetricCard
from components.battery_gauge import BatteryGauge
from components.device_card import DeviceCard
from components.navbar import Navbar
from typing import Callable


class DashboardView(ft.UserControl):
    """
    Main dashboard with KPI cards, battery gauge, device list and live updates.

    Args:
        on_logout: Callback invoked when the user logs out.
    """

    def __init__(self, on_logout: Callable = None):
        super().__init__()
        self.on_logout = on_logout

        # Metric card references for live updates
        self._power_card: MetricCard | None = None
        self._solar_card: MetricCard | None = None
        self._savings_card: MetricCard | None = None
        self._temp_card: MetricCard | None = None
        self._battery_gauge: BatteryGauge | None = None

        self._devices_ref = ft.Ref[ft.Column]()
        self._loading_ref = ft.Ref[ft.ProgressRing]()
        self._last_update_ref = ft.Ref[ft.Text]()

    # ------------------------------------------------------------------ #
    #  Lifecycle                                                           #
    # ------------------------------------------------------------------ #

    def did_mount(self) -> None:
        """Called when the view is added to the page."""
        asyncio.create_task(self._load_initial_data())
        ws_service.add_listener(self._on_ws_message)
        ws_service.start_background()

    def will_unmount(self) -> None:
        """Called when the view is removed from the page."""
        ws_service.remove_listener(self._on_ws_message)

    # ------------------------------------------------------------------ #
    #  Data loading                                                        #
    # ------------------------------------------------------------------ #

    async def _load_initial_data(self) -> None:
        stats, devices = await asyncio.gather(
            energy_service.get_statistics(),
            energy_service.get_devices(),
        )
        self._update_stats(stats)
        self._render_devices(devices)
        self._loading_ref.current.visible = False
        self.update()

    def _update_stats(self, stats: dict) -> None:
        if self._power_card:
            self._power_card.update_value(f"{stats.get('total_power_kw', 0):.2f}")
        if self._solar_card:
            self._solar_card.update_value(f"{stats.get('solar_generation_kw', 0):.2f}")
        if self._savings_card:
            self._savings_card.update_value(f"{stats.get('daily_savings_usd', 0):.2f}")
        if self._battery_gauge:
            self._battery_gauge.update_level(stats.get("battery_level_pct", 0))

    def _render_devices(self, devices: list[dict]) -> None:
        if not self._devices_ref.current:
            return
        self._devices_ref.current.controls.clear()
        if not devices:
            self._devices_ref.current.controls.append(
                ft.Text(
                    value="No hay dispositivos registrados",
                    color=settings.TEXT_SECONDARY,
                    size=14,
                )
            )
        else:
            for device in devices:
                card = DeviceCard(
                    device_id=device["id"],
                    name=device["name"],
                    mac_address=device["mac_address"],
                    status=device["status"],
                    on_toggle=self._handle_device_toggle,
                )
                self._devices_ref.current.controls.append(card)
        self.update()

    # ------------------------------------------------------------------ #
    #  WebSocket handler                                                   #
    # ------------------------------------------------------------------ #

    def _on_ws_message(self, data: dict) -> None:
        """Receive live sensor data and update the UI."""
        if self._power_card:
            self._power_card.update_value(f"{data.get('power', 0):.2f}")
        if self._temp_card:
            self._temp_card.update_value(f"{data.get('temperature', 0):.1f}")
        if self._battery_gauge:
            self._battery_gauge.update_level(data.get("battery_level", 0))
        if self._last_update_ref.current:
            import datetime
            now = datetime.datetime.now().strftime("%H:%M:%S")
            self._last_update_ref.current.value = f"Última actualización: {now}"
            self.update()

    # ------------------------------------------------------------------ #
    #  Device toggle                                                       #
    # ------------------------------------------------------------------ #

    async def _handle_device_toggle(self, device_id: int, new_status: str) -> None:
        await energy_service.toggle_device(device_id, new_status)

    # ------------------------------------------------------------------ #
    #  Logout                                                              #
    # ------------------------------------------------------------------ #

    def _handle_logout(self) -> None:
        ws_service.remove_listener(self._on_ws_message)
        auth_service.logout()
        if self.on_logout:
            self.on_logout()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def build(self) -> ft.Column:
        # Instantiate metric cards
        self._power_card = MetricCard(
            title="Potencia Total",
            value="0.00",
            unit="kW",
            icon=ft.icons.BOLT,
            icon_color=settings.SECONDARY_COLOR,
        )
        self._solar_card = MetricCard(
            title="Generación Solar",
            value="0.00",
            unit="kW",
            icon=ft.icons.SOLAR_POWER,
            icon_color=settings.PRIMARY_COLOR,
        )
        self._savings_card = MetricCard(
            title="Ahorro del Día",
            value="0.00",
            unit="USD",
            icon=ft.icons.SAVINGS,
            icon_color="#1565C0",
        )
        self._temp_card = MetricCard(
            title="Temperatura",
            value="0.0",
            unit="°C",
            icon=ft.icons.THERMOSTAT,
            icon_color=settings.ERROR_COLOR,
        )
        self._battery_gauge = BatteryGauge(level=0.0)

        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Top navbar
                Navbar(
                    user_email=auth_service.user_email or "",
                    on_logout=self._handle_logout,
                ),
                # Scrollable body
                ft.Container(
                    expand=True,
                    bgcolor=settings.BACKGROUND_COLOR,
                    padding=ft.padding.all(24),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=24,
                        controls=[
                            # Section header
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                value="Panel de Control",
                                                size=24,
                                                weight=ft.FontWeight.BOLD,
                                                color=settings.TEXT_PRIMARY,
                                            ),
                                            ft.Text(
                                                ref=self._last_update_ref,
                                                value="Cargando datos...",
                                                size=12,
                                                color=settings.TEXT_SECONDARY,
                                            ),
                                        ],
                                    ),
                                    ft.ProgressRing(
                                        ref=self._loading_ref,
                                        visible=True,
                                        color=settings.PRIMARY_COLOR,
                                        width=24,
                                        height=24,
                                    ),
                                ],
                            ),
                            # KPI metric cards row
                            ft.ResponsiveRow(
                                spacing=16,
                                run_spacing=16,
                                controls=[
                                    ft.Container(
                                        col={"xs": 12, "sm": 6, "md": 3},
                                        content=self._power_card,
                                    ),
                                    ft.Container(
                                        col={"xs": 12, "sm": 6, "md": 3},
                                        content=self._solar_card,
                                    ),
                                    ft.Container(
                                        col={"xs": 12, "sm": 6, "md": 3},
                                        content=self._savings_card,
                                    ),
                                    ft.Container(
                                        col={"xs": 12, "sm": 6, "md": 3},
                                        content=self._temp_card,
                                    ),
                                ],
                            ),
                            # Battery + devices row
                            ft.ResponsiveRow(
                                spacing=16,
                                run_spacing=16,
                                controls=[
                                    # Battery gauge
                                    ft.Container(
                                        col={"xs": 12, "md": 4},
                                        content=self._battery_gauge,
                                    ),
                                    # Device list
                                    ft.Container(
                                        col={"xs": 12, "md": 8},
                                        content=ft.Container(
                                            bgcolor=settings.CARD_COLOR,
                                            border_radius=16,
                                            padding=ft.padding.all(20),
                                            shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=8,
                                                color=ft.colors.with_opacity(
                                                    0.08, ft.colors.BLACK
                                                ),
                                                offset=ft.Offset(0, 2),
                                            ),
                                            content=ft.Column(
                                                spacing=16,
                                                controls=[
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Text(
                                                                value="Dispositivos IoT",
                                                                size=18,
                                                                weight=ft.FontWeight.W_600,
                                                                color=settings.TEXT_PRIMARY,
                                                            ),
                                                            ft.Icon(
                                                                name=ft.icons.DEVICES_OTHER,
                                                                color=settings.PRIMARY_COLOR,
                                                            ),
                                                        ],
                                                    ),
                                                    ft.Divider(height=1),
                                                    ft.Column(
                                                        ref=self._devices_ref,
                                                        spacing=10,
                                                        controls=[
                                                            ft.Text(
                                                                value="Cargando dispositivos...",
                                                                color=settings.TEXT_SECONDARY,
                                                                size=14,
                                                            )
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                            # Info banner
                            ft.Container(
                                bgcolor=ft.colors.with_opacity(
                                    0.08, settings.PRIMARY_COLOR
                                ),
                                border_radius=12,
                                padding=ft.padding.all(16),
                                content=ft.Row(
                                    spacing=12,
                                    controls=[
                                        ft.Icon(
                                            name=ft.icons.INFO_OUTLINE,
                                            color=settings.PRIMARY_COLOR,
                                        ),
                                        ft.Text(
                                            value="Los datos se actualizan automáticamente vía WebSocket cuando hay nuevas lecturas de los sensores.",
                                            size=13,
                                            color=settings.PRIMARY_COLOR,
                                            expand=True,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )
