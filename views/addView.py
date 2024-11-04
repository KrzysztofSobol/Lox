from textual.screen import Screen
from textual.widgets import Footer, Placeholder
from textual.app import ComposeResult

class AddView(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("AddView")
        yield Footer()