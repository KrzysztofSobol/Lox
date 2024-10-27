# controllers/screen_controller.py
from typing import Dict, Type
from textual.screen import Screen
from views import LoginView, DashboardView, HelpView


class ScreenController:
    def __init__(self, app):
        self.app = app
        self._views: Dict[str, Type[Screen]] = {
            "login": LoginView,
            "dashboard": DashboardView,
            "help": HelpView,
        }

    def switch_to(self, screen_name: str) -> None:
        if screen_name not in self._views:
            raise ValueError(f"Unknown screen: {screen_name}")
        self.app.switch_mode(screen_name)

    def get_available_views(self) -> Dict[str, Type[Screen]]:
        return self._views