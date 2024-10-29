from textual.app import Screen, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Static, Footer


class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            with VerticalScroll(id="left-pane"):
                yield Static("wynncraft.com")
                yield Static("localhost:5173")
                yield Static("cez.wi.pb.edu.pl")
            with VerticalScroll(id="right-pane"):
                    yield Static(f"Vertical layout")
        yield Footer()