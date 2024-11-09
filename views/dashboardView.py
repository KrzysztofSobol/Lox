from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Input
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from containerService.container import Container as ServiceContainer


class WebsiteItem(Static):
    def __init__(self, website, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.website = website

    def compose(self) -> ComposeResult:
        with Horizontal(id="website-pane"):
            yield Button(f"{self.website.name}", id="website-name", variant="default")
            yield Button("Del", id="Delete", variant="error")


class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    websites = reactive([])
    selected_website = reactive(None)

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
                yield Static("Website details will appear here", id="website-details")
        yield Footer()

    def watch_websites(self, websites: list) -> None:
        container = self.query_one("#left-pane-list")
        container.remove_children()
        for website in websites:
            container.mount(WebsiteItem(website))

    def display_credentials(self, website_id: int) -> None:
        credentials = self.credential_controller.getCredentialsByWebsite(website_id)
        details = self.query_one("#website-details")

        if not credentials:
            details.update("No credentials found for this website")
            return

        credential_text = "Stored Credentials:\n\n"
        for cred in credentials:
            credential_text += f"Username: {cred.username}\n"
            credential_text += f"Password: {cred.encrypted_password}\n\n"

        details.update(credential_text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            from views.addView import AddView
            add_view = AddView(user=self.user)
            self.app.push_screen(add_view)

        else:
            website_item = event.button.parent.parent
            if isinstance(website_item, WebsiteItem):
                if event.button.id == "website-name":
                    self.selected_website = website_item.website
                    self.display_credentials(self.selected_website.id)
                elif event.button.id == "Delete":
                    self.websites = [w for w in self.websites if w.id != website_item.website.id]

    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)