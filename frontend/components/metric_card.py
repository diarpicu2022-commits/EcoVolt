"""
MetricCard: reusable card that displays a single KPI with icon and value.
"""
import flet as ft
from config.settings import settings


class MetricCard(ft.UserControl):
    """
    A styled card showing a metric (e.g. battery level, solar power).

    Args:
        title:      Label shown below the value (in Spanish).
        value:      Current value as a formatted string.
        unit:       Unit of measurement (e.g. 'kW', '%').
        icon:       Flet icon name.
        icon_color: Hex color string for the icon.
        bg_color:   Optional background color override.
    """

    def __init__(
        self,
        title: str,
        value: str,
        unit: str,
        icon: str,
        icon_color: str = None,
        bg_color: str = None,
    ):
        super().__init__()
        self.title = title
        self.value = value
        self.unit = unit
        self.icon = icon
        self.icon_color = icon_color or settings.PRIMARY_COLOR
        self.bg_color = bg_color or settings.CARD_COLOR

        # References for live updates
        self._value_ref = ft.Ref[ft.Text]()
        self._unit_ref = ft.Ref[ft.Text]()

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def update_value(self, new_value: str, new_unit: str = None) -> None:
        """Update the displayed value without rebuilding the whole card."""
        self._value_ref.current.value = new_value
        if new_unit:
            self._unit_ref.current.value = new_unit
        self.update()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=self.bg_color,
            border_radius=16,
            padding=ft.padding.all(20),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(
                                name=self.icon,
                                color=self.icon_color,
                                size=32,
                            ),
                            ft.Container(
                                bgcolor=ft.colors.with_opacity(
                                    0.1, self.icon_color
                                ),
                                border_radius=8,
                                padding=ft.padding.all(6),
                                content=ft.Icon(
                                    name=ft.icons.TRENDING_UP,
                                    color=self.icon_color,
                                    size=16,
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        spacing=4,
                        controls=[
                            ft.Text(
                                ref=self._value_ref,
                                value=self.value,
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=settings.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                ref=self._unit_ref,
                                value=self.unit,
                                size=14,
                                color=settings.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                    ft.Text(
                        value=self.title,
                        size=13,
                        color=settings.TEXT_SECONDARY,
                    ),
                ],
            ),
        )
