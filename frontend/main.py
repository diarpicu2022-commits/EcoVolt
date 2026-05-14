"""
EcoVolt Frontend – entry point.

Run with:
    flet run main.py
"""
import flet as ft
from config.settings import settings
from views.login_view import LoginView
from views.dashboard_view import DashboardView


class EcoVoltApp:
    """
    Root application controller.

    Manages top-level navigation between the login screen
    and the main dashboard using a simple page-swap pattern.
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self._configure_page()
        self._show_login()

    # ------------------------------------------------------------------ #
    #  Page configuration                                                  #
    # ------------------------------------------------------------------ #

    def _configure_page(self) -> None:
        self.page.title = settings.APP_TITLE
        self.page.bgcolor = settings.BACKGROUND_COLOR
        self.page.padding = 0
        self.page.spacing = 0
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.fonts = {
            "Roboto": "https://fonts.gstatic.com/s/roboto/v30/KFOmCnqEu92Fr1Me5Q.ttf"
        }
        self.page.theme = ft.Theme(
            color_scheme_seed=settings.PRIMARY_COLOR,
            use_material3=True,
        )

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #

    def _show_login(self) -> None:
        """Replace page content with the login view."""
        self.page.controls.clear()
        login = LoginView(on_login_success=self._show_dashboard)
        self.page.add(login)
        self.page.update()

    def _show_dashboard(self) -> None:
        """Replace page content with the dashboard view."""
        self.page.controls.clear()
        dashboard = DashboardView(on_logout=self._show_login)
        self.page.add(dashboard)
        self.page.update()


# ------------------------------------------------------------------ #
#  Application entry point                                             #
# ------------------------------------------------------------------ #

def main(page: ft.Page) -> None:
    EcoVoltApp(page)


if __name__ == "__main__":
    ft.app(target=main)
