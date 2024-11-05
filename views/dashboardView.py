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
            yield Static(f"{self.website.name}", id="website-name")
            yield Button("Delete", id="Delete", variant="error")


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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            from views.addView import AddView
            add_view = AddView(user=self.user)
            self.app.push_screen(add_view)

    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)