from textual.app import App
from views.dashboardView import DashboardView
from views.loginView import LoginView
from service.container import Container

class ModesApp(App):
    BINDINGS = [
        ("ctrl+d", "switch_screen('dashboard')", "Dashboard"),
        ("h", "switch_screen('help')", "Help"),
    ]

    SCREENS = {
        "login": LoginView,
        "dashboard": DashboardView,
    }

    def __init__(self):
        super().__init__()
        Container.initialize()

    def action_switch_screen(self, screen_name: str) -> None:
        if screen_name in self.SCREENS:
            self.push_screen(self.SCREENS[screen_name]())

    def on_mount(self) -> None:
        self.action_switch_screen("login")

if __name__ == "__main__":
    app = ModesApp()
    app.run()