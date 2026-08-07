# Script Catalog

Complete list of all software that is automatically installed on the first boot of the generated Linux system.

---

## Languages and Compilers

### C / C++
**File:** `scripts/languages/c_cpp.sh`

| Tool | Description |
|---|---|
| `gcc` | C Compiler (GNU Compiler Collection) |
| `g++` | C++ Compiler |
| `clang` | Alternative C/C++ compiler (LLVM) |
| `make` | Build automation tool |
| `cmake` | Cross-platform build configuration system |
| `gdb` | GNU Debugger |
| `valgrind` | Memory analyzer and profiler |

### C++ Graphics Libraries
**File:** `scripts/languages/cpp_libraries.sh`

| Library | Description |
|---|---|
| `libsdl2-dev` | SDL2 — 2D Graphics, audio, input |
| `libglfw3-dev` | GLFW — OpenGL contexts and windows |
| `libglew-dev` | GLEW — OpenGL extensions |
| `libsfml-dev` | SFML — 2D Multimedia in C++ |
| `mesa-utils` | OpenGL/Mesa utilities |

### Java
**File:** `scripts/languages/java.sh`

| Tool | Description |
|---|---|
| `openjdk-17-jdk` | OpenJDK 17 LTS |
| `openjdk-21-jdk` | OpenJDK 21 LTS |
| `maven` | Java project and dependency management |

### Python
**File:** `scripts/languages/python.sh`

| Tool | Description |
|---|---|
| `python3` | Python 3 (latest repository version) |
| `python3-pip` | pip package manager |
| `python3-venv` | Virtual environment support |
| `flake8` | Python code linter (PEP 8) |
| `ipython` | Enhanced interactive Python shell |

### Node.js / JavaScript
**File:** `scripts/languages/node.sh`

| Tool | Description |
|---|---|
| `nodejs` (LTS) | Node.js (installed via NodeSource) |
| `npm` | Node package manager |
| `typescript` | TypeScript (installed globally via npm) |

### .NET / C#
**File:** `scripts/languages/dotnet.sh`

| Tool | Description |
|---|---|
| `.NET SDK` | Full Microsoft .NET SDK (latest LTS) |

### Web and Mobile Frameworks
**File:** `scripts/languages/frameworks.sh`

| Framework | Ecosystem | Description |
|---|---|---|
| Flask | Python | Web microframework |
| Django | Python | Full web framework |
| FastAPI | Python | Modern and fast REST API |
| Flutter SDK | Dart | Cross-platform UI framework |
| Dart SDK | Dart | Flutter language |

---

## IDEs and Editors

### Main IDEs
**File:** `scripts/ide_tools/ide.sh`

| Tool | Description | Installation |
|---|---|---|
| Visual Studio Code | Microsoft editor | Official Microsoft repository |
| IntelliJ IDEA CE | JetBrains Java/Kotlin IDE | JetBrains Toolbox or `.tar.gz` |
| JetBrains Toolbox | JetBrains IDEs manager | Official download |

### Additional Editors
**File:** `scripts/ide_tools/editors.sh`

| Tool | Description |
|---|---|
| Emacs | Extensible text editor with LISP |

---

## Databases

### Database Engines
**File:** `scripts/ide_tools/databases.sh`

| Tool | Description |
|---|---|
| PostgreSQL | Robust relational database |
| SQLite3 | Single-file embedded database |

### Database Clients
**File:** `scripts/ide_tools/database_tools.sh`

| Tool | Description |
|---|---|
| DBeaver CE | Universal database client (GUI) |
| pgAdmin 4 | PostgreSQL web administrator |

---

## System Utilities

### Containers
**File:** `scripts/system_utils/docker.sh`

| Tool | Description |
|---|---|
| Docker Engine | Container engine |
| Docker Compose | Multi-service container orchestration |

### Git and Version Control
**File:** `scripts/system_utils/git.sh`

| Tool | Description |
|---|---|
| `git` | Version control system |
| GitHub CLI (`gh`) | Command line interface for GitHub |

### Terminal and Shell
**File:** `scripts/system_utils/terminal.sh`

| Tool | Description |
|---|---|
| `zsh` | Shell with better experience than bash |
| Oh My Zsh | Configuration framework for zsh |
| `tmux` | Terminal multiplexer |
| `fzf` | Fuzzy finder |
| `ripgrep` (`rg`) | Ultra-fast text search |
| `htop` | Interactive process monitor |
| `btop` | Resource monitor with graphics |
| `jq` | Command line JSON processor |

### Browsers
**File:** `scripts/system_utils/browsers.sh`

| Tool | Description |
|---|---|
| Brave Browser | Private browser based on Chromium |
| Firefox | Mozilla browser |

### Multimedia and Office
**File:** `scripts/system_utils/multimedia.sh`

| Tool | Description |
|---|---|
| OBS Studio | Screen recording and streaming |
| VLC | Universal media player |
| LibreOffice | Full office suite |

### Extras and Utilities
**File:** `scripts/system_utils/extras.sh`

| Tool | Description |
|---|---|
| JFLAP | Automata and formal languages tool |
| `curl` | HTTP data transfer |
| `wget` | File downloading |
| `unzip` / `tar` | Archive extraction |

### Data Science
**File:** `scripts/languages/frameworks.sh` (pip section)

| Library | Description |
|---|---|
| Pandas | Data analysis and manipulation |
| NumPy | Numerical computing |
| JupyterLab | Interactive notebook environment |

---

## Visual Customization

**File:** `scripts/system_utils/appearance.sh`

| Element | Description |
|---|---|
| Custom wallpaper | Image `assets/wallpaper.png` applied to the desktop |
| Terminal configuration | Colors and fonts for the terminal |

---

## Verification Scripts

**File:** `scripts/verify_installation.sh` and `scripts/core/rookie-verify.sh`

After installing all the software, a verification script is run that:
1. Confirms that main executables are available in `PATH`.
2. Generates a report of what was successfully installed and what failed.
3. The report is saved to `~/rookie-install-report.txt` for user reference.
