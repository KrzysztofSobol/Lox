import customtkinter as ctk


class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Store controller reference

        # Configure grid layout for the main screen
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Welcome label
        self.welcome_label = ctk.CTkLabel(
            self,
            text="Welcome to the Password Manager",
            font=("Helvetica", 24, "bold")
        )
        self.welcome_label.grid(row=0, column=0, pady=(100, 20), sticky="ns")

        # Description label
        self.description_label = ctk.CTkLabel(
            self,
            text="Manage your passwords securely",
            font=("Helvetica", 16)
        )
        self.description_label.grid(row=1, column=0, pady=20, sticky="ns")

        # Import here to avoid circular import
        from viewsGUI.loginView import LoginScreen

        # Logout button
        self.logout_button = ctk.CTkButton(
            self,
            text="Logout",
            width=400,
            command=lambda: self.controller.show_frame(LoginScreen)
        )
        self.logout_button.grid(row=2, column=0, pady=20, sticky="n")