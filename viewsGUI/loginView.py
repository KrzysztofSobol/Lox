import customtkinter as ctk
import os
import sys
import subprocess
import tkinter.messagebox as messagebox

from containerService.container import Container
from viewsGUI.mainView import MainScreen


class LoginScreen(ctk.CTkFrame):
    def toggle_mode_window(self):
        """
        Toggle the visibility of the mode selection frame
        """
        if self.mode_selection_frame.winfo_viewable():
            self.mode_selection_frame.place_forget()
        else:
            x = self.mode_button.winfo_rootx() - self.winfo_rootx()
            y = self.mode_button.winfo_rooty() - self.winfo_rooty() + self.mode_button.winfo_height()
            self.mode_selection_frame.place(x=x, y=y)

    def save_mode_settings(self, restart=False):
        # Determine the mode based on the option menu selection
        mode = "true" if self.mode_option_menu.get() == "GUI Mode" else "false"

        # Save mode to mode.txt in the project root
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            mode_file_path = os.path.join(project_root, 'mode.txt')

            # Write the mode to the file
            with open(mode_file_path, 'w') as file:
                file.write(mode)

            # Hide the mode selection frame
            self.mode_selection_frame.place_forget()

            # If restart is requested, restart the main application
            if restart:
                # Get the path to main.py
                main_py_path = os.path.join(project_root, 'main.py')

                # Restart the application
                subprocess.Popen([sys.executable, main_py_path])

                # Close the current application
                self.controller.quit()

        except Exception as e:
            # Show an error message if saving fails
            messagebox.showerror("Error", f"Failed to save mode settings: {str(e)}")

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.userController = Container.getUserController()

        # Create a main container frame that will center everything
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Create a top left frame for Mode button
        self.top_left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_left_frame.pack(side="top", anchor="nw", padx=10, pady=10)

        # Mode Button
        self.mode_button = ctk.CTkButton(
            self.top_left_frame,
            text="Mode",
            width=80,
            command=self.toggle_mode_window
        )
        self.mode_button.pack()

        # Mode selection frame (initially hidden)
        self.mode_selection_frame = ctk.CTkFrame(self, width=300)

        # Mode Option Menu
        self.mode_option_menu = ctk.CTkOptionMenu(
            self.mode_selection_frame,
            values=["GUI Mode", "Console Mode"],
            width=280
        )
        # Set initial value to GUI Mode
        self.mode_option_menu.set("GUI Mode")
        self.mode_option_menu.pack(pady=(10, 10))

        # Button frame
        self.mode_buttons_frame = ctk.CTkFrame(self.mode_selection_frame, fg_color="transparent")
        self.mode_buttons_frame.pack(pady=(0, 10))

        # Save and Restart Button
        self.save_restart_button = ctk.CTkButton(
            self.mode_buttons_frame,
            text="Save and Restart",
            width=140,
            command=lambda: self.save_mode_settings(restart=True)
        )
        self.save_restart_button.pack(side="left", padx=(0, 5))

        # Save Button
        self.save_button = ctk.CTkButton(
            self.mode_buttons_frame,
            text="Save",
            width=140,
            command=lambda: self.save_mode_settings(restart=False)
        )
        self.save_button.pack(side="left")

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

        self.footer_label = ctk.CTkLabel(
            self,
            text="© 2024 Password Manager",
            text_color="gray",
            font=("", 10)
        )
        self.footer_label.pack(side="bottom", pady=10)

    def clear_inputs(self):
        """
        Clear username and password input fields
        """
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

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