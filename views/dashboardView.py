from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Input, Switch
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from containerService.container import Container as ServiceContainer


class WebsiteItem(Static):
    def __init__(self, website, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.website = website
        self.to_delete = False

    def compose(self) -> ComposeResult:
        with Horizontal(id="website-pane"):
            yield Button(f"{self.website.name}", id="website-name", variant="default")
            yield Switch(animate=False, id="Delete", classes="delete-toggle")

    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "Delete":
            self.to_delete = event.value


class DashboardView(Screen):
    CSS_PATH = "../tcss/dashboard.tcss"

    websites = reactive([])
    selected_website = reactive(None)
    delete_mode = reactive(False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.website_controller = ServiceContainer.getWebsiteController()
        self.credential_controller = ServiceContainer.getCredentialController()

    def on_mount(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)
        # Hide delete toggles and confirmation button initially
        self.toggle_delete_mode(False)

    def compose(self) -> ComposeResult:
        with TextualContainer(id="app-grid"):
            with Vertical(id="left-pane"):
                with Horizontal(id="button-pane"):
                    yield Button("Delete", id="delete-websites-button", variant="error")
                    yield Button("Add", id="add-website-button", variant="success")
                yield Button("I'm sure, delete", id="delete-sure-button", variant="error")
                with VerticalScroll(id="left-pane-list"):
                    pass
            with VerticalScroll(id="right-pane"):
                yield Static("Website details will appear here", id="website-details")
        yield Footer()

    def toggle_delete_mode(self, enabled: bool) -> None:
        self.delete_mode = enabled
        for switch in self.query(".delete-toggle"):
            switch.display = enabled
        sure_button = self.query_one("#delete-sure-button")
        sure_button.display = enabled

        if not enabled:
            for switch in self.query(".delete-toggle"):
                switch.value = False

    def watch_websites(self, websites: list) -> None:
        container = self.query_one("#left-pane-list")
        container.remove_children()
        for website in websites:
            container.mount(WebsiteItem(website))
        self.toggle_delete_mode(self.delete_mode)

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

    def delete_selected_websites(self) -> None:
        # Get all selected websites
        to_delete = []
        for website_item in self.query(WebsiteItem):
            if website_item.to_delete:
                to_delete.append(website_item.website.id)

        # Delete from database
        #for website_id in to_delete:
            #self.website_controller.delete_website(website_id)

        # Update UI
        self.websites = [w for w in self.websites if w.id not in to_delete]
        # Exit delete mode
        self.toggle_delete_mode(False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            from views.addView import AddView
            add_view = AddView(user=self.user)
            self.app.push_screen(add_view)
        elif event.button.id == "delete-websites-button":
            self.toggle_delete_mode(not self.delete_mode)
        elif event.button.id == "delete-sure-button":
            self.delete_selected_websites()
        elif event.button.id == "website-name" and not self.delete_mode:
            website_item = event.button.parent.parent
            if isinstance(website_item, WebsiteItem):
                self.selected_website = website_item.website
                self.display_credentials(self.selected_website.id)

    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)