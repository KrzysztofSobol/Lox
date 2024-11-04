from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Input
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from containerService.container import Container as ServiceContainer
from views.addView import AddView


class WebsiteItem(Static):
    def __init__(self, website, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.website = website
        self.update_content()

    def update_content(self):
        self.update(f"{self.website.name}")


class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    # Reactive variables
    websites = reactive([])
    selected_website = reactive(None)
    url = reactive("")
    login = reactive("")
    password = reactive("")

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.website_controller = ServiceContainer.getWebsiteController()
        self.credential_controller = ServiceContainer.getCredentialController()

    def on_mount(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)

    def compose(self) -> ComposeResult:
        with TextualContainer(id="app-grid"):
            with Vertical(id="left-pane"):
                with Horizontal(id="button-pane"):
                    yield Button("Add", id="add-website-button", variant="success")
                with VerticalScroll(id="left-pane-list"):
                    pass
            with VerticalScroll(id="right-pane"):
                with VerticalScroll(id="add-window"):
                    yield Input(placeholder="Url", id="url-input")
                    with Horizontal(id="password-login-pane"):
                        yield Input(placeholder="Login", id="login-input")
                        yield Input(placeholder="Password", id="password-input")
                    with Horizontal(id="add-cancel-pane"):
                        yield Button("Cancel", id="cancel-button", variant="error")
                        yield Button("Add", id="add-button", variant="success")
                yield Static("Website details will appear here", id="website-details")
        yield Footer()

    def watch_websites(self, websites: list) -> None:
        container = self.query_one("#left-pane-list")
        container.remove_children()
        for website in websites:
            container.mount(WebsiteItem(website))

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "url-input":
            self.url = event.value
        elif event.input.id == "login-input":
            self.login = event.value
        elif event.input.id == "password-input":
            self.password = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "add-website-button":
            self.app.push_screen("add_view")

        elif event.button.id == "add-button":
            if not all([self.url, self.login, self.password]):
                self.notify("Please fill in all fields", severity="error")
                return

            credential = self.credential_controller.create_credential(
                self.user.id,
                self.url,
                self.login,
                self.password
            )

            if credential:
                self.websites = self.website_controller.get_user_websites(self.user.id)
                self.url = ""
                self.login = ""
                self.password = ""
                self.query_one("#url-input").value = ""
                self.query_one("#login-input").value = ""
                self.query_one("#password-input").value = ""
                self.notify("Website added successfully!")
            else:
                self.notify("Failed to add website", severity="error")

        elif event.button.id == "cancel-button":
            self.url = ""
            self.login = ""
            self.password = ""
            self.query_one("#url-input").value = ""
            self.query_one("#login-input").value = ""
            self.query_one("#password-input").value = ""