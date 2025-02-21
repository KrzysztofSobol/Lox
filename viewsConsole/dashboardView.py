from textual import log
from textual.app import Screen, ComposeResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.css.query import NoMatches
from textual.widgets import Static, Footer, Button, Switch, Input
from textual.containers import Container as TextualContainer
from textual.reactive import reactive
from utils.DependencyInjector import Injector as ServiceInjector
import pyperclip

website_controller = ServiceInjector.getWebsiteController()
credential_controller = ServiceInjector.getCredentialController()

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
        # Get UI elements
        elements = {
            "row": self.query_one("#row"),
            "login_button": self.query_one("#copy-button-login"),
            "password_button": self.query_one("#copy-button-password"),
            "login_input": self.query_one("#edit-input-login"),
            "password_input": self.query_one("#edit-input-password"),
            "edit_button": self.query_one("#edit-credential-button"),
            "edit_confirm_button": self.query_one("#edit-confirm-credential-button"),
            "delete_button": self.query_one("#delete-credential-button"),
            "delete_cancel_button": self.query_one("#delete-cancel-credential-button"),
            "delete_confirm_button": self.query_one("#delete-sure-credential-button"),
        }

        button_id = event.button.id

        # Copy to clipboard
        if button_id in ["copy-button-login", "copy-button-password"]:
            pyperclip.copy(event.button.label)
            return

        # Handle edit mode
        if button_id == "edit-credential-button":
            self._set_edit_mode(elements, True)

        # Handle edit confirmation
        elif button_id == "edit-confirm-credential-button":
            new_username = elements["login_input"].value
            new_password = elements["password_input"].value

            success = credential_controller.edit(
                credential_id=self.credential_id,
                username=new_username,
                password=new_password
            )

            if success:
                self.username = success.decrypted_username
                self.password = success.decrypted_password

            self._set_edit_mode(elements, False)

        # Handle delete button
        elif button_id == "delete-credential-button":
            self._set_delete_mode(elements, True)

        # Handle delete cancellation
        elif button_id == "delete-cancel-credential-button":
            self._set_delete_mode(elements, False)

        # Handle delete confirmation
        elif button_id == "delete-sure-credential-button":
            if credential_controller.delete(self.credential_id):
                self.remove()
                dashboard_view = self.screen
                dashboard_view.refresh_credentials()
            self._set_delete_mode(elements, False)

    def _set_edit_mode(self, elements, enable: bool):
        if enable:
            # Enable edit mode
            elements["login_button"].display = False
            elements["password_button"].display = False
            elements["login_input"].display = True
            elements["password_input"].display = True
            elements["edit_button"].display = False
            elements["edit_confirm_button"].display = True
            elements["delete_button"].display = True
            elements["delete_cancel_button"].display = False
            elements["delete_confirm_button"].display = False
            elements["row"].styles.border = ("round", "#F9D923")  # Yellow for edit
        else:
            # Disable edit mode (back to normal)
            elements["login_button"].display = True
            elements["password_button"].display = True
            elements["login_input"].display = False
            elements["password_input"].display = False
            elements["edit_confirm_button"].display = False
            elements["edit_button"].display = True
            elements["row"].styles.border = ("round", "#80B3FF")  # Blue for normal

    def _set_delete_mode(self, elements, enable: bool):
        """Set the UI to delete confirmation mode or normal mode"""
        if enable:
            # Enable delete confirmation mode
            elements["login_button"].display = True
            elements["password_button"].display = True
            elements["login_input"].display = False
            elements["password_input"].display = False
            elements["delete_button"].display = False
            elements["delete_cancel_button"].display = True
            elements["delete_confirm_button"].display = True
            elements["edit_confirm_button"].display = False
            elements["edit_button"].display = True
            elements["row"].styles.border = ("round", "#EB5353")  # Red for delete
        else:
            # Disable delete confirmation mode (back to normal)
            elements["delete_button"].display = True
            elements["delete_cancel_button"].display = False
            elements["delete_confirm_button"].display = False
            elements["row"].styles.border = ("round", "#80B3FF")  # Blue for normal

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
    last_clicked_button = None

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

        if not credentials:
            credentialsPlaceholder.styles.display = "block"
            credentialsPlaceholder.update(renderable="No credentials found for this website")
            details.styles.display = "none"
            rightPane.styles.align = ("center", "middle")
            return

        credentialsPlaceholder.styles.display = "none"
        details.styles.display = "block"
        rightPane.styles.align = ("left", "top")

        current_credential_ids = {item.credential_id for item in self.query(CredentialItem)}
        new_credential_ids = {cred.id for cred in credentials}

        for item in self.query(CredentialItem):
            if item.credential_id not in new_credential_ids:
                item.remove()

        for cred in credentials:
            if cred.id not in current_credential_ids:
                details.mount(CredentialItem(
                    credential_id=cred.id,
                    username=cred.decrypted_username,
                    password=cred.decrypted_password,
                    savedLink=cred.decrypted_saved_link,
                    url=self.selected_website.url if self.selected_website else ""
                ))

    def watch_websites(self, websites: list) -> None:
        container = self.query_one("#left-pane-list")

        if self.selected_website:
            if self.last_clicked_button:
                self.last_clicked_button.styles.border_top = ("tall", "#454a50")
                self.last_clicked_button.styles.border_bottom = ("tall", "#000000")

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

    # ------------ Listeners ------------
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search-input":
            self.search_query = event.input.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-website-button":
            def handle_added_website(website_id: int | None) -> None:
                if website_id is not None:
                    self.websites = website_controller.get_user_websites(self.user.id)
                    for website in self.websites:
                        if website.id == website_id:
                            self.selected_website = website
                            self.refresh_credentials()
                            break
            from viewsConsole.addView import AddView
            add_view = AddView(user=self.user)
            self.app.push_screen(add_view, handle_added_website)
        elif event.button.id == "delete-websites-button":
            self.toggle_delete_website_mode(not self.delete_mode)
        elif event.button.id == "delete-sure-website-button":
            self.delete_selected_websites()
            self.refresh_credentials()
        elif event.button.id == "website-name" and not self.delete_mode:
            website_item = event.button.parent.parent
            if isinstance(website_item, WebsiteItem):
                if self.last_clicked_button:
                    self.last_clicked_button.styles.border_top = ("tall", "#454a50")
                    self.last_clicked_button.styles.border_bottom = ("tall", "#000000")
                event.button.styles.border_top = ("tall", "#80B3FF")
                event.button.styles.border_bottom = ("tall", "#3485ff")
                self.last_clicked_button = event.button
                self.selected_website = website_item.website
                self.refresh_credentials()

    # ------------ On resume ------------
    def on_screen_resume(self) -> None:
        if self.user:
            self.websites = website_controller.get_user_websites(self.user.id)
            if self.selected_website:
                self.refresh_credentials()