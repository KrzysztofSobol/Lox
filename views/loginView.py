from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Static, Input, Button
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal

from controllers.UserController import UserController
from database.database import init_db
from repositories.UserRepository import UserRepository
from views.dashboardView import DashboardView


class LoginView:
    pass


class LockDisplay(Static):
    SCREENS = {
        "login": LoginView,
    }

    color = reactive("white")

    def render(self) -> str:
        return f"[{self.color}]" + """             
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@#*#@@@@@@@@@
         @@@@@@@. *@* .@@@@@@@
         @@@@@@@@@@@+ -@@@@@@@
         @@@@@@@@@@ :@@@@@@@@@
         @@@@@@@@@@+@@@@@@@@@@
         @@@@@@@@@@=@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """

class LoginView(Screen):
    color = reactive("white")
    CSS_PATH = "../tcss/login.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = init_db()
        self.userRepository = UserRepository(self.conn)
        self.userController = UserController(self.userRepository)

    def compose(self) -> ComposeResult:
        yield LockDisplay(id="lock")
        with Vertical(id="login-container"):
            yield Input(placeholder="Login", id="login-input")
            yield Input(placeholder="Password", id="password-input", password=True)
            yield Input(placeholder="Confirm password", id="confirmPassword-input", password=True)
            yield Button("Login", id="login-button", variant="primary")
            with Horizontal(id="newAcc-container"):
                yield Static("Don't have an account?", id="goToRegister-text")
                yield Button("Create", id="goToRegister-button")
                yield Button("Go back", id="goToLogin-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        lock = self.query_one(LockDisplay)
        lrButton = self.query_one("#login-button")

        # Logic for switching to register mode
        if event.button.id == "goToRegister-button":
            lock.color = "white"
            self.add_class("register")
            lrButton.label = "Register"
            self.query_one("#goToRegister-text").update(renderable="Go back to login?")

        # Logic for returning to login mode
        elif event.button.id == "goToLogin-button":
            lock.color = "white"
            self.remove_class("register")
            lrButton.label = "Login"
            self.query_one("#goToRegister-text").update(renderable="Don't have an account?")


        elif event.button.id == "login-button":

            username = self.query_one("#login-input", Input).value

            password = self.query_one("#password-input", Input).value

            user = None
            if f"{lrButton.label}" == "Login":
                user = self.userController.authenticateUser(username, password)
            else:
                confirmPassword = self.query_one("#confirmPassword-input", Input).value
                user = self.userController.createUser(username, password, confirmPassword)
            if user:
                lock.color = "green"
                dashboard = DashboardView(user=user)
                self.app.push_screen(dashboard)
            else:
                lock.color = "red"