# Script Catalog

Complete list of all software that is automatically installed on the first boot of the generated Linux system.

---

## Languages and Compilers

### C / C++
**File:** `scripts/languages/c_cpp.sh`

| Tool | Description | Documentation |
|---|---|---|
| `gcc` | C Compiler (GNU Compiler Collection) | [Official Site](https://gcc.gnu.org/) |
| `g++` | C++ Compiler | [Official Site](https://gcc.gnu.org/) |
| `clang` | Alternative C/C++ compiler (LLVM) | [Official Site](https://clang.llvm.org/) |
| `make` | Build automation tool | [Official Site](https://www.gnu.org/software/make/) |
| `cmake` | Cross-platform build configuration system | [Official Site](https://cmake.org/) |
| `gdb` | GNU Debugger | [Official Site](https://www.gnu.org/software/gdb/) |
| `valgrind` | Memory analyzer and profiler | [Official Site](https://valgrind.org/) |

### C++ Graphics Libraries
**File:** `scripts/languages/cpp_libraries.sh`

| Library | Description | Documentation |
|---|---|---|
| `libsdl2-dev` | SDL2 — 2D Graphics, audio, input | [Official Site](https://www.libsdl.org/) |
| `libglfw3-dev` | GLFW — OpenGL contexts and windows | [Official Site](https://www.glfw.org/) |
| `libglew-dev` | GLEW — OpenGL extensions | [Official Site](https://glew.sourceforge.net/) |
| `libsfml-dev` | SFML — 2D Multimedia in C++ | [Official Site](https://www.sfml-dev.org/) |
| `mesa-utils` | OpenGL/Mesa utilities | [Official Site](https://www.mesa3d.org/) |

### Java
**File:** `scripts/languages/java.sh`

| Tool | Description | Documentation |
|---|---|---|
| `openjdk-17-jdk` | OpenJDK 17 LTS | [Official Site](https://openjdk.org/projects/jdk/17/) |
| `openjdk-21-jdk` | OpenJDK 21 LTS | [Official Site](https://openjdk.org/projects/jdk/21/) |
| `maven` | Java project and dependency management | [Official Site](https://maven.apache.org/) |

### Python
**File:** `scripts/languages/python.sh`

| Tool | Description | Documentation |
|---|---|---|
| `python3` | Python 3 (latest repository version) | [Official Site](https://docs.python.org/3/) |
| `python3-pip` | pip package manager | [Official Site](https://pip.pypa.io/) |
| `python3-venv` | Virtual environment support | [Official Site](https://docs.python.org/3/library/venv.html) |
| `flake8` | Python code linter (PEP 8) | [Official Site](https://flake8.pycqa.org/) |
| `ipython` | Enhanced interactive Python shell | [Official Site](https://ipython.readthedocs.io/) |

### Node.js / JavaScript
**File:** `scripts/languages/node.sh`

| Tool | Description | Documentation |
|---|---|---|
| `nodejs` (LTS) | Node.js (installed via NodeSource) | [Official Site](https://nodejs.org/) |
| `npm` | Node package manager | [Official Site](https://docs.npmjs.com/) |
| `typescript` | TypeScript (installed globally via npm) | [Official Site](https://www.typescriptlang.org/) |

### .NET / C#
**File:** `scripts/languages/dotnet.sh`

| Tool | Description | Documentation |
|---|---|---|
| `.NET SDK` | Full Microsoft .NET SDK (latest LTS) | [Official Site](https://dotnet.microsoft.com/) |

### Web and Mobile Frameworks
**File:** `scripts/languages/frameworks.sh`

| Framework | Ecosystem | Description | Documentation |
|---|---|---|---|
| Flask | Python | Web microframework | [Official Site](https://flask.palletsprojects.com/) |
| Django | Python | Full web framework | [Official Site](https://www.djangoproject.com/) |
| FastAPI | Python | Modern and fast REST API | [Official Site](https://fastapi.tiangolo.com/) |
| Flutter SDK | Dart | Cross-platform UI framework | [Official Site](https://flutter.dev/) |
| Dart SDK | Dart | Flutter language | [Official Site](https://dart.dev/) |

---

## IDEs and Editors

### Main IDEs
**File:** `scripts/ide_tools/ide.sh`

| Tool | Description | Installation | Documentation |
|---|---|---|---|
| Visual Studio Code | Microsoft editor | Official Microsoft repository | [Official Site](https://code.visualstudio.com/) |
| IntelliJ IDEA CE | JetBrains Java/Kotlin IDE | Official `.tar.gz` package | [Official Site](https://www.jetbrains.com/idea/) |
| Antigravity IDE | AI-powered development environment | Official download | [Official Site](https://antigravity.google/) |

### Additional Editors
**File:** `scripts/ide_tools/editors.sh`

| Tool | Description | Documentation |
|---|---|---|
| Emacs | Extensible text editor with LISP | [Official Site](https://www.gnu.org/software/emacs/) |

---

## Databases

### Database Engines
**File:** `scripts/ide_tools/databases.sh`

| Tool | Description | Documentation |
|---|---|---|
| PostgreSQL | Robust relational database | [Official Site](https://www.postgresql.org/) |
| SQLite3 | Single-file embedded database | [Official Site](https://www.sqlite.org/) |

### Database Clients
**File:** `scripts/ide_tools/database_tools.sh`

| Tool | Description | Documentation |
|---|---|---|
| DBeaver CE | Universal database client (GUI) | [Official Site](https://dbeaver.io/) |
| pgAdmin 4 | PostgreSQL web administrator | [Official Site](https://www.pgadmin.org/) |

---

## System Utilities

### Containers
**File:** `scripts/system_utils/docker.sh`

| Tool | Description | Documentation |
|---|---|---|
| Docker Engine | Container engine | [Official Site](https://docs.docker.com/) |
| Docker Compose | Multi-service container orchestration | [Official Site](https://docs.docker.com/compose/) |

### Git and Version Control
**File:** `scripts/system_utils/git.sh`

| Tool | Description | Documentation |
|---|---|---|
| `git` | Version control system | [Official Site](https://git-scm.com/) |
| GitHub CLI (`gh`) | Command line interface for GitHub | [Official Site](https://cli.github.com/) |

### Terminal and Shell
**File:** `scripts/system_utils/terminal.sh`

| Tool | Description | Documentation |
|---|---|---|
| `zsh` | Shell with better experience than bash | [Official Site](https://zsh.sourceforge.io/) |
| Oh My Zsh | Configuration framework for zsh | [Official Site](https://ohmyz.sh/) |
| `tmux` | Terminal multiplexer | [Official Site](https://github.com/tmux/tmux/wiki) |
| `fzf` | Fuzzy finder | [Official Site](https://github.com/junegunn/fzf) |
| `ripgrep` (`rg`) | Ultra-fast text search | [Official Site](https://github.com/BurntSushi/ripgrep) |
| `htop` | Interactive process monitor | [Official Site](https://htop.dev/) |
| `btop` | Resource monitor with graphics | [Official Site](https://github.com/aristocratos/btop) |
| `jq` | Command line JSON processor | [Official Site](https://jqlang.github.io/jq/) |

### Browsers
**File:** `scripts/system_utils/browsers.sh`

| Tool | Description | Documentation |
|---|---|---|
| Brave Browser | Private browser based on Chromium | [Official Site](https://brave.com/) |
| Firefox | Mozilla browser | [Official Site](https://www.mozilla.org/en-US/firefox/) |

### Multimedia and Office
**File:** `scripts/system_utils/multimedia.sh`

| Tool | Description | Documentation |
|---|---|---|
| OBS Studio | Screen recording and streaming | [Official Site](https://obsproject.com/) |
| VLC | Universal media player | [Official Site](https://www.videolan.org/vlc/) |
| LibreOffice | Full office suite | [Official Site](https://www.libreoffice.org/) |

### Extras and Utilities
**File:** `scripts/system_utils/extras.sh`

| Tool | Description | Documentation |
|---|---|---|
| JFLAP | Automata and formal languages tool | [Official Site](https://www.jflap.org/) |
| `curl` | HTTP data transfer | [Official Site](https://curl.se/) |
| `wget` | File downloading | [Official Site](https://www.gnu.org/software/wget/) |
| `unzip` / `tar` | Archive extraction | [Official Site](https://www.gnu.org/software/tar/) |

### Data Science
**File:** `scripts/languages/frameworks.sh` (pip section)

| Library | Description | Documentation |
|---|---|---|
| Pandas | Data analysis and manipulation | [Official Site](https://pandas.pydata.org/) |
| NumPy | Numerical computing | [Official Site](https://numpy.org/) |
| JupyterLab | Interactive notebook environment | [Official Site](https://jupyter.org/) |

---

## Visual Customization

**File:** `scripts/system_utils/appearance.sh`

| Element | Description | Documentation |
|---|---|---|
| Custom wallpaper | Image `assets/wallpaper.png` applied to the desktop|
| Terminal configuration | Colors and fonts for the terminal|

---

## Verification Scripts

**File:** `scripts/verify_installation.sh` and `scripts/core/rookie-verify.sh`

After installing all the software, a verification script is run that:
1. Confirms that main executables are available in `PATH`.
2. Generates a report of what was successfully installed and what failed.
3. The report is saved to `~/rookie-install-report.txt` for user reference.
