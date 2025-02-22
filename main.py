import subprocess
import sys
import os
import psutil
import time

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def read_mode_from_file():
    try:
        mode_path = get_resource_path('mode.txt')
        with open(mode_path, 'r') as file:
            mode = file.read().strip().lower()
        return mode == 'true'
    except FileNotFoundError:
        return True
    except Exception as e:
        return True

def close_console_window():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == 'your_app_name.exe':
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    is_gui_mode = read_mode_from_file()

    if is_gui_mode:
        from gui_app import main as gui_main
        gui_main()
    else:
        from console_app import ModesApp
        app = ModesApp()
        app.run()

    sys.exit(0)

if __name__ == "__main__":
    main()