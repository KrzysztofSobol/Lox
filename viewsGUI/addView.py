import customtkinter as ctk
from containerService.container import Container

class AddView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.credentialController = Container.getCredentialController()
        self.current_user_id = None

        # Center the container on the screen
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create the main container
        self.container = ctk.CTkFrame(self, width=600, height=400, corner_radius=10)
        self.container.grid(row=0, column=0, padx=20, pady=20)

        # URL Input
        self.url_label = ctk.CTkLabel(self.container, text="Website URL")
        self.url_label.pack(padx=10, pady=(20, 2), anchor="w")
        self.url_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="https://example.com",
            width=400
        )
        self.url_entry.pack(padx=10, pady=5, fill="x")

        # Username/Login Input
        self.username_label = ctk.CTkLabel(self.container, text="Login/Username")
        self.username_label.pack(padx=10, pady=(10, 2), anchor="w")
        self.username_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="username or email",
            width=400
        )
        self.username_entry.pack(padx=10, pady=5, fill="x")

        # Password Input
        self.password_label = ctk.CTkLabel(self.container, text="Password")
        self.password_label.pack(padx=10, pady=(10, 2), anchor="w")
        self.password_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Enter password",
            show="*",
            width=400
        )
        self.password_entry.pack(padx=10, pady=5, fill="x")

        # Notification Label
        self.notification_label = ctk.CTkLabel(
            self.container,
            text="",
            text_color="red",
            font=("", 12)
        )
        self.notification_label.pack(padx=10, pady=5)

        # Button Frame
        button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        button_frame.pack(padx=10, pady=10, fill="x")

        # Cancel Button
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel_and_return,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.cancel_button.pack(side="left", padx=5, expand=True, fill="x")

        # Save Button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save_credential,
            fg_color="#00b8d9",
            hover_color="#007d8c"
        )
        self.save_button.pack(side="right", padx=5, expand=True, fill="x")

        self.footer_label = ctk.CTkLabel(
            self,
            text="© 2024 Password Manager",
            text_color="gray",
            font=("", 10)
        )
        self.footer_label.grid(row=2, column=0, columnspan=2, pady=10)

    def set_current_user(self, user_id):
        """
        Set the current user ID when navigating to AddView
        """
        self.current_user_id = user_id

        # Reset entries when navigating to the view
        self.url_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.notification_label.configure(text="")

    def save_credential(self):
        """
        Save the credential and return to MainScreen
        """
        # Reset notification
        self.notification_label.configure(text="")

        # Check if user is logged in
        if not self.current_user_id:
            self.show_notification("No user logged in", is_error=True)
            return

        # Get input values
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate inputs
        if not all([url, username, password]):
            self.show_notification("Please fill in all fields", is_error=True)
            return

        try:
            # Attempt to create credential (which should handle website creation internally)
            credential = self.credentialController.create_credential(
                self.current_user_id,
                url,
                username,
                password
            )

            if credential:
                # Success: Show notification and return to MainScreen
                self.show_notification("Website added successfully!", is_error=False)

                # Refresh the website list in MainScreen
                from viewsGUI.mainView import MainScreen
                main_screen = self.controller.frames[MainScreen]
                main_screen.refresh_website_list()

                # Short delay before returning to main screen to show notification
                self.after(500, self.return_to_main_screen)
            else:
                # Failure in credential creation
                self.show_notification("Failed to add website", is_error=True)

        except Exception as e:
            # Handle any unexpected errors
            self.show_notification(f"Error: {str(e)}", is_error=True)

    def show_notification(self, message, is_error=False):
        """
        Display a notification message
        """
        text_color = "red" if is_error else "green"
        self.notification_label.configure(text=message, text_color=text_color)

    def return_to_main_screen(self):
        """
        Return to MainScreen after a short delay
        """
        # Clear entries
        self.url_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.notification_label.configure(text="")

        # Return to MainScreen
        from viewsGUI.mainView import MainScreen
        self.controller.show_frame(MainScreen)

    def cancel_and_return(self):
        """
        Cancel adding and return to MainScreen
        """
        # Clear all entries
        self.url_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.notification_label.configure(text="")

        # Return to MainScreen
        from viewsGUI.mainView import MainScreen
        self.controller.show_frame(MainScreen)