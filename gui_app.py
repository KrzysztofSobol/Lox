import customtkinter as ctk

def run_gui():
    app = ctk.CTk()
    app.geometry("720x480")
    app.title("PasswordManager")
    app.resizable(False, False)
    # Add your GUI components here
    app.mainloop()

def main():
    run_gui()

if __name__ == "__main__":
    main()
