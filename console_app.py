# main.py
from textual.app import App
from controllers.screen_controller import ScreenController
from models.app_state import AppState

class ModesApp(App):
    BINDINGS = [
        ("ctrl+d", "switch_screen('dashboard')", "Dashboard"),
        ("h", "switch_screen('help')", "Help"),
    ]

    def __init__(self):
        super().__init__()
        self.state = AppState()
        self.screen_controller = ScreenController(self)
        self._modes = self.screen_controller.get_available_views()

    def action_switch_screen(self, screen_name: str) -> None:
        self.screen_controller.switch_to(screen_name)
        self.state.set_current_screen(screen_name)

    def on_mount(self) -> None:
        self.action_switch_screen("login")

if __name__ == "__main__":
    app = ModesApp()
    app.run()