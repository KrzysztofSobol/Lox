import customtkinter as ctk
import os
import sys
import subprocess
import tkinter.messagebox as messagebox
import tkinter as tk

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
        self.is_register_mode = False  # Track current mode

        # Create a background label to hold the image
        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Open the image
        self.background_image = tk.PhotoImage(file="viewsGUI/icons/background.png").subsample(2, 2)

        # Set the background image
        self.background_label.config(image=self.background_image)

        # Rest of the existing __init__ method remains the same...
        # Create a main container frame that will center everything
        self.container = ctk.CTkFrame(self, fg_color="#333333", bg_color="#3e8ad8", border_width=1, border_color="#687eff")
        self.container.place(relx=0.5, rely=0.5, anchor="center")


        # Create a top left frame for Mode button
        self.top_left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_left_frame.pack(side="top", anchor="nw", padx=10, pady=10)

        # Mode Button
        self.mode_button = ctk.CTkButton(
            self.top_left_frame,
            text="Mode",
            width=80,
            fg_color="#687eff",
            bg_color="#133b83",
            hover_color="#4958B3",
            command=self.toggle_mode_window
        )
        self.mode_button.pack()

        # Mode selection frame (initially hidden)
        self.mode_selection_frame = ctk.CTkFrame(self, width=300)

        # Mode Option Menu
        self.mode_option_menu = ctk.CTkOptionMenu(
            self.mode_selection_frame,
            values=["GUI Mode", "Console Mode"],
            width=280,
            fg_color = "#687eff",
            button_color = "#5365CC",
            button_hover_color = "#3E4C99",
            dropdown_fg_color = "#5365CC",
            dropdown_hover_color = "#3E4C99"
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
            fg_color="#687eff",
            hover_color="#4958B3",
            command=lambda: self.save_mode_settings(restart=True)
        )
        self.save_restart_button.pack(side="left", padx=(0, 5))

        # Save Button
        self.save_button = ctk.CTkButton(
            self.mode_buttons_frame,
            text="Save",
            width=140,
            fg_color="#687eff",
            hover_color="#4958B3",
            command=lambda: self.save_mode_settings(restart=False)
        )
        self.save_button.pack(side="left")

        # Title
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Password Manager",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=(20, 20))  # Add more vertical padding

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self.container,
            width=300,
            placeholder_text="Username"
        )
        self.username_entry.pack(pady=10, padx=20)  # Add horizontal padding

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.container,
            width=300,
            show="*",
            placeholder_text="Password"
        )
        self.password_entry.pack(pady=10, padx=20)  # Add horizontal padding

        # Login Button
        self.login_button = ctk.CTkButton(
            self.container,
            text="Login",
            fg_color="#687eff",
            hover_color="#4958B3",
            width=300,
            command=self.login
        )
        self.error_message_label = ctk.CTkLabel(
            self.container,
            text="",
            text_color="#eb5353",
            font=("Helvetica", 13),  # Reduce font size
            height=15,  # Very small height
            width=300
        )
        self.error_message_label.pack(pady=(0, 2), padx=20)  # Minimal padding
        self.login_button.pack(pady=10, padx=20)

        # Adjust switch frame padding
        self.switch_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.switch_frame.pack(pady=(10, 20))

        self.footer_label = ctk.CTkLabel(
            self,
            text="© 2024 Password Manager",
            text_color="gray",
            fg_color="transparent",
            font=("", 10),
            width=self.winfo_screenwidth(),
            corner_radius=0
        )
        self.footer_label.pack(side="bottom", pady=0, fill="x")  # Remove vertical padding and fill horizontally

        # "Don't have an account?" text
        self.switch_text = ctk.CTkLabel(
            self.switch_frame,
            text="Don't have an account?",
            text_color="gray"
        )
        self.switch_text.pack(side="left", pady=10, padx=20)

        # Register/Login switch button
        self.switch_button = ctk.CTkButton(
            self.switch_frame,
            text="Create",
            fg_color="#454a50",
            hover_color="#303438",
            width=100,
            command=self.toggle_register_mode
        )
        self.switch_button.pack(side="left")

        # Confirm Password Entry (initially hidden)
        self.confirm_password_entry = ctk.CTkEntry(
            self.container,
            width=300,
            show="*",
            placeholder_text="Repeat Password"
        )

        # Modify the login button to be toggleable

    def clear_inputs(self):
        """
        Clear username and password input fields
        """
        self.title_label.configure(text_color="#FFFFFF")
        self.container.focus_set()
        self.username_entry.delete(0, 'end')
        self.username_entry.configure(placeholder_text="Username")

        self.password_entry.delete(0, 'end')
        self.password_entry.configure(placeholder_text="Password")

        self.confirm_password_entry.delete(0, 'end')
        self.confirm_password_entry.configure(placeholder_text="Repeat password")

    def error_animation(self):
        animation_texts = [
            "Password Manager  ",
            "Password Manager   ",
            "Password Manager  ",
            "Password Manager",
            "  Password Manager",
            "   Password Manager",
            "  Password Manager",
            "Password Manager",
            "Password Manager ",
            "Password Manager",
            " Password Manager",
            "Password Manager",
        ]

        def animate_text(index=0):
            if index < len(animation_texts):
                self.title_label.configure(text=animation_texts[index], text_color="#eb5353")
                self.after(30, animate_text, index + 1)
        animate_text()

    def success_animation(self):
        self.title_label.configure(text="Password Manager", text_color="#4ebf71")

    def login(self):
        # Clear any previous error messages
        self.error_message_label.configure(text="")

        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.login_button.cget('text') == "Login":
            user = self.userController.authenticateUser(username, password)

            if user == 1:
                self.error_message_label.configure(text="User not found!")
                self.error_animation()
            elif user == 2:
                self.error_message_label.configure(text="Wrong password!")
                self.error_animation()
            elif user:
                self.success_animation()
                self.after(250, lambda: self.switch_to_main_screen(user))
        elif self.login_button.cget('text') == "Register":
            confirm_password = self.confirm_password_entry.get()
            user = self.userController.createUser(username, password, confirm_password)

            if user == 3:
                self.error_message_label.configure(text="User with that name already exists!")
                self.error_animation()
            elif user == 4:
                self.error_message_label.configure(text="Passwords are not the same!")
                self.error_animation()
            elif user == 5:
                self.error_message_label.configure(text="Password should be 5 characters or longer!")
                self.error_animation()
            if user:
                main_screen = self.controller.frames[MainScreen]
                main_screen.load_websites(user.id)
                self.controller.show_frame(MainScreen)
                return

    def switch_to_main_screen(self, user):
        main_screen = self.controller.frames[MainScreen]
        main_screen.load_websites(user.id)
        self.controller.show_frame(MainScreen)

    def toggle_register_mode(self):
        # Clear error message when switching modes
        self.error_message_label.configure(text="")

        if not self.is_register_mode:
            # Switch to Register mode
            self.clear_inputs()
            self.confirm_password_entry.pack(after=self.password_entry, pady=10)
            self.login_button.configure(text="Register")
            self.switch_button.configure(text="Go back")
            self.switch_text.configure(text="Go back to login?")
            self.is_register_mode = True
        else:
            # Switch back to Login mode
            self.clear_inputs()
            self.confirm_password_entry.pack_forget()
            self.login_button.configure(text="Login")
            self.switch_button.configure(text="Create")
            self.switch_text.configure(text="Don't have an account?")
            self.is_register_mode = False
