# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# La raiz del proyecto es un nivel arriba de compile/
# Al compilar, el CWD es la raiz del proyecto
project_root = os.getcwd()
frontend_dir = os.path.join(project_root, 'frontend')

a = Analysis(
    [os.path.join(frontend_dir, 'main.py')],
    pathex=[frontend_dir],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',
        'screens',
        'screens.core',
        'screens.core.start_screen',
        'screens.core.option_selection_screen',
        'screens.info_manuals',
        'screens.info_manuals.info_screen',
        'screens.info_manuals.explanation_screen',
        'screens.info_manuals.about_screen',
        'screens.info_manuals.bitlocker_screen',
        'screens.info_manuals.documentation_screen',
        'screens.info_manuals.instructions_screen',
        'screens.installation_tools',
        'screens.installation_tools.build_progress_screen',
        'screens.installation_tools.usb_flash_screen',
        'screens.installation_tools.wsl_install_screen',
        'screens.installation_tools.flasher_worker_windows',
        'screens.installation_tools.flasher_worker_linux',
        'screens.linux_concepts',
        'screens.linux_concepts.distro_selection_screen',
        'screens.linux_concepts.distro_info_screen',
        'screens.linux_concepts.basic_concepts_screen',
        'screens.linux_concepts.virtual_machine_screen',
        'screens.linux_concepts.clean_installation_screen',
        'utils',
        'custom_messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    collect_all=['customtkinter'],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Rookie-Linux-Builder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'assets', 'Utils', 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Rookie-Linux-Builder',
)
