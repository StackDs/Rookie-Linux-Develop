# Frontend Screen Structure

Complete map of all application screens, their responsibilities, and the navigation transitions between them.

---

## File Tree

```
frontend/
├── main.py                          Entry point, App class
├── utils.py                         Utility functions (paths, effects)
├── custom_messagebox.py             Modal dialogs system
└── screens/
    ├── core/                        Main navigation screens
    │   ├── start_screen.py
    │   └── option_selection_screen.py
    ├── info_manuals/                Informative and manual screens
    │   ├── info_screen.py
    │   ├── explanation_screen.py
    │   ├── instructions_screen.py
    │   ├── documentation_screen.py
    │   ├── about_screen.py
    │   └── bitlocker_screen.py
    ├── linux_concepts/              Linux educational screens
    │   ├── distro_selection_screen.py
    │   ├── distro_info_screen.py
    │   ├── basic_concepts_screen.py
    │   ├── virtual_machine_screen.py
    │   └── clean_installation_screen.py
    └── installation_tools/          Installation tools screens
        ├── build_progress_screen.py
        ├── usb_flash_screen.py
        ├── wsl_install_screen.py
        ├── wsl_app_install_screen.py
        ├── wsl_main_install_screen.py
        ├── flasher_worker_linux.py
        └── flasher_worker_windows.py
```

---

## Detailed description per screen

### `core/` — Main navigation

#### `StartScreen`
- **Purpose**: Welcome screen with terminal-style typing animation.
- **Navigates to**: `OptionSelectionScreen` ("Start" button)
- **`on_show()`**: Yes — restarts the typing animation if it was already completed.
- **Notes**: Has a blinking cursor effect (`_`) after the text.

#### `OptionSelectionScreen`
- **Purpose**: Main menu with the 7 application options.
- **Navigates to**: All main menu screens.
- **`on_show()`**: No.
- **Notes**: 
  - The WSL button is visually disabled on Linux (`dimmed=True` mode) but is clickable and shows an informative message.
  - Each option has an animated `>` arrow on hover.

---

### `info_manuals/` — Informative screens

#### `InfoScreen`
- **Purpose**: User manual — list of tools included in the ISO.
- **Navigates to**: `OptionSelectionScreen` (← Back)
- **`on_show()`**: Yes — animates the text if it hasn't been animated yet (marks it with `has_animated`).
- **Notes**: Displays content with a typewriter animation.

#### `ExplanationScreen`
- **Purpose**: "About Linux" hub with three routes: Dual Boot, Virtual Machine, Clean Installation.
- **Navigates to**: `BasicConceptsScreen`, `VirtualMachineScreen`, `CleanInstallationScreen`, `OptionSelectionScreen`.
- **`on_show()`**: No.

#### `InstructionsScreen`
- **Purpose**: Step-by-step instructions for using the installation USB.
- **Navigates to**: `OptionSelectionScreen` (← Back)
- **`on_show()`**: No.

#### `DocumentationScreen`
- **Purpose**: Links to official documentation, organized in tabs by category.
- **Navigates to**: `OptionSelectionScreen` (← Back)
- **`on_show()`**: No.
- **Notes**: Uses `ctk.CTkTabview` with 6 tabs: OS and Kernel, Languages, IDEs and Terminal, Databases, Libraries and Frameworks, Office.

#### `AboutScreen`
- **Purpose**: Information about the app, credits, and presentation image.
- **Navigates to**: `OptionSelectionScreen` (← Back)
- **`on_show()`**: No.
- **Notes**: The image supports zooming in a popup window (`CTkToplevel`). The popup uses `root` as the direct parent to avoid hierarchy bugs on Linux with `CTkScrollableFrame`.

#### `BitlockerScreen`
- **Purpose**: Explanation of what BitLocker is and how to disable it before installing Linux.
- **Navigates to**: `CleanInstallationScreen` (← Back)
- **`on_show()`**: No.

---

### `linux_concepts/` — Linux Education

#### `DistroSelectionScreen`
- **Purpose**: Distribution selector via radio buttons.
- **Navigates to**: `DistroInfoScreen` (→ View Details), `OptionSelectionScreen` (← Back)
- **`on_show()`**: No.
- **Shared state**: `self.distro_var` (StringVar) — read by `DistroInfoScreen` and `BuildProgressScreen`.

#### `DistroInfoScreen`
- **Purpose**: Detailed information of the selected distro with screenshots and animated text.
- **Navigates to**: `DistroSelectionScreen` (← Back), `BuildProgressScreen` (Confirm and Generate)
- **`on_show()`**: Yes — loads images and animates text if the distro changed since the last visit.
- **Notes**: Images support zooming. Saves `self.last_distro` to detect changes. Includes a `msg_ask_yes_no` confirmation dialog before initiating the image generation process to prevent unintended downloads.

#### `BasicConceptsScreen`
- **Purpose**: What is Dual Boot. Includes explanatory image.
- **Navigates to**: `ExplanationScreen` (← Back), `VirtualMachineScreen` (Next →)
- **`on_show()`**: No.

#### `VirtualMachineScreen`
- **Purpose**: What is a Virtual Machine. Includes explanatory image.
- **Navigates to**: `BasicConceptsScreen` (← Back), `CleanInstallationScreen` (Next →)
- **`on_show()`**: No.

#### `CleanInstallationScreen`
- **Purpose**: What is a Clean Installation. Includes explanatory image.
- **Navigates to**: `VirtualMachineScreen` (← Back), `BitlockerScreen` (Next →)
- **`on_show()`**: No.

---

### `installation_tools/` — Installation Tools

#### `BuildProgressScreen`
- **Purpose**: Orchestrates ISO download and custom image building.
- **Navigates to**: `DistroInfoScreen` (← Back when finished), `UsbFlashScreen` (button that appears at the end), `OptionSelectionScreen` (upon successful completion)
- **`on_show()`**: Yes — resets state and launches `ejecutar_script()` automatically.
- **Internal state**: Two `ProgressBarManager` (download and generate), reference to current process (`self.current_process`), cancel flag (`self.is_cancelled`).
- **Notes**: This is the most complex screen. Uses threads to avoid blocking the GUI.

#### `UsbFlashScreen`
- **Purpose**: ISO and USB selector, with flashing progress.
- **Navigates to**: `OptionSelectionScreen` (← Back), `OptionSelectionScreen` (upon successful completion)
- **`on_show()`**: Yes — automatically detects connected USBs.
- **Notes**: Launches an elevated worker process (`pkexec` / `RunAs`) to write to disk. Progress is communicated via a temporary JSON file.

#### `WslInstallScreen`
- **Purpose**: WSL installation mode selection menu (Relevant only on Windows).
- **Navigates to**: `OptionSelectionScreen` (← Back), `WslAppInstallScreen` (App Mode), `WslMainInstallScreen` (Main Mode)
- **`on_show()`**: No.

#### `WslAppInstallScreen`
- **Purpose**: Installs a basic WSL subsystem and an auxiliary distribution (Ubuntu) to be able to compile ISO images within the tool.
- **Navigates to**: `OptionSelectionScreen` (← Back)
- **`on_show()`**: Yes — resets installation state.
- **Notes**: Includes confirmation dialogs before requiring administrator permissions. Automatically redirects to the menu upon successful completion.

#### `WslMainInstallScreen`
- **Purpose**: Comprehensive dashboard to install WSL and manage any Linux distribution available in the Microsoft Store as your primary system.
- **Navigates to**: `OptionSelectionScreen` (← Back)
- **`on_show()`**: Yes — asynchronously scans the current WSL status and installed distributions.
- **Notes**: Uses tabs (`CTkTabview`) to separate environment status and distribution management. Features integrated confirmation dialogs.

---

### Workers (not screens)

#### `flasher_worker_linux.py`
- **Purpose**: Separate process with root permissions that cleans the USB and writes the ISO with `dd`.
- **Not a GUI screen** — runs as an elevated subprocess.
- **Communicates progress** via `/tmp/rookie_flash_progress.json`.

#### `flasher_worker_windows.py`
- **Purpose**: Equivalent to the Linux worker for Windows. Uses DISKPART and Windows `dd`.
- **Not a GUI screen** — runs as an elevated subprocess with `RunAs`.

---

## Full Navigation Map

```
StartScreen
    └─[Start]→ OptionSelectionScreen
                   │
                   ├─[User Manual]────────→ InfoScreen
                   │                            └─[Back]→ OptionSelectionScreen
                   │
                   ├─[About Linux]───────────→ ExplanationScreen
                   │                            ├─[Dual Boot]→ BasicConceptsScreen
                   │                            │                  └─[Next]→ VirtualMachineScreen
                   │                            │                                └─[Next]→ CleanInstallationScreen
                   │                            │                                              └─[Next]→ BitlockerScreen
                   │                            ├─[Virtual Mach.]→ VirtualMachineScreen
                   │                            └─[Clean Install]→ CleanInstallationScreen
                   │
                   ├─[Create Image]──────────→ DistroSelectionScreen
                   │                            └─[View Details]→ DistroInfoScreen
                   │                                                  └─[Confirm]→ BuildProgressScreen
                   │                                                                   ├─[Flash USB]→ UsbFlashScreen
                   │                                                                   └─[Success]→ OptionSelectionScreen
                   │
                   ├─[Mount Image]─────────→ UsbFlashScreen
                   │                            └─[Success]→ OptionSelectionScreen
                   │
                   ├─[WSL (Windows)]───────→ WslInstallScreen
                   │                            ├─[App Mode]→ WslAppInstallScreen
                   │                            │                └─[Success/Back]→ OptionSelectionScreen
                   │                            └─[Main Mode]→ WslMainInstallScreen
                   │                                             └─[Back]→ OptionSelectionScreen
                   │ [WSL (Linux)] → Informative popup
                   │
                   ├─[Documentation]───────→ DocumentationScreen
                   │                            └─[Back]→ OptionSelectionScreen
                   │
                   └─[About]───────────────→ AboutScreen
                                                └─[Back]→ OptionSelectionScreen
```
