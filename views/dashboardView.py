from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Switch
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from containerService.container import Container as ServiceContainer

class CredentialItem(Static):
    def __init__(self, username: str, password: str, savedLink: str, url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.savedLink = savedLink
        self.url = url

    def compose(self) -> ComposeResult:
        with Horizontal(classes="credential-row"):
            with Vertical(classes="links-field"):
                yield Static(f"Website: https://www.{self.url}", classes="link-label")
                yield Static(f"Saved link: {self.savedLink}", classes="link-label")
            with Horizontal(classes="credential-field"):
                yield Static(f"Login: {self.username}", classes="credential-label")
                yield Button("copy", classes="copy-button")
                yield Button("edit", classes="edit-button")
            with Horizontal(classes="credential-field"):
                yield Static(f"Password: {self.password}", classes="credential-label")
                yield Button("copy", classes="copy-button")
                yield Button("edit", classes="edit-button")

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
        self.toggle_delete_mode(False)
        leftPane = self.query_one("#left-pane")
        leftPane.border_title = "Websites"

        leftPane = self.query_one("#right-pane")
        leftPane.border_title = "Credentials"

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
                yield Static("Website details will appear here", id="credentials-placehodler")
                yield Static("", id="website-details")
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

    def display_credentials(self, website_id: int, websiteName: str) -> None:
        credentials = self.credential_controller.getCredentialsByWebsite(website_id)

        details = self.query_one("#website-details")
        details.styles.display = "block"
        details.remove_children()

        credentialsPlaceholder = self.query_one("#credentials-placehodler")
        rightPane = self.query_one("#right-pane")

        if not credentials:
            credentialsPlaceholder.styles.display = "block"
            credentialsPlaceholder.update(renderable="No credentials found for this website")
            details.styles.display = "none"
            rightPane.styles.align = ("center", "middle")
            return

        credentialsPlaceholder.styles.display = "none"
        rightPane.styles.align = ("left", "top")

        for cred in credentials:
            details.mount(CredentialItem(cred.username, cred.encrypted_password, cred.saved_link, websiteName))

    def delete_selected_websites(self) -> None:
        to_delete = []
        for website_item in self.query(WebsiteItem):
            if website_item.to_delete:
                to_delete.append(website_item.website.id)

        for website_id in to_delete:
            self.website_controller.delete_website(website_id)

        self.websites = [w for w in self.websites if w.id not in to_delete]
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
                self.display_credentials(self.selected_website.id, self.selected_website.url)

    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)