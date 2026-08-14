# Frontend Architecture

## Overview

The frontend is built in **Python 3** using the **CustomTkinter** (CTk) library, which extends Tkinter with modern widgets and dark mode support. The structure follows a **stacked screens** pattern where all views exist in memory and alternate by raising the active screen to the front with `tkraise()`.

---

## Entry Point: `frontend/main.py`

The `main.py` file contains the main `App` class that inherits from `ctk.CTk` (the root window). Its responsibilities are:

1. **Worker mode detection**: If launched with `--worker-windows` or `--worker-linux`, it executes the USB flasher as an elevated process (administrator) and exits immediately. This avoids having to package a separate executable just for flashing.

2. **Screen initialization**: Instantiates all screen classes in a loop, places them in a stacked grid, and saves references in `self.frames = {}`.

3. **Anti-flickering on Linux**: The main window is hidden with `self.withdraw()` while all screens are created, and is shown with `self.deiconify()` only when everything is ready.

4. **Global navigation**: Exposes the `show_frame(page_name)` method that any screen can call. If the target screen has an `on_show()` method, it is automatically invoked to reset state.

5. **Top banner**: A persistent frame with quick navigation buttons to "Main Menu" and "Start Screen".

### Fatal Error Logger (System Crash Capture)
To prevent silent crashes (especially when running the compiled Windows binary with `--windowed`, where there is no console), `main.py` implements a global logging system before any heavy imports:
- Redirects `sys.stdout` and `sys.stderr` through a proxy class (`_LoggerWriter`) to a local file `rookie_error.log`.
- Overrides `sys.excepthook` and the global Tkinter handler (`tk.Tk.report_callback_exception`) with the `_fatal_error_handler` function, which saves the complete traceback to disk and triggers a critical messagebox (using CustomTkinter/Tkinter) before aborting the process.

---

## Screen Communication Pattern

All screens receive two arguments in their constructor:
- `parent`: the CTk container where they are mounted.
- `controller`: the `App` instance, which acts as a centralized controller.

Any screen can navigate to another like this:
```python
self.controller.show_frame("ScreenName")
```

To read data from another screen (e.g., the selected distro):
```python
distro = self.controller.frames["DistroSelectionScreen"].distro_var.get()
```

---

## Screen Map

```
App (main.py)
│
├── [Global Banner]
│   ├── ⌂ Main Menu  → OptionSelectionScreen
│   └── ⏻ Start Screen → StartScreen
│
└── [Stacked Screens Container]
    │
    ├── core/
    │   ├── StartScreen               Welcome screen with typing animation
    │   └── OptionSelectionScreen     Main menu with 7 options
    │
    ├── info_manuals/
    │   ├── InfoScreen                User manual (list of installed tools)
    │   ├── ExplanationScreen         "About Linux" hub with 3 sub-options
    │   ├── InstructionsScreen        USB/installation usage instructions
    │   ├── DocumentationScreen       Links to official documentation (tabview)
    │   ├── AboutScreen               About the app (image, author info)
    │   └── BitlockerScreen           Explanation and guide to disable BitLocker
    │
    ├── linux_concepts/
    │   ├── BasicConceptsScreen       What is Dual Boot
    │   ├── VirtualMachineScreen      What is a Virtual Machine
    │   ├── CleanInstallationScreen   What is a Clean Installation
    │   ├── DistroSelectionScreen     Distribution selector (radio buttons)
    │   └── DistroInfoScreen          Info + screenshots for each distro
    │
    └── installation_tools/
        ├── BuildProgressScreen       Download + ISO build progress
        ├── UsbFlashScreen            USB selector + flash progress
        ├── WslInstallScreen          WSL installation mode selection menu (Windows only)
        ├── WslAppInstallScreen       WSL Installation (App Mode)
        └── WslMainInstallScreen      WSL installation and distribution management dashboard (Main Mode)
```

---

## Screen Lifecycle

```
1. __init__(parent, controller)
   └── Created once when the app starts.
       Builds all widgets in the layout.

2. on_show()   [Optional]
   └── Called every time the screen becomes visible.
       Use it to reset state, clear fields, or read
       fresh data from other screens.

3. [User Interaction]
   └── Events from buttons, comboboxes, etc.
       Can launch threads (to avoid blocking the GUI).

4. Navigation
   └── self.controller.show_frame("AnotherScreen")
```

---

## Reusable Components

### `custom_messagebox.py`
Modal dialogs system with consistent aesthetics. Exposes:
- `msg_show_info(title, message)` — General information
- `msg_show_error(title, message)` — Error (red)
- `msg_show_warning(title, message)` — Warning (orange)
- `msg_ask_yes_no(title, message)` → `bool` — Confirmation dialog

The modals are centered on screen and are cross-platform (Linux + Windows).

### `utils.py` (frontend)
- `apply_glow_effect(btn, default_text, hover_text)` — Applies a "glow" effect when hovering over buttons.
- `get_project_root()` — Returns the project root path, compatible with normal and packaged (PyInstaller) execution.

### `ProgressBarManager` (in `BuildProgressScreen`)
Abstraction over `ctk.CTkProgressBar` that allows switching between indeterminate mode (pulse animation) and determinate mode (progress bar with percentage) without recreating the widget.

---

## Image Management (PIL/CTkImage)

To display images on the screens, `CTkImage` from CustomTkinter (wrapper over Pillow) is used.

**Critical Rule — Anti-Garbage Collection:**
Python can release a `CTkImage` from memory if no "live" reference points to it. To prevent images from disappearing, a reference is always stored in the widget or the frame that contains it:

```python
ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
lbl = ctk.CTkLabel(parent, image=ctk_img, text="")
lbl.image_ref = ctk_img  # ← Explicit reference to avoid GC
```

For zoom viewers (popup `CTkToplevel` windows):
```python
top.zoomed_img = ctk_img  # ← Attached to the window object
```
