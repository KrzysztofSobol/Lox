import os
import PyInstaller.__main__
import shutil

shutil.rmtree('dist', ignore_errors=True)
shutil.rmtree('build', ignore_errors=True)

PyInstaller.__main__.run([
    'console_app.py',
    '--onefile',
    '--name=PasswordManager',
    '--add-data=tcss;tcss',
    '--hidden-import=sqlite3',
    '--clean'
])

if os.path.exists('password_manager.db'):
    shutil.copy('password_manager.db', 'dist/password_manager.db')