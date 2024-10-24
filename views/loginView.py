# views/dashboard.py
from textual.screen import Screen
from textual.widgets import Footer, Placeholder
from textual.app import ComposeResult

class LoginView(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Login Screen")
        yield Footer()