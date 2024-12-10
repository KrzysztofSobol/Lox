import customtkinter as ctk
from viewsGUI.loginView import LoginScreen
from viewsGUI.mainView import MainScreen

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.geometry("720x480")
        self.title("PasswordManager")
        self.resizable(False, False)

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
        for F in (LoginScreen, MainScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show login screen initially
        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        """Raise the specified frame to the top"""
        frame = self.frames[cont]
        frame.tkraise()

def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()