from textual.screen import Screen
from textual.widgets import Footer, Placeholder
from textual.app import ComposeResult

class DashboardView(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Dashboard Screen")
        yield Footer()