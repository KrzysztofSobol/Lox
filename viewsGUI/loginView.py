import customtkinter as ctk

from containerService.container import Container
from viewsGUI.mainView import MainScreen


class LoginScreen(ctk.CTkFrame):
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.userController.authenticateUser(username, password)

        if user == 1:
            print("placeholder")
        elif user == 2:
            print("placeholder")
        elif user == 3:
            print("placeholder")
        elif user == 4:
            print("placeholder")
        elif user == 5:
            print("placeholder")
        elif user:
            # Pass the authenticated user to the MainScreen
            main_screen = self.controller.frames[MainScreen]
            main_screen.load_websites(user.id)  # Load websites for this user
            self.controller.show_frame(MainScreen)
            return

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.userController = Container.getUserController()

        # Create a main container frame that will center everything
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Title
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Password Manager",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=(0, 20))

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self.container,
            width=300,
            placeholder_text="Username"
        )
        self.username_entry.pack(pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.container,
            width=300,
            show="*",
            placeholder_text="Password"
        )
        self.password_entry.pack(pady=10)

        # Login Button
        self.login_button = ctk.CTkButton(
            self.container,
            text="Login",
            width=300,
            command=self.login
        )
        self.login_button.pack(pady=20)