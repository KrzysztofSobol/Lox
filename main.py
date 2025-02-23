import subprocess
import sys
import os
import time

def read_mode_from_file():
    try:
        with open('mode.txt', 'r') as file:
            mode = file.read().strip().lower()
        return mode == 'true'
    except FileNotFoundError:
        return True  # Default to GUI mode if file doesn't exist
    except Exception as e:
        print(f"Error reading mode file: {e}")
        return True

def main():
    is_gui_mode = read_mode_from_file()

    if is_gui_mode:
        # Launch gui_app.py (CustomTkinter) in a new process, detached from the console
        subprocess.Popen([sys.executable, 'gui_app.py'],
                        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        # Launch console_app.py (Textual) in a new console window
        subprocess.Popen([sys.executable, 'console_app.py'],
                        creationflags=subprocess.CREATE_NEW_CONSOLE)

    # mall delay for the new process to start before exiting
    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    main()