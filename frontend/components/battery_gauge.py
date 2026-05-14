"""
BatteryGauge: animated circular progress indicator for battery level.
"""
import flet as ft
from config.settings import settings


class BatteryGauge(ft.UserControl):
    """
    Circular gauge that visualises battery charge percentage.

    Args:
        level: Battery level from 0.0 to 100.0.
    """

    def __init__(self, level: float = 0.0):
        super().__init__()
        self.level = max(0.0, min(100.0, level))
        self._ring_ref = ft.Ref[ft.ProgressRing]()
        self._label_ref = ft.Ref[ft.Text]()
        self._status_ref = ft.Ref[ft.Text]()

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _gauge_color(self) -> str:
        if self.level >= 60:
            return settings.SUCCESS_COLOR
        if self.level >= 30:
            return settings.WARNING_COLOR
        return settings.ERROR_COLOR

    def _status_text(self) -> str:
        if self.level >= 80:
            return "Carga óptima"
        if self.level >= 50:
            return "Carga normal"
        if self.level >= 20:
            return "Carga baja"
        return "Carga crítica"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def update_level(self, new_level: float) -> None:
        """Animate the gauge to a new battery level."""
        self.level = max(0.0, min(100.0, new_level))
        self._ring_ref.current.value = self.level / 100
        self._ring_ref.current.color = self._gauge_color()
        self._label_ref.current.value = f"{self.level:.0f}%"
        self._status_ref.current.value = self._status_text()
        self.update()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=settings.CARD_COLOR,
            border_radius=16,
            padding=ft.padding.all(24),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Text(
                        value="Nivel de Batería",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=settings.TEXT_PRIMARY,
                    ),
                    ft.Stack(
                        width=140,
                        height=140,
                        controls=[
                            ft.ProgressRing(
                                ref=self._ring_ref,
                                value=self.level / 100,
                                width=140,
                                height=140,
                                stroke_width=14,
                                color=self._gauge_color(),
                                bgcolor=ft.colors.with_opacity(
                                    0.1, ft.colors.GREY
                                ),
                            ),
                            ft.Container(
                                width=140,
                                height=140,
                                alignment=ft.alignment.center,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=2,
                                    controls=[
                                        ft.Icon(
                                            name=ft.icons.BATTERY_CHARGING_FULL,
                                            color=self._gauge_color(),
                                            size=28,
                                        ),
                                        ft.Text(
                                            ref=self._label_ref,
                                            value=f"{self.level:.0f}%",
                                            size=22,
                                            weight=ft.FontWeight.BOLD,
                                            color=settings.TEXT_PRIMARY,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    ft.Text(
                        ref=self._status_ref,
                        value=self._status_text(),
                        size=13,
                        color=self._gauge_color(),
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        )
