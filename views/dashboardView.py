from textual.app import Screen, ComposeResult
from textual.containers import Container, VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button
from repositories.WebsiteRepository import WebsiteRepository
from controllers.WebsiteController import WebsiteController

class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.website_repository = WebsiteRepository()
        self.website_controller = WebsiteController(self.website_repository)

    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                with Horizontal(id="button-pane"):
                    yield Button("Add", id="add-website-button", variant="success")
                with VerticalScroll(id="left-pane-list"):
                    if self.user:
                        websites = self.website_controller.get_user_websites(self.user.id)
                        for website in websites:
                            yield Static(f"{website.name}")
            with VerticalScroll(id="right-pane"):
                    yield Static("Website details will appear here")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            self.notify("Add website button pressed")