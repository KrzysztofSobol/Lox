import customtkinter as ctk
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class PasswordManager(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    isGUI = True
    with open('boolean.txt', 'r') as file:
        isGUI = file.read().strip()
    isGUI = True if isGUI == "True" else False

    if(isGUI):
        appGUI = ctk.CTk()
        appGUI.geometry("720x480")
        appGUI.title("PasswordManager")
        appGUI.resizable(False, False)
        appGUI.mainloop()
    else:
        appText = PasswordManager()
        appText.run()