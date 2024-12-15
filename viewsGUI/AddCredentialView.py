import customtkinter as ctk

class AddCredentialView(ctk.CTkFrame):
    def __init__(self, parent, controller, on_save):
        super().__init__(parent)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="URL")
        self.url_entry.pack(padx=10, pady=5, fill="x")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(padx=10, pady=5, fill="x")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(padx=10, pady=5, fill="x")

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(padx=10, pady=10, fill="x")

        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side="left", fill="x", expand=True)

        self.save_button = ctk.CTkButton(button_frame, text="Save", command=lambda: self._on_save_click(on_save))
        self.save_button.pack(side="right", fill="x", expand=True)

    def _on_save_click(self, on_save_callback):
        url = self.url_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if on_save_callback:
            on_save_callback(url, username, password)

        self.destroy()