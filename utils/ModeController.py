import os
import sys
import subprocess
import asyncio

class ModeController:
    @staticmethod
    def save_mode(mode):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            mode_file_path = os.path.join(project_root, 'mode.txt')

            with open(mode_file_path, 'w') as file:
                file.write(mode)

            return True
        except Exception as e:
            print(f"Error saving mode: {e}")
            return False

    @staticmethod
    def restart_application():
        try:
            # Get the project root directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            main_py_path = os.path.join(project_root, 'main.py')

            subprocess.Popen([sys.executable, main_py_path],
                           creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)

            if 'textual' in sys.modules:
                for task in asyncio.all_tasks():
                    task.cancel()
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.stop()

            sys.exit(0)
        except Exception as e:
            print(f"Error restarting application: {e}")