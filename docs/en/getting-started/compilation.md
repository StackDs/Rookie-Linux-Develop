# Compilation and Distribution

## Overview

The project uses **PyInstaller** to generate native single-file executables. The compilation scripts are in the `compile/` folder and output the final result into the `app release/` folder (ignored by git).

---

## Available Scripts

| Script | Platform | Run on |
|---|---|---|
| `compile/build_linux.py` | Linux (native) | Linux |
| `compile/build_windows.py` | Windows (x64) | Linux with Docker or directly on Windows |

---

## Compile for Linux

### Requirements
- Python 3.10+
- pip

### Command

```bash
# From the project root:
python3 compile/build_linux.py
```

The script automatically:
1. Installs `pyinstaller`, `customtkinter` and `pillow` if not present.
2. Runs PyInstaller on `frontend/main.py` with the correct flags.
3. Moves the executable to a temporary folder `Rookie Linux Develop Linux/`.
4. Copies necessary folders: `assets/`, `builder/`, `templates/`, `configs/`, `scripts/`.
5. Creates necessary empty folders: `downloads/iso/`, `output/`, `logs/`.
6. Packages everything into `app release/Rookie Linux Develop Linux.rar` (or `.zip` if `rar` is not installed).
7. Cleans up temporary compilation files.

### Result

```
app release/
└── Rookie Linux Develop Linux.rar
    └── Rookie Linux Develop Linux/
        ├── Rookie-Linux-Builder    ← Executable
        ├── assets/
        ├── builder/
        ├── scripts/
        ├── configs/
        ├── downloads/iso/          ← Empty (filled in use)
        ├── output/                 ← Empty (filled in use)
        └── logs/                   ← Empty (filled in use)
```

---

## Compile for Windows

### Requirements
- Python 3.10+ **on the same Windows machine**

### Command (run on Windows)

```powershell
python compile\build_windows.py
```

The flow is identical to Linux. The result is:

```
app release/
└── Rookie Linux Develop Win x64.rar
    └── Rookie Linux Develop Win x64/
        ├── Rookie-Linux-Builder.exe  ← Executable
        ├── assets/
        ├── builder/
        ├── scripts/
        ├── configs/
        ├── downloads/iso/
        ├── output/
        └── logs/
```

---

## Important PyInstaller Flags

Both scripts use the following critical flags:

```bash
pyinstaller \
  --noconfirm \
  --windowed \                          # No terminal console
  --name "Rookie-Linux-Builder" \
  --hidden-import PIL._tkinter_finder \ # Required for PIL in packaged environments
  --collect-all customtkinter \         # Includes all CustomTkinter assets
  frontend/main.py
```

> ⚠️ **`--hidden-import PIL._tkinter_finder`** is mandatory. Without this flag, images do not load in the packaged executable (silent error on Linux, crash on Windows).

> ⚠️ **`--collect-all customtkinter`** is mandatory. CustomTkinter has JSON theme files and assets that PyInstaller does not automatically detect.

---

## Adding New Dependencies

If you add a new Python library to the project, you must include it in the corresponding compilation script. Add a line to the dependency installation block:

```python
subprocess.run([sys.executable, "-m", "pip", "install", "new-library", ...], check=False)
```

And if PyInstaller doesn't detect it automatically, add the hidden import:

```python
"--hidden-import", "new_library.internal_module",
```

---

## Temporary Compilation Folders

PyInstaller generates `build/` and `dist/` folders during compilation. The `compile/` scripts clean them up automatically upon completion. If the script fails mid-process, you can delete them manually:

```bash
rm -rf build/ dist/ *.spec
```
