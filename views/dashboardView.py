from textual.app import Screen, ComposeResult
from textual.containers import Container, VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Input
from repositories.WebsiteRepository import WebsiteRepository
from controllers.WebsiteController import WebsiteController

class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.websiteRepository = WebsiteRepository()
        self.websiteController = WebsiteController(self.websiteRepository)

    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                with Horizontal(id="button-pane"):
                    yield Button("Add", id="add-website-button", variant="success")
                with VerticalScroll(id="left-pane-list"):
                    if self.user:
                        websites = self.websiteController.get_user_websites(self.user.id)
                        for website in websites:
                            yield Static(f"{website.name}")
            with VerticalScroll(id="right-pane"):
                with VerticalScroll(id="add-window"):
                    yield Input(placeholder="Url", id="url-input")
                    yield Input(placeholder="Login", id="login-input")
                    yield Input(placeholder="Password", id="password-input")
                    yield Button("Add", id="add-button", variant="success")
                    yield Button("Cancel", id="cancel-button", variant="error")
                yield Static("Website details will appear here")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            self.notify("Add website button pressed")
        if event.button.id == "add-button":
            url = self.query_one("#url-input", Input).value
            login = self.query_one("#login-input", Input).value
            password = self.query_one("#password-input", Input).value
            credential = self.credentialController.createCredential(self, url, login ,password)