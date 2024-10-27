from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Static, Input, Button
from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal

from controllers.UserController import UserController
from database.database import init_db
from repositories.UserRepository import UserRepository


class LockDisplay(Static):
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
                yield Static("Don't have an account?", id="newAcc-text")
                yield Button("Create", id="newAcc-button", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "newAcc-button":
            username = self.query_one("#login-input", Input).value
            password = self.query_one("#password-input", Input).value
            confirmPassword = self.query_one("#confirmPassword-input", Input).value
            user = UserController.create_user(self, username, password)
            lock = self.query_one(LockDisplay)
            if(user):
                lock.color = "green"
            else:
                lock.color = "red"

