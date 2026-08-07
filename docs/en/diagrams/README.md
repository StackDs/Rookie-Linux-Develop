# Architecture Diagrams

This folder stores diagrams and visual schematics of the project's architecture.

## General Flow Diagram (text)

```
┌─────────────────────────────────────────────────────────┐
│                    END USER                             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (Python + CustomTkinter)          │
│                                                         │
│  StartScreen → OptionSelectionScreen                    │
│                       │                                 │
│         ┌─────────────┼──────────────┐                 │
│         ▼             ▼              ▼                  │
│  InfoScreens   DistroSelection  UsbFlashScreen          │
│                      │                                  │
│                       ▼                                 │
│               BuildProgressScreen                       │
│                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │ subprocess.Popen() + stdout pipe
                       ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND (Bash scripts)                     │
│                                                         │
│  download_iso.sh ──► Downloads official ISO             │
│                                   │                     │
│                                   ▼                     │
│  build_iso.sh ────► Injects preseed/kickstart           │
│                  ──► Copies scripts/                     │
│                  ──► Repackages with xorriso             │
│                                   │                     │
│                                   ▼                     │
│                     output/{distro}/image.iso           │
└─────────────────────────────────────────────────────────┘
                       │ JSON temporary polling
                       ▼
┌─────────────────────────────────────────────────────────┐
│           FLASHER WORKER (Elevated Process)             │
│                                                         │
│  flasher_worker_linux.py  ──► wipefs + parted + dd      │
│  flasher_worker_windows.py ─► DISKPART + dd             │
│                                                         │
│  Communicates progress via: /tmp/rookie_flash_progress.json │
└─────────────────────────────────────────────────────────┘
```

## Relationship between modules

```
main.py
  └── App (CTk)
        ├── Banner (global buttons)
        └── Container (stacked screens)
              ├── StartScreen
              ├── OptionSelectionScreen
              ├── InfoScreen
              ├── ExplanationScreen
              ├── DistroSelectionScreen ──► distro_var (shared state)
              ├── DistroInfoScreen     ◄─── reads distro_var
              ├── BuildProgressScreen  ◄─── reads distro_var
              │     └── launches: download_iso.sh → build_iso.sh
              ├── UsbFlashScreen
              │     └── launches: flasher_worker_{os}.py (elevated)
              ├── BasicConceptsScreen
              ├── VirtualMachineScreen
              ├── CleanInstallationScreen
              ├── BitlockerScreen
              ├── WslInstallScreen
              ├── InstructionsScreen
              ├── DocumentationScreen
              └── AboutScreen
```

## Adding new diagrams

To add visual diagrams (PNG, SVG, etc.) to this folder, name them descriptively:

- `iso-flow-ubuntu.png` — Specific flow for Ubuntu
- `general-architecture.svg` — SVG diagram of the full architecture
- `screen-navigation.png` — Screenshot of the navigation map
