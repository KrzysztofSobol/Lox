from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Static, Footer, Button, Switch, Input
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from containerService.container import Container as ServiceContainer
from textual.message import Message
import pyperclip

class CredentialItem(Static):
    class DeleteCredential(Message):
        def __init__(self, credential_id: int):
            super().__init__()
            self.credential_id = credential_id

    def __init__(self, credential_id: int, username: str, password: str, savedLink: str, url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credential_id = credential_id
        self.username = username
        self.password = password
        self.savedLink = savedLink
        self.url = url

    def compose(self) -> ComposeResult:
        with Horizontal(classes="credential-row"):
            with Horizontal(classes="credential-field-top"):
                with Horizontal(classes="links-field"):
                    yield Static(f"Saved link:", classes="saved-link")
                    yield Static(f" {self.savedLink}", classes="link-label")
                yield Button("edit", classes="edit-button")
                yield Button("delete", id="delete-credential-button")
                yield Button("sure??", id="delete-sure-credential-button", classes="hidden")
            yield Static("click to copy", classes="copy-text")
            with Vertical(classes="credential-field"):
                with Horizontal(classes="loginAndPassword-field"):
                    yield Static("Login:    ", classes="saved-link")
                    yield Button(f"{self.username}", id="copy-button", classes="credential-label")
                with Horizontal(classes="loginAndPassword-field"):
                    yield Static("Password: ", classes="saved-link")
                    yield Button(f"{self.password}", id="copy-button", classes="credential-label")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        deleteButton = self.query_one("#delete-credential-button")
        sureButton = self.query_one("#delete-sure-credential-button")

        if event.button.id == "delete-credential-button":
            deleteButton.display = False
            sureButton.display = True
        elif event.button.id == "delete-sure-credential-button":
            # Post the DeleteCredential message to be handled by the DashboardView
            self.post_message(self.DeleteCredential(self.credential_id))
            # Reset button state
            deleteButton.display = True
            sureButton.display = False

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
    credentials = reactive([])
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
        self.toggle_delete_website_mode(False)
        leftPane = self.query_one("#left-pane")
        leftPane.border_title = "Websites"

        leftPane = self.query_one("#right-pane")
        leftPane.border_title = "Credentials"

    def compose(self) -> ComposeResult:
        with TextualContainer(id="app-grid"):
            with Vertical(id="left-pane"):
                with Vertical(id="button-pane"):
                    with Horizontal(id="button-pane-del-add"):
                        yield Button("Delete website", id="delete-websites-button", variant="error")
                        yield Button("Add website", id="add-website-button", variant="success")
                        yield Button("I'm sure, delete", id="delete-sure-website-button", variant="error")
                    yield Input(placeholder="Search", id="search-input")
                with VerticalScroll(id="left-pane-list"):
                    pass
            with VerticalScroll(id="right-pane"):
                yield Static("Website details will appear here", id="credentials-placehodler")
                yield Static("", id="website-details")
        yield Footer()

    def toggle_delete_website_mode(self, enabled: bool) -> None:
        self.delete_mode = enabled
        for switch in self.query(".delete-toggle"):
            switch.display = enabled
        sure_button = self.query_one("#delete-sure-website-button")
        sure_button.display = enabled

        if not enabled:
            for switch in self.query(".delete-toggle"):
                switch.value = False

    def watch_credentials(self, credentials: list) -> None:
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
            details.mount(CredentialItem(
                credential_id=cred.id,
                username=cred.username,
                password=cred.encrypted_password,
                savedLink=cred.saved_link,
                url=self.selected_website.url if self.selected_website else ""
            ))

    def delete_credential(self, credential_id: int) -> None:
        self.credential_controller.delete(credential_id)
        self.credentials = [cred for cred in self.credentials if cred.id != credential_id]

    def on_credential_item_delete_credential(self, message: CredentialItem.DeleteCredential) -> None:
        self.delete_credential(message.credential_id)

    def refresh_credentials(self) -> None:
        if self.selected_website:
            self.credentials = self.credential_controller.getCredentialsByWebsite(self.selected_website.id)

    def display_credentials(self, website_id: int, websiteName: str) -> None:
        self.credentials = self.credential_controller.getCredentialsByWebsite(website_id)

    def watch_websites(self, websites: list) -> None:
        container = self.query_one("#left-pane-list")
        container.remove_children()
        for website in websites:
            container.mount(WebsiteItem(website))
        self.toggle_delete_website_mode(self.delete_mode)

    def delete_selected_websites(self) -> None:
        to_delete = []
        for website_item in self.query(WebsiteItem):
            if website_item.to_delete:
                to_delete.append(website_item.website.id)

        for website_id in to_delete:
            self.website_controller.delete_website(website_id)

        self.websites = [w for w in self.websites if w.id not in to_delete]
        self.toggle_delete_website_mode(False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            from views.addView import AddView
            add_view = AddView(user=self.user)
            self.app.push_screen(add_view)
        elif event.button.id == "delete-websites-button":
            self.toggle_delete_website_mode(not self.delete_mode)
        elif event.button.id == "delete-sure-website-button":
            self.delete_selected_websites()
        elif event.button.id == "website-name" and not self.delete_mode:
            website_item = event.button.parent.parent
            if isinstance(website_item, WebsiteItem):
                self.selected_website = website_item.website
                self.refresh_credentials()
        elif event.button.id == "copy-button":
            pyperclip.copy(event.button.label)

    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = self.website_controller.get_user_websites(self.user.id)
            if self.selected_website:
                self.refresh_credentials()