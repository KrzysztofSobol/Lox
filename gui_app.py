import tkinter as tk  # Add this import
import customtkinter as ctk
from viewsGUI.loginView import LoginScreen
from viewsGUI.mainView import MainScreen
from viewsGUI.addView import AddView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.geometry("720x480")
        self.title("Lox")
        self.resizable(True, True)

        # Configure grid for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a container to hold different frames
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        # Configure grid for the container
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Dictionary to store different screens
        self.frames = {}

        # Create screens
        for F in (LoginScreen, MainScreen, AddView):  # Add AddView here
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show login screen initially
        self.show_frame(LoginScreen)
        self.bind("<Control-l>", self.return_to_login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def return_to_login(self, event=None):
        login_screen = self.frames[LoginScreen]
        login_screen.clear_inputs()
        self.show_frame(LoginScreen)

def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")


    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()