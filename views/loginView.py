from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Static, Input, Button
from textual.app import ComposeResult
from textual.containers import Center, Vertical


class LockDisplay(Static):
    color = reactive("white")

    def render(self) -> str:
        return f"[{self.color}]" + """             
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@#*#@@@@@@@@@
         @@@@@@@. *@* .@@@@@@@
         @@@@@@@@@@@+ -@@@@@@@
         @@@@@@@@@@ :@@@@@@@@@
         @@@@@@@@@@+@@@@@@@@@@
         @@@@@@@@@@=@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """

class LoginView(Screen):
    color = reactive("white")

    CSS_PATH = "../tcss/login.tcss"

    def compose(self) -> ComposeResult:
        yield LockDisplay(id="lock")
        with Vertical(id="login-container"):
            yield Input(placeholder="Login")
            yield Input(placeholder="Password", password=True)
            yield Button("Login", id="color-button", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "color-button":
            lock = self.query_one(LockDisplay)
            lock.color = "red"