from textual.app import Screen, ComposeResult
from textual.containers import Container, VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button


class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                with Horizontal(id="button-pane"):
                    yield Button("Add", id="login-button3", variant="success")
                with VerticalScroll(id="left-pane-list"):
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
                    yield Static("wynncraft.com")
                    yield Static("localhost:5173")
                    yield Static("cez.wi.pb.edu.pl")
            with VerticalScroll(id="right-pane"):
                    yield Static(f"Vertical layout")
        yield Footer()