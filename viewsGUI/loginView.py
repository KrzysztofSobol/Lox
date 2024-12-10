import customtkinter as ctk

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Configure grid layout for the login screen
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.controller = controller  # Store controller reference

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="Password Manager",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(100, 20), sticky="ns")

        # Username entry
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=0, pady=(20, 5), sticky="w", padx=300)

        self.username_entry = ctk.CTkEntry(self, width=400)
        self.username_entry.grid(row=2, column=0, pady=5, sticky="ew", padx=300)

        # Password entry
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=3, column=0, pady=5, sticky="w", padx=300)

        self.password_entry = ctk.CTkEntry(self, show="*", width=400)
        self.password_entry.grid(row=4, column=0, pady=5, sticky="ew", padx=300)

        # Import here to avoid circular import
        from viewsGUI.mainView import MainScreen

        # Login button
        self.login_button = ctk.CTkButton(
            self,
            text="Login",
            width=400,
            command=lambda: self.login()
        )
        self.login_button.grid(row=5, column=0, pady=20, sticky="n")

    def login(self):
        from viewsGUI.mainView import MainScreen

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simple placeholder login
        if username and password:
            self.controller.show_frame(MainScreen)
        else:
            # You might want to add error handling or display a message
            pass