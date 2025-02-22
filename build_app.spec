# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Helper function to collect all .py files recursively
def collect_py_files(start_path):
    py_files = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

# Get all Python files
py_files = collect_py_files('.')

# Define additional data files
additional_datas = [
    ('mode.txt', '.'),
    ('tcss/*.tcss', 'tcss/'),  # TCSS files
    ('viewsGUI/icons/*', 'viewsGUI/icons/'),  # Icons if any exist
]

a = Analysis(
    ['main.py'],  # Main entry point
    pathex=[os.path.abspath('.')],  # Add current directory to path
    binaries=[],
    datas=additional_datas,
    hiddenimports=[
        'customtkinter',
        'textual',
        'sqlite3',
        'hashlib',
        'base64',
        'cryptography',
        # Controllers
        'controllers.CredentialController',
        'controllers.UserController',
        'controllers.WebsiteController',
        # Models
        'models.*',
        # Repositories
        'repositories.CredentialRepository',
        'repositories.UserRepository',
        'repositories.WebsiteRepository',
        # Utils
        'utils.CryptoUtils',
        'utils.DependencyInjector',
        'utils.ModeController',
        # Views
        'viewsConsole.addView',
        'viewsConsole.dashboardView',
        'viewsConsole.loginView',
        'viewsGUI.addView',
        'viewsGUI.loginView',
        'viewsGUI.mainView',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Lox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False if you want to hide console in GUI mode
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)