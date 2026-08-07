# Backend Architecture

## Overview

The backend of Rookie Linux Develop is entirely composed of **Bash** scripts that run in a Linux environment (native or via WSL on Windows). The Python frontend acts only as an orchestrator: it launches the scripts, reads their stdout in real-time, and updates the interface with the progress.

---

## File Tree

```
builder/
├── download_iso.sh     Downloads the official ISO for each distro
├── build_iso.sh        Modifies the ISO and injects all content
├── utils.sh            Shared utility functions (log, download_file, etc.)
├── ejecutar.sh         Test/development script to launch the build manually
├── entrypoint.sh       Entry point for Docker containers (legacy Windows mode)
└── templates/
    ├── ubuntu/         Cloud-Init templates for Ubuntu
    ├── mint/           preseed templates for Linux Mint
    ├── fedora/         Kickstart (ks.cfg) for Fedora
    └── popos/          Scripts and configuration for Pop!_OS

scripts/
├── install.sh              Main script that calls all modules
├── verify_installation.sh  Verifies that the installation was successful
├── core/
│   ├── utils.sh            Logging and utility functions
│   ├── update.sh           System update (apt/dnf)
│   └── rookie-verify.sh    Post-installation verification script
├── ide_tools/
│   ├── ide.sh              VSCode, IntelliJ, JetBrains Toolbox
│   ├── editors.sh          Emacs and other editors
│   ├── databases.sh        DBeaver, pgAdmin4
│   └── database_tools.sh   Additional database clients
├── languages/
│   ├── c_cpp.sh            GCC, Clang, Make, CMake, GDB, Valgrind
│   ├── cpp_libraries.sh    SDL2, OpenGL, SFML
│   ├── java.sh             OpenJDK 17/21, Maven
│   ├── python.sh           Python 3, pip, venv, Flake8, IPython
│   ├── node.sh             Node.js LTS, npm
│   ├── dotnet.sh           .NET SDK
│   └── frameworks.sh       Flask, Django, FastAPI, Flutter, Dart
└── system_utils/
    ├── docker.sh           Docker Engine, Docker Compose
    ├── git.sh              Git, GitHub CLI
    ├── terminal.sh         Zsh, Oh-My-Zsh, tmux, fzf, ripgrep
    ├── browsers.sh         Brave, Firefox
    ├── multimedia.sh       OBS Studio, VLC
    ├── extras.sh           JFLAP, various tools
    ├── appearance.sh       Custom wallpaper, visual theme
    └── easter_eggs.sh      Special details and customizations
```

---

## Backend Execution Flow

### Phase 1: Download (`download_iso.sh`)

1. Receives the distro name as an argument (`ubuntu`, `mint`, `fedora`, `popos_nvidia`, etc.).
2. Calls `resolve_iso_source()` which dynamically determines the download URL.
   - **Ubuntu**: Scraping the `releases.ubuntu.com` index to get the latest LTS release.
   - **Mint**: Stable URL based on configurable version and edition.
   - **Fedora**: Scraping the Fedora mirror to get the latest Workstation Live ISO.
   - **Pop!_OS**: Queries the `api.pop-os.org` JSON API to get the correct URL based on variant (generic/nvidia).
3. Downloads the ISO using `wget` or `aria2c` showing percentage to stdout so Python updates the bar.
4. The ISO is saved in `downloads/iso/{distro}/`.

### Phase 2: Build (`build_iso.sh`)

1. **Locates the downloaded ISO** in `downloads/iso/{distro}/`.
2. **Prepares the content to inject**: copies all files from `scripts/` to `/tmp/iso_unpacked/custom_scripts/`.
3. **Copies the wallpaper** from `assets/wallpaper.png` to the temporary folder.
4. **Per distribution**, applies the corresponding automation strategy (see [ISO Creation Flow](./iso-creation-flow.md)).
5. **Repackages the ISO** using `xorriso` with preserved EFI+BIOS boot.
6. Saves the result in `output/{distro}/`.

### Phase 3: First Boot (Post-installation scripts)

The `scripts/` injected into the ISO are executed the first time the system boots on the user's computer. The `install.sh` script acts as the orchestrator, calling all modules in order.

---

## Frontend → Backend Communication

```
frontend/screens/installation_tools/build_progress_screen.py
    │
    ├─ Creates a subprocess.Popen() with the Bash script
    ├─ Reads stdout line by line (char by char for more fluidity)
    ├─ Detects patterns like "XX%" → updates progress bar
    ├─ Detects keywords like "exitosa" (successful) → success signal
    ├─ Detects "[FATAL_ERROR]" → critical error signal
    └─ When the process finishes → shows result popup
```

The Bash script never interacts with the GUI directly. All communication is one-way through `stdout`.

---

## Backend Environment Variables

| Variable | Script | Description |
|----------|--------|-------------|
| `ISO_DISTRO` | `download_iso.sh`, `build_iso.sh` | Target distro (`ubuntu`, `mint`, `fedora`, `popos_nvidia`) |
| `CUSTOM_ISO_NAME` | `build_iso.sh` | Custom name embedded in the final ISO |
| `UBUNTU_VERSION` | `download_iso.sh` | Ubuntu version (default: `24.04`) |
| `MINT_VERSION` | `download_iso.sh` | Mint version (default: `22.1`) |
| `FEDORA_VERSION` | `download_iso.sh` | Fedora version (default: `41`) |
| `POP_VARIANT` | `download_iso.sh` | Pop!_OS variant (`generic` or `nvidia`) |
| `ISO_URL` | `download_iso.sh` | Manual URL to override automatic detection |
| `ISO_NAME` | `download_iso.sh` | Manual filename to override detection |
