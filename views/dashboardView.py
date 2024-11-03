from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Input
from textual.containers import Container as TextualContainer
from service.container import Container as ServiceContainer

class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.website_controller = ServiceContainer.get_website_controller()
        self.credential_controller = ServiceContainer.get_credential_controller()

    def compose(self) -> ComposeResult:
        with TextualContainer(id="app-grid"):
            with Vertical(id="left-pane"):
                with Horizontal(id="button-pane"):
                    yield Button("Add", id="add-website-button", variant="success")
                with VerticalScroll(id="left-pane-list"):
                    if self.user:
                        websites = self.website_controller.get_user_websites(self.user.id)
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
            credential = self.credential_controller.create_credential(self.user.id, url, login, password)