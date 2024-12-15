import subprocess

def read_mode_from_file():
    try:
        with open('mode.txt', 'r') as file:
            mode = file.read().strip().lower()
        return mode == 'true'
    except FileNotFoundError:
        return True
    except Exception as e:
        return True

def main():
    is_gui_mode = read_mode_from_file()

    if is_gui_mode:
        # Launch gui_app.py using pythonw (no console)
        subprocess.run(['pythonw', 'gui_app.py'])
    else:
        # Launch console_app.py using python (with console)
        subprocess.run(['python', 'console_app.py'])

if __name__ == "__main__":
    main()