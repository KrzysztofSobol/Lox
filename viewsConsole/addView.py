from textual.containers import Grid, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Footer, Input, Button, Label
from textual.app import ComposeResult
from containerService.container import Container as ServiceContainer

class AddView(ModalScreen[int | None]):
    CSS_PATH = "../tcss/addView.tcss"

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.website_controller = ServiceContainer.getWebsiteController()
        self.credential_controller = ServiceContainer.getCredentialController()

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="add-window"):
            yield Input(placeholder="Url", id="url-input")
            with Horizontal(id="password-login-pane"):
                yield Input(placeholder="Login", id="login-input-add")
                yield Input(placeholder="Password", id="password-input-add")
            with Horizontal(id="add-cancel-pane"):
                yield Button("Cancel", id="cancel-button", variant="error")
                yield Button("Add", id="add-button", variant="success")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-button":
            url = self.query_one("#url-input", Input).value
            login = self.query_one("#login-input-add", Input).value
            password = self.query_one("#password-input-add", Input).value

            if not all([url, login, password]):
                self.notify("Please fill in all fields", severity="error")
                return
            else:
                # Create website and credential
                credential = self.credential_controller.create_credential(self.user.id, url, login, password)
                if credential:
                    self.notify("Website added successfully!")
                    # Dismiss with the website ID
                    self.dismiss(credential.website_id)
                else:
                    self.notify("Failed to add website", severity="error")
                    self.dismiss(None)

        elif event.button.id == "cancel-button":
            self.dismiss(None)