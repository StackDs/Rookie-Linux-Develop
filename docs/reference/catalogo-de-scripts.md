# Catálogo de Scripts

Lista completa de todo el software que se instala automáticamente en el primer arranque del sistema Linux generado.

---

## Lenguajes y Compiladores

### C / C++
**Archivo:** `scripts/languages/c_cpp.sh`

| Herramienta | Descripción |
|---|---|
| `gcc` | Compilador C (GNU Compiler Collection) |
| `g++` | Compilador C++ |
| `clang` | Compilador C/C++ alternativo (LLVM) |
| `make` | Herramienta de automatización de builds |
| `cmake` | Sistema de configuración de builds multiplataforma |
| `gdb` | Debugger GNU |
| `valgrind` | Analizador de memoria y profiler |

### Librerías C++ para gráficos
**Archivo:** `scripts/languages/cpp_libraries.sh`

| Librería | Descripción |
|---|---|
| `libsdl2-dev` | SDL2 — Gráficos 2D, audio, input |
| `libglfw3-dev` | GLFW — Contextos OpenGL y ventanas |
| `libglew-dev` | GLEW — Extensiones OpenGL |
| `libsfml-dev` | SFML — Multimedia 2D en C++ |
| `mesa-utils` | Utilidades OpenGL/Mesa |

### Java
**Archivo:** `scripts/languages/java.sh`

| Herramienta | Descripción |
|---|---|
| `openjdk-17-jdk` | OpenJDK 17 LTS |
| `openjdk-21-jdk` | OpenJDK 21 LTS |
| `maven` | Gestión de proyectos y dependencias Java |

### Python
**Archivo:** `scripts/languages/python.sh`

| Herramienta | Descripción |
|---|---|
| `python3` | Python 3 (última versión de repositorio) |
| `python3-pip` | Gestor de paquetes pip |
| `python3-venv` | Soporte para entornos virtuales |
| `flake8` | Linter de código Python (PEP 8) |
| `ipython` | Shell interactivo mejorado de Python |

### Node.js / JavaScript
**Archivo:** `scripts/languages/node.sh`

| Herramienta | Descripción |
|---|---|
| `nodejs` (LTS) | Node.js (instalado via NodeSource) |
| `npm` | Gestor de paquetes de Node |
| `typescript` | TypeScript (instalado globalmente via npm) |

### .NET / C#
**Archivo:** `scripts/languages/dotnet.sh`

| Herramienta | Descripción |
|---|---|
| `.NET SDK` | SDK completo de Microsoft .NET (última LTS) |

### Frameworks web y móvil
**Archivo:** `scripts/languages/frameworks.sh`

| Framework | Ecosistema | Descripción |
|---|---|---|
| Flask | Python | Microframework web |
| Django | Python | Framework web completo |
| FastAPI | Python | API REST moderno y rápido |
| Flutter SDK | Dart | Framework de UI multiplataforma |
| Dart SDK | Dart | Lenguaje de Flutter |

---

## IDEs y Editores

### IDEs principales
**Archivo:** `scripts/ide_tools/ide.sh`

| Herramienta | Descripción | Instalación |
|---|---|---|
| Visual Studio Code | Editor de Microsoft | Repositorio oficial de Microsoft |
| IntelliJ IDEA CE | IDE Java/Kotlin de JetBrains | JetBrains Toolbox o `.tar.gz` |
| JetBrains Toolbox | Gestor de IDEs JetBrains | Descarga oficial |

### Editores adicionales
**Archivo:** `scripts/ide_tools/editors.sh`

| Herramienta | Descripción |
|---|---|
| Emacs | Editor extensible con LISP |

---

## Bases de Datos

### Motores de base de datos
**Archivo:** `scripts/ide_tools/databases.sh`

| Herramienta | Descripción |
|---|---|
| PostgreSQL | Base de datos relacional robusta |
| SQLite3 | Base de datos embebida de fichero único |

### Clientes de bases de datos
**Archivo:** `scripts/ide_tools/database_tools.sh`

| Herramienta | Descripción |
|---|---|
| DBeaver CE | Cliente universal de bases de datos (GUI) |
| pgAdmin 4 | Administrador web de PostgreSQL |

---

## Utilidades del Sistema

### Contenedores
**Archivo:** `scripts/system_utils/docker.sh`

| Herramienta | Descripción |
|---|---|
| Docker Engine | Motor de contenedores |
| Docker Compose | Orquestación de contenedores multi-servicio |

### Git y control de versiones
**Archivo:** `scripts/system_utils/git.sh`

| Herramienta | Descripción |
|---|---|
| `git` | Sistema de control de versiones |
| GitHub CLI (`gh`) | Interfaz de línea de comandos para GitHub |

### Terminal y shell
**Archivo:** `scripts/system_utils/terminal.sh`

| Herramienta | Descripción |
|---|---|
| `zsh` | Shell con mejor experiencia que bash |
| Oh My Zsh | Framework de configuración para zsh |
| `tmux` | Multiplexor de terminal |
| `fzf` | Buscador difuso (fuzzy finder) |
| `ripgrep` (`rg`) | Búsqueda de texto ultrarrápida |
| `htop` | Monitor de procesos interactivo |
| `btop` | Monitor de recursos con gráficos |
| `jq` | Procesador de JSON en línea de comandos |

### Navegadores
**Archivo:** `scripts/system_utils/browsers.sh`

| Herramienta | Descripción |
|---|---|
| Brave Browser | Navegador privado basado en Chromium |
| Firefox | Navegador de Mozilla |

### Multimedia y ofimática
**Archivo:** `scripts/system_utils/multimedia.sh`

| Herramienta | Descripción |
|---|---|
| OBS Studio | Grabación y streaming de pantalla |
| VLC | Reproductor multimedia universal |
| LibreOffice | Suite ofimática completa |

### Extras y utilidades
**Archivo:** `scripts/system_utils/extras.sh`

| Herramienta | Descripción |
|---|---|
| JFLAP | Herramienta de autómatas y lenguajes formales |
| `curl` | Transferencia de datos HTTP |
| `wget` | Descarga de archivos |
| `unzip` / `tar` | Descompresión de archivos |

### Data Science
**Archivo:** `scripts/languages/frameworks.sh` (sección pip)

| Librería | Descripción |
|---|---|
| Pandas | Análisis y manipulación de datos |
| NumPy | Computación numérica |
| JupyterLab | Entorno interactivo de notebooks |

---

## Personalización visual

**Archivo:** `scripts/system_utils/appearance.sh`

| Elemento | Descripción |
|---|---|
| Wallpaper personalizado | Imagen `assets/wallpaper.png` aplicada al escritorio |
| Configuración de terminal | Colores y fuentes para la terminal |

---

## Scripts de verificación

**Archivo:** `scripts/verify_installation.sh` y `scripts/core/rookie-verify.sh`

Después de instalar todo el software, se ejecuta un script de verificación que:
1. Confirma que los ejecutables principales están disponibles en `PATH`.
2. Genera un reporte de qué se instaló correctamente y qué falló.
3. El reporte se guarda en `~/rookie-install-report.txt` para referencia del usuario.
