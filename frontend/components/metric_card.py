"""
MetricCard: tarjeta reutilizable para mostrar métricas del dashboard.
Ejemplo: voltaje, consumo, potencia, temperatura, etc.
"""

import flet as ft
from config.settings import settings


class MetricCard(ft.UserControl):

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

        # Datos principales que recibirá la tarjeta
        self.title = title
        self.value = value
        self.unit = unit
        self.icon = icon

        # Color del icono o color principal de la app por defecto
        self.icon_color = icon_color or settings.PRIMARY_COLOR

        # Color de fondo de la tarjeta
        self.bg_color = bg_color or settings.CARD_COLOR

        # Referencias para poder actualizar valores dinámicamente
        self._value_ref = ft.Ref[ft.Text]()
        self._unit_ref = ft.Ref[ft.Text]()

    # --------------------------------------------------------------- #
    # Método para actualizar valores de la tarjeta en tiempo real
    # --------------------------------------------------------------- #

    def update_value(self, new_value: str, new_unit: str = None) -> None:

        # Actualiza el valor principal
        self._value_ref.current.value = new_value

        # Si también cambia la unidad, se actualiza
        if new_unit:
            self._unit_ref.current.value = new_unit

        # Refresca la tarjeta visualmente
        self.update()

    # --------------------------------------------------------------- #
    # Construcción visual de la tarjeta
    # --------------------------------------------------------------- #

    def build(self) -> ft.Container:

        return ft.Container(

            # Color de fondo de la tarjeta
            bgcolor=self.bg_color,

            # Bordes redondeados para un diseño más moderno
            border_radius=24,

            # Espaciado interno
            padding=ft.padding.symmetric(horizontal=24, vertical=22),

            # Animación suave al actualizar
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),

            # Sombra para dar efecto de profundidad
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=18,
                color=ft.colors.with_opacity(0.10, ft.colors.BLACK),
                offset=ft.Offset(0, 6),
            ),

            # Borde sutil alrededor de la tarjeta
            border=ft.border.all(
                1,
                ft.colors.with_opacity(0.06, ft.colors.WHITE)
            ),

            content=ft.Column(
                spacing=16,

                controls=[

                    # --------------------------------------------------- #
                    # Parte superior: iconos
                    # --------------------------------------------------- #

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            # Contenedor principal del icono
                            ft.Container(
                                padding=14,
                                border_radius=16,

                                # Fondo transparente con color del icono
                                bgcolor=ft.colors.with_opacity(
                                    0.12,
                                    self.icon_color
                                ),

                                content=ft.Icon(
                                    name=self.icon,
                                    color=self.icon_color,
                                    size=34,
                                ),
                            ),

                            # Icono decorativo de tendencia
                            ft.Container(
                                padding=10,
                                border_radius=14,

                                bgcolor=ft.colors.with_opacity(
                                    0.08,
                                    self.icon_color
                                ),

                                content=ft.Icon(
                                    name=ft.icons.TRENDING_UP,
                                    color=self.icon_color,
                                    size=18,
                                ),
                            ),
                        ],
                    ),

                    # --------------------------------------------------- #
                    # Parte central: valor y descripción
                    # --------------------------------------------------- #

                    ft.Column(
                        spacing=4,

                        controls=[

                            # Fila donde se muestra valor + unidad
                            ft.Row(
                                spacing=6,
                                vertical_alignment=ft.CrossAxisAlignment.END,

                                controls=[

                                    # Valor principal
                                    ft.Text(
                                        ref=self._value_ref,
                                        value=self.value,

                                        size=34,
                                        weight=ft.FontWeight.BOLD,

                                        color=settings.TEXT_PRIMARY,
                                    ),

                                    # Unidad del valor
                                    ft.Text(
                                        ref=self._unit_ref,
                                        value=self.unit,

                                        size=16,
                                        weight=ft.FontWeight.W_500,

                                        color=settings.TEXT_SECONDARY,
                                    ),
                                ],
                            ),

                            # Texto descriptivo de la métrica
                            ft.Text(
                                value=self.title,

                                size=14,
                                weight=ft.FontWeight.W_500,

                                color=settings.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                ],
            ),
        )