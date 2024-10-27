# models/app_state.py
class AppState:
    def __init__(self):
        self.current_screen = "login"

    def set_current_screen(self, screen_name: str):
        self.current_screen = screen_name

    def get_current_screen(self) -> str:
        return self.current_screen