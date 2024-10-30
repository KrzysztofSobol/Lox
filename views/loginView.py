from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Static, Input, Button
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
import asyncio

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
    display_state = reactive("normal")  # Can be "normal", "error", "success"
    animation_frame = reactive(0)  # current animation frame

    def render(self) -> str:
        normal_lock = """     
        
                
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

        error_frames = [
            """      
        
               
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@  @@@@@  @@@@@@
         @@@@@@@@  @  @@@@@@@@
         @@@@@@@@@   @@@@@@@@@
         @@@@@@@  @@@  @@@@@@@
         @@@@@  @@@@@@@  @@@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """,
            """      
        
               
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@  @@@@@  @@@@@@@
         @@@@@@@@@  @  @@@@@@@
         @@@@@@@@   @@@@@@@@@@
         @@@@@@@@  @@@  @@@@@@
         @@@@  @@@@@@@  @@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """,
            """      
        
               
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@  @@@@@@  @@@@@@
         @@@@@@@@@@@  @  @@@@@
         @@@@@@@   @@@@@@@@@@@
         @@@@@@@  @@@  @@@@@@@
         @@@@  @@@@@@@@@  @@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """,
            """      
        
               
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@  @@@@@  @@@@@@
         @@@@@@@@  @  @@@@@@@@
         @@@@@@@@@   @@@@@@@@@
         @@@@@@@  @@@  @@@@@@@
         @@@@@  @@@@@@@  @@@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """
        ]

        success_frames = [
            """             
            
            
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@@@@@@  @@@@@
         @@@@@  @@@@@  @@@@@@@
         @@@@@@@  @  @@@@@@@@@
         @@@@@@@@  @@@@@@@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """,
            """             
            
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
                         @@@ 
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@@@@@@  @@@@@
         @@@@@  @@@@@  @@@@@@@
         @@@@@@@  @  @@@@@@@@@
         @@@@@@@@  @@@@@@@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """,
            """             
               +@@@@@@@+
             %@@@@@@@@@@@%
            @@@@:     .@@@@
           @@@@         @@@@
           @@@*         +@@@
           @@@#         *@@@
                         @@@ 
                         @@@ 
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         @@@@@@@@@@@@@@  @@@@@
         @@@@@  @@@@@  @@@@@@@
         @@@@@@@  @  @@@@@@@@@
         @@@@@@@@  @@@@@@@@@@@
         @@@@@@@@@@@@@@@@@@@@@
         #@@@@@@@@@@@@@@@@@@@#
                """
        ]

        if self.display_state == "success":
            return f"[{self.color}]" + success_frames[self.animation_frame]
        elif self.display_state == "error":
            return f"[{self.color}]" + error_frames[self.animation_frame]
        else:
            return f"[{self.color}]" + normal_lock

    async def animateSuccess(self):
        for frame in range(3):
            self.animation_frame = frame
            await asyncio.sleep(0.07)

    async def animateError(self):
        for frame in range(4):
            self.animation_frame = frame
            await asyncio.sleep(0.05)


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

    async def handle_successful_login(self, user):
        lock = self.query_one(LockDisplay)
        lock.color = "#08f26e"
        lock.display_state = "success"

        # Run the animation
        await lock.animateSuccess()
        await asyncio.sleep(0.5) # small break between changing the screen

        # Transition to dashboard
        dashboard = DashboardView(user=user)
        self.app.push_screen(dashboard)

    async def handle_error_login(self):
        lock = self.query_one(LockDisplay)
        lock.color = "red"
        lock.display_state = "error"

        # Run the animation
        await lock.animateError()
        await asyncio.sleep(0.5) # small break between changing the screen

    # button actions
    def on_button_pressed(self, event: Button.Pressed) -> None:
        lock = self.query_one(LockDisplay)
        lrButton = self.query_one("#login-button")

        # Logic for switching to register mode
        if event.button.id == "goToRegister-button":
            lock.color = "white"
            lock.display_state = "normal"
            lock.animation_frame = 0
            self.add_class("register")
            lrButton.label = "Register"
            self.query_one("#goToRegister-text").update(renderable="Go back to login?")

        # Logic for returning to login mode
        elif event.button.id == "goToLogin-button":
            lock.color = "white"
            lock.display_state = "normal"
            lock.animation_frame = 0
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
                asyncio.create_task(self.handle_successful_login(user))
            else:
                asyncio.create_task(self.handle_error_login())