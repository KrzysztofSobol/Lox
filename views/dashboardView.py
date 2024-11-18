from textual import log
from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.css.query import NoMatches
from textual.widgets import Static, Footer, Button, Switch, Input
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from containerService.container import Container as ServiceContainer
import pyperclip

website_controller = ServiceContainer.getWebsiteController()
credential_controller = ServiceContainer.getCredentialController()

class CredentialItem(Static):
    username = reactive("")
    password = reactive("")

    def __init__(self, credential_id: int, username: str, password: str, savedLink: str, url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credential_id = credential_id
        self.username = username
        self.password = password
        self.savedLink = savedLink
        self.url = url

    def compose(self) -> ComposeResult:
        with Vertical(id="row", classes="credential-row"):
            with Horizontal(classes="credential-field-top"):
                with Horizontal(classes="links-field"):
                    yield Static(f"Saved link:", classes="saved-link")
                    yield Static(f" {self.savedLink}", classes="link-label")
                yield Button("edit", id="edit-credential-button", classes="edit-button")
                yield Button("delete", id="delete-credential-button")
                yield Button("cancel", id="delete-cancel-credential-button")
                yield Button("done", id="edit-confirm-credential-button", variant="success")
            with Horizontal(classes="credential-field-top"):
                yield Static("click to copy login/password", classes="copy-text")
                yield Button("sure??", id="delete-sure-credential-button")
            with Vertical(classes="credential-field"):
                with Horizontal(classes="loginAndPassword-field"):
                    yield Static("Login:    ", classes="saved-link")
                    yield Button(f"{self.username}", id="copy-button-login", classes="credential-label")
                    yield Input(placeholder=f"{self.username}", id="edit-input-login", classes="edit-input")
                with Horizontal(classes="loginAndPassword-field"):
                    yield Static("Password: ", classes="saved-link")
                    yield Button(f"{self.password}", id="copy-button-password", classes="credential-label")
                    yield Input(placeholder=f"{self.password}", id="edit-input-password", classes="edit-input")

    async def on_mount(self) -> None:
        self.watch_username(self.username)
        self.watch_password(self.password)

    def watch_username(self, value: str) -> None:
        try:
            self.query_one("#copy-button-login").label = value
            self.query_one("#edit-input-login").placeholder = value
        except NoMatches as e:
            log(f"Error in watch_username: {e}")

    def watch_password(self, value: str) -> None:
        try:
            self.query_one("#copy-button-password").label = value
            self.query_one("#edit-input-password").placeholder = value
        except NoMatches as e:
            log(f"Error in watch_password: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        deleteButton = self.query_one("#delete-credential-button")
        deleteCancelButton = self.query_one("#delete-cancel-credential-button")
        deleteSureButton = self.query_one("#delete-sure-credential-button")
        loginButton = self.query_one("#copy-button-login")
        passwordButton = self.query_one("#copy-button-password")
        loginEditInput = self.query_one("#edit-input-login")
        passwordEditInput = self.query_one("#edit-input-password")
        editButton = self.query_one("#edit-credential-button")
        editCancelButton = self.query_one("#edit-confirm-credential-button")
        credentialRow = self.query_one("#row")

        if event.button.id == "copy-button-login" or event.button.id == "copy-button-password":
            pyperclip.copy(event.button.label)
        elif event.button.id == "edit-credential-button":
            loginButton.display = False
            passwordButton.display = False
            loginEditInput.display = True
            passwordEditInput.display = True
            editButton.display = False
            editCancelButton.display = True
            deleteButton.display = True
            deleteCancelButton.display = False
            deleteSureButton.display = False

            credentialRow.styles.border = ("round", "#F9D923")
        if event.button.id == "edit-confirm-credential-button":
            new_username = self.query_one("#edit-input-login").value
            new_password = self.query_one("#edit-input-password").value

            success = credential_controller.edit(
                credential_id=self.credential_id,
                username=new_username,
                password=new_password
            )

            if success:
                self.username = success.username
                self.password = success.password

            loginButton.display = True
            passwordButton.display = True
            loginEditInput.display = False
            passwordEditInput.display = False
            editCancelButton.display = False
            editButton.display = True
            credentialRow.styles.border = ("round", "#80B3FF")
        elif event.button.id == "delete-credential-button":
            deleteButton.display = False
            deleteCancelButton.display = True
            deleteSureButton.display = True
            editCancelButton.display = False
            editButton.display = True
            credentialRow.styles.border = ("round", "#EB5353")
        elif event.button.id == "delete-cancel-credential-button":
            deleteButton.display = True
            deleteCancelButton.display = False
            deleteSureButton.display = False
            credentialRow.styles.border = ("round", "#80B3FF")
        elif event.button.id == "delete-sure-credential-button":
            if credential_controller.delete(self.credential_id):
                self.remove()
            deleteButton.display = True
            deleteCancelButton.display = False
            deleteSureButton.display = False

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

    search_query = reactive("")
    websites = reactive([])
    credentials = reactive([])
    selected_website = reactive(None)
    delete_mode = reactive(False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def on_mount(self) -> None:
        if self.user:
            self.websites = website_controller.get_user_websites(self.user.id)
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
                        yield Button("Add credential", id="add-website-button", variant="success")
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

    def refresh_credentials(self) -> None:
        if self.selected_website:
            self.credentials = credential_controller.getCredentialsByWebsite(self.selected_website.id)

    def delete_selected_websites(self) -> None:
        to_delete = []
        for website_item in self.query(WebsiteItem):
            if website_item.to_delete:
                to_delete.append(website_item.website.id)

        for website_id in to_delete:
            website_controller.delete_website(website_id)

        self.websites = [w for w in self.websites if w.id not in to_delete]
        self.toggle_delete_website_mode(False)

    # ------------ Watch functions ------------
    def watch_search_query(self, query: str) -> None:
        filtered_websites = [
            website for website in website_controller.get_user_websites(self.user.id)
            if query.lower() in website.name.lower()
        ]
        self.websites = filtered_websites

    def watch_credentials(self, credentials: list) -> None:
        details = self.query_one("#website-details")
        credentialsPlaceholder = self.query_one("#credentials-placehodler")
        rightPane = self.query_one("#right-pane")

        # Show placeholder if no credentials exist
        if not credentials:
            credentialsPlaceholder.styles.display = "block"
            credentialsPlaceholder.update(renderable="No credentials found for this website")
            details.styles.display = "none"
            rightPane.styles.align = ("center", "middle")
            return

        # Otherwise, update UI
        credentialsPlaceholder.styles.display = "none"
        details.styles.display = "block"
        rightPane.styles.align = ("left", "top")

        # Get current credential IDs
        current_credential_ids = {item.credential_id for item in self.query(CredentialItem)}
        new_credential_ids = {cred.id for cred in credentials}

        # Remove credentials no longer present
        for item in self.query(CredentialItem):
            if item.credential_id not in new_credential_ids:
                item.remove()

        # Add new credentials
        for cred in credentials:
            if cred.id not in current_credential_ids:
                details.mount(CredentialItem(
                    credential_id=cred.id,
                    username=cred.username,
                    password=cred.password,
                    savedLink=cred.saved_link,
                    url=self.selected_website.url if self.selected_website else ""
                ))

    def watch_websites(self, websites: list) -> None:
        container = self.query_one("#left-pane-list")

        # Get the current set of websites in the container
        current_website_ids = {item.website.id for item in self.query(WebsiteItem)}
        new_website_ids = {website.id for website in websites}

        # Remove websites that are no longer present
        for item in self.query(WebsiteItem):
            if item.website.id not in new_website_ids:
                item.remove()

        # Add new websites
        for website in websites:
            if website.id not in current_website_ids:
                container.mount(WebsiteItem(website))

        # Optionally update existing website items if needed
        self.toggle_delete_website_mode(self.delete_mode)

    # ------------ Listeners ------------
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search-input":
            self.search_query = event.input.value

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

    # ------------ On resume ------------
    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = website_controller.get_user_websites(self.user.id)
            if self.selected_website:
                self.refresh_credentials()