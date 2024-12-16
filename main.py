import subprocess
import sys
import os
import psutil
import time

def read_mode_from_file():
    try:
        with open('mode.txt', 'r') as file:
            mode = file.read().strip().lower()
        return mode == 'true'
    except FileNotFoundError:
        return True
    except Exception as e:
        return True

def close_console_window():
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            exe_path = proc.info.get('exe')
            if exe_path and 'python.exe' in exe_path and 'console_app.py' in exe_path:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    is_gui_mode = read_mode_from_file()

    if is_gui_mode:
        # Launch gui_app.py using python
        subprocess.Popen([sys.executable, 'gui_app.py'], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        # Launch console_app.py using python
        subprocess.Popen([sys.executable, 'console_app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

    close_console_window()

    if not is_gui_mode:
        close_console_window()

    sys.exit(0)

if __name__ == "__main__":
    main()