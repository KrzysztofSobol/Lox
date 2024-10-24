from textual.screen import Screen
from textual.widgets import Footer, Placeholder
from textual.app import ComposeResult

class HelpView(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Help Screen")
        yield Footer()