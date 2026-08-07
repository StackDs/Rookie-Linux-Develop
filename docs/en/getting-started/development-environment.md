# Development Environment

## Prerequisites

| Requirement | Minimum Version | Installation |
|---|---|---|
| Python | 3.10+ | `sudo apt install python3` |
| pip | Included with Python | — |
| Git | Any | `sudo apt install git` |
| Tkinter | Included with Python | `sudo apt install python3-tk` |

> **On Windows**: Python 3.10+ from [python.org](https://www.python.org/downloads/) is required, along with WSL installed for the ISO building part.

---

## Clone the repository

```bash
git clone https://github.com/your-username/Rookie-Linux-Develop.git
cd Rookie-Linux-Develop
```

---

## Install Python dependencies

```bash
pip install customtkinter pillow
```

Or if you use a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install customtkinter pillow
```

---

## Run the application

The application must be launched from the **project root** because `utils.get_project_root()` determines the root path using the relative position of `main.py`:

```bash
# From the project root:
python3 frontend/main.py
```

> ⚠️ **Do not run from inside `frontend/`**. Paths to `assets/`, `builder/`, and `scripts/` are calculated relative to the project root.

---

## Structure you need to know

```
Rookie-Linux-Develop/
├── frontend/
│   ├── main.py              ← GUI entry point
│   ├── utils.py             ← Utilities (paths, visual effects)
│   ├── custom_messagebox.py ← Modal dialogs system
│   └── screens/             ← All application screens
├── assets/                  ← Images, wallpaper, icon
├── builder/                 ← Download and build scripts
├── scripts/                 ← Post-boot installation scripts
├── configs/                 ← Global configuration (optional)
├── downloads/iso/           ← Downloaded ISOs (ignored by git)
├── output/                  ← Generated ISOs (ignored by git)
└── logs/                    ← Logs (ignored by git)
```

---

## Verify everything works

When launching `frontend/main.py`, the application window should appear with:
- Black terminal-style background
- Top banner with "⌂ Main Menu" and "Start Screen ⏻"
- Welcome screen with text typing animation

If an import error appears, verify:

```bash
python3 -c "import customtkinter; print('OK')"
python3 -c "from PIL import Image; print('OK')"
python3 -c "import tkinter; print('OK')"
```

---

## Common Issues

### `No module named 'tkinter'`
```bash
sudo apt install python3-tk
```

### Images not displaying
Verify they exist in `assets/`:
```bash
ls assets/
# Should contain: welcome.jpg, dualboot.jpg, bitlocker.jpg, maquinaVirtual.jpg, onlyLinux.jpg
```

### Window appears in a corner or empty (Linux)
This is a window manager mapping issue. The `withdraw/deiconify` mechanism already mitigates this; if it persists, try running with another window manager or update CustomTkinter:
```bash
pip install --upgrade customtkinter
```

---

## Add a new screen (quick summary)

1. Create `frontend/screens/category/my_screen.py` with a class inheriting from `ctk.CTkFrame`.
2. In `frontend/main.py`, import the class and add it to the frame initialization loop.
3. Navigate to it with `self.controller.show_frame("MyScreen")`.

Check the [complete screen guide](../reference/screen-structure.md) for more details.
