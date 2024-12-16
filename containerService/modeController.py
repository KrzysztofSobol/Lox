# containerService/modeController.py
import os
import sys
import subprocess
import asyncio

class ModeController:
    @staticmethod
    def save_mode(mode):
        try:
            # Get the project root directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            mode_file_path = os.path.join(project_root, 'mode.txt')

            # Write the mode to the file
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

            # Instead of sys.exit(), use subprocess to start the new process
            subprocess.Popen([sys.executable, main_py_path])

            # For Textual apps, we need to cancel all running tasks
            # and close the event loop gracefully
            for task in asyncio.all_tasks():
                task.cancel()

            # Return instead of exiting
            return
        except Exception as e:
            print(f"Error restarting application: {e}")