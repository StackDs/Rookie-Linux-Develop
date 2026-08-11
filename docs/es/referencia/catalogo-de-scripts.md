# Catálogo de Scripts

Lista completa de todo el software que se instala automáticamente en el primer arranque del sistema Linux generado.

---

## Lenguajes y Compiladores

### C / C++
**Archivo:** `scripts/languages/c_cpp.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `gcc` | Compilador C (GNU Compiler Collection) | [Sitio Oficial](https://gcc.gnu.org/) |
| `g++` | Compilador C++ | [Sitio Oficial](https://gcc.gnu.org/) |
| `clang` | Compilador C/C++ alternativo (LLVM) | [Sitio Oficial](https://clang.llvm.org/) |
| `make` | Herramienta de automatización de builds | [Sitio Oficial](https://www.gnu.org/software/make/) |
| `cmake` | Sistema de configuración de builds multiplataforma | [Sitio Oficial](https://cmake.org/) |
| `gdb` | Debugger GNU | [Sitio Oficial](https://www.gnu.org/software/gdb/) |
| `valgrind` | Analizador de memoria y profiler | [Sitio Oficial](https://valgrind.org/) |

### Librerías C++ para gráficos
**Archivo:** `scripts/languages/cpp_libraries.sh`

| Librería | Descripción | Documentación |
|---|---|---|
| `libsdl2-dev` | SDL2 — Gráficos 2D, audio, input | [Sitio Oficial](https://www.libsdl.org/) |
| `libglfw3-dev` | GLFW — Contextos OpenGL y ventanas | [Sitio Oficial](https://www.glfw.org/) |
| `libglew-dev` | GLEW — Extensiones OpenGL | [Sitio Oficial](https://glew.sourceforge.net/) |
| `libsfml-dev` | SFML — Multimedia 2D en C++ | [Sitio Oficial](https://www.sfml-dev.org/) |
| `mesa-utils` | Utilidades OpenGL/Mesa | [Sitio Oficial](https://www.mesa3d.org/) |

### Java
**Archivo:** `scripts/languages/java.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `openjdk-17-jdk` | OpenJDK 17 LTS | [Sitio Oficial](https://openjdk.org/projects/jdk/17/) |
| `openjdk-21-jdk` | OpenJDK 21 LTS | [Sitio Oficial](https://openjdk.org/projects/jdk/21/) |
| `maven` | Gestión de proyectos y dependencias Java | [Sitio Oficial](https://maven.apache.org/) |

### Python
**Archivo:** `scripts/languages/python.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `python3` | Python 3 (última versión de repositorio) | [Sitio Oficial](https://docs.python.org/3/) |
| `python3-pip` | Gestor de paquetes pip | [Sitio Oficial](https://pip.pypa.io/) |
| `python3-venv` | Soporte para entornos virtuales | [Sitio Oficial](https://docs.python.org/3/library/venv.html) |
| `flake8` | Linter de código Python (PEP 8) | [Sitio Oficial](https://flake8.pycqa.org/) |
| `ipython` | Shell interactivo mejorado de Python | [Sitio Oficial](https://ipython.readthedocs.io/) |

### Node.js / JavaScript
**Archivo:** `scripts/languages/node.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `nodejs` (LTS) | Node.js (instalado via NodeSource) | [Sitio Oficial](https://nodejs.org/) |
| `npm` | Gestor de paquetes de Node | [Sitio Oficial](https://docs.npmjs.com/) |
| `typescript` | TypeScript (instalado globalmente via npm) | [Sitio Oficial](https://www.typescriptlang.org/) |

### .NET / C#
**Archivo:** `scripts/languages/dotnet.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `.NET SDK` | SDK completo de Microsoft .NET (última LTS) | [Sitio Oficial](https://dotnet.microsoft.com/es-es/) |

### Frameworks web y móvil
**Archivo:** `scripts/languages/frameworks.sh`

| Framework | Ecosistema | Descripción | Documentación |
|---|---|---|---|
| Flask | Python | Microframework web | [Sitio Oficial](https://flask.palletsprojects.com/) |
| Django | Python | Framework web completo | [Sitio Oficial](https://www.djangoproject.com/) |
| FastAPI | Python | API REST moderno y rápido | [Sitio Oficial](https://fastapi.tiangolo.com/) |
| Flutter SDK | Dart | Framework de UI multiplataforma | [Sitio Oficial](https://flutter.dev/) |
| Dart SDK | Dart | Lenguaje de Flutter | [Sitio Oficial](https://dart.dev/) |

---

## IDEs y Editores

### IDEs principales
**Archivo:** `scripts/ide_tools/ide.sh`

| Herramienta | Descripción | Instalación | Documentación |
|---|---|---|---|
| Visual Studio Code | Editor de Microsoft | Repositorio oficial de Microsoft | [Sitio Oficial](https://code.visualstudio.com/) |
| IntelliJ IDEA CE | IDE Java/Kotlin de JetBrains | Paquete `.tar.gz` oficial | [Sitio Oficial](https://www.jetbrains.com/idea/) |
| Antigravity IDE | Entorno de desarrollo impulsado por IA | Descarga oficial | [Sitio Oficial](https://antigravity.google/) |

### Editores adicionales
**Archivo:** `scripts/ide_tools/editors.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| Emacs | Editor extensible con LISP | [Sitio Oficial](https://www.gnu.org/software/emacs/) |

---

## Bases de Datos

### Motores de base de datos
**Archivo:** `scripts/ide_tools/databases.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| PostgreSQL | Base de datos relacional robusta | [Sitio Oficial](https://www.postgresql.org/) |
| SQLite3 | Base de datos embebida de fichero único | [Sitio Oficial](https://www.sqlite.org/) |

### Clientes de bases de datos
**Archivo:** `scripts/ide_tools/database_tools.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| DBeaver CE | Cliente universal de bases de datos (GUI) | [Sitio Oficial](https://dbeaver.io/) |
| pgAdmin 4 | Administrador web de PostgreSQL | [Sitio Oficial](https://www.pgadmin.org/) |

---

## Utilidades del Sistema

### Contenedores
**Archivo:** `scripts/system_utils/docker.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| Docker Engine | Motor de contenedores | [Sitio Oficial](https://docs.docker.com/) |
| Docker Compose | Orquestación de contenedores multi-servicio | [Sitio Oficial](https://docs.docker.com/compose/) |

### Git y control de versiones
**Archivo:** `scripts/system_utils/git.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `git` | Sistema de control de versiones | [Sitio Oficial](https://git-scm.com/) |
| GitHub CLI (`gh`) | Interfaz de línea de comandos para GitHub | [Sitio Oficial](https://cli.github.com/) |

### Terminal y shell
**Archivo:** `scripts/system_utils/terminal.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| `zsh` | Shell con mejor experiencia que bash | [Sitio Oficial](https://zsh.sourceforge.io/) |
| Oh My Zsh | Framework de configuración para zsh | [Sitio Oficial](https://ohmyz.sh/) |
| `tmux` | Multiplexor de terminal | [Sitio Oficial](https://github.com/tmux/tmux/wiki) |
| `fzf` | Buscador difuso (fuzzy finder) | [Sitio Oficial](https://github.com/junegunn/fzf) |
| `ripgrep` (`rg`) | Búsqueda de texto ultrarrápida | [Sitio Oficial](https://github.com/BurntSushi/ripgrep) |
| `htop` | Monitor de procesos interactivo | [Sitio Oficial](https://htop.dev/) |
| `btop` | Monitor de recursos con gráficos | [Sitio Oficial](https://github.com/aristocratos/btop) |
| `jq` | Procesador de JSON en línea de comandos | [Sitio Oficial](https://jqlang.github.io/jq/) |

### Navegadores
**Archivo:** `scripts/system_utils/browsers.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| Brave Browser | Navegador privado basado en Chromium | [Sitio Oficial](https://brave.com/) |
| Firefox | Navegador de Mozilla | [Sitio Oficial](https://www.mozilla.org/es-ES/firefox/) |

### Multimedia y ofimática
**Archivo:** `scripts/system_utils/multimedia.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| OBS Studio | Grabación y streaming de pantalla | [Sitio Oficial](https://obsproject.com/) |
| VLC | Reproductor multimedia universal | [Sitio Oficial](https://www.videolan.org/vlc/) |
| LibreOffice | Suite ofimática completa | [Sitio Oficial](https://es.libreoffice.org/) |

### Extras y utilidades
**Archivo:** `scripts/system_utils/extras.sh`

| Herramienta | Descripción | Documentación |
|---|---|---|
| JFLAP | Herramienta de autómatas y lenguajes formales | [Sitio Oficial](https://www.jflap.org/) |
| `curl` | Transferencia de datos HTTP | [Sitio Oficial](https://curl.se/) |
| `wget` | Descarga de archivos | [Sitio Oficial](https://www.gnu.org/software/wget/) |
| `unzip` / `tar` | Descompresión de archivos | [Sitio Oficial](https://www.gnu.org/software/tar/) |

### Data Science
**Archivo:** `scripts/languages/frameworks.sh` (sección pip)

| Librería | Descripción | Documentación |
|---|---|---|
| Pandas | Análisis y manipulación de datos | [Sitio Oficial](https://pandas.pydata.org/) |
| NumPy | Computación numérica | [Sitio Oficial](https://numpy.org/) |
| JupyterLab | Entorno interactivo de notebooks | [Sitio Oficial](https://jupyter.org/) |

---

## Personalización visual

**Archivo:** `scripts/system_utils/appearance.sh`

| Elemento | Descripción | Documentación |
|---|---|---|
| Wallpaper personalizado | Imagen `assets/wallpaper.png` aplicada al escritorio |
| Configuración de terminal | Colores y fuentes para la terminal |

---

## Scripts de verificación

**Archivo:** `scripts/verify_installation.sh` y `scripts/core/rookie-verify.sh`

Después de instalar todo el software, se ejecuta un script de verificación que:
1. Confirma que los ejecutables principales están disponibles en `PATH`.
2. Genera un reporte de qué se instaló correctamente y qué falló.
3. El reporte se guarda en `~/rookie-install-report.txt` para referencia del usuario.
