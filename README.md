# Rookie Linux Builder 🐧🛠️

**Rookie Linux Builder** es una herramienta integral diseñada para crear imágenes ISO personalizadas (remasterizadas) de distribuciones Linux orientadas al desarrollo de software. Permite inyectar un ecosistema completo de herramientas de desarrollo, IDEs, bases de datos y configuraciones en una imagen ISO "vanilla", de forma que, tras instalar el sistema operativo, el entorno de programación quede completamente configurado de manera desatendida durante el primer inicio.

## 🚀 ¿Qué contiene la aplicación?

La aplicación se compone de varios módulos principales:

1. **Frontend (Interfaz de Usuario)**: Desarrollada en Python (utilizando `customtkinter`), proporciona una interfaz gráfica para que el usuario seleccione la distribución base (Ubuntu, Mint, Pop!_OS, Fedora) e inicie el proceso de construcción de la ISO.
2. **Builder (Motor de Construcción)**: Scripts (como `build_iso.sh`) que operan aislados dentro de un contenedor Docker. Se encargan de descargar la ISO original, desempaquetarla (usando herramientas como `xorriso` y `unsquashfs`), inyectar las plantillas de configuración (`/templates`) y los scripts de instalación (`/scripts`), y finalmente reconstruir una nueva imagen ISO booteable.
3. **Scripts de Post-Instalación**: Una extensa batería de scripts bash modulares (`/scripts`) que se copian al sistema de archivos de la nueva ISO. Estos se ejecutan automáticamente la primera vez que el usuario inicia sesión en el nuevo sistema, instalando y configurando todo el software necesario.
4. **Plantillas (Templates)**: Archivos de configuración (`.desktop`, `ks.cfg`, etc.) necesarios para automatizar el instalador de cada distribución de Linux soportada o para orquestar el auto-arranque gráfico post-instalación.

## 📂 Descripción de los Scripts (`/scripts`)

La carpeta `/scripts` es el corazón de la configuración del entorno de desarrollo. Contiene scripts Bash modulares que instalan y configuran herramientas específicas:

- **`install.sh`**: Es el orquestador principal. Es llamado durante el primer inicio del sistema y se encarga de ejecutar de manera secuencial (Paso a Paso) todos los demás scripts de esta carpeta.
- **`update.sh`**: Actualiza el sistema operativo base y prepara las dependencias esenciales antes de proceder con el resto de las instalaciones.
- **`ide.sh`**: Instala entornos de desarrollo integrados (IDEs) como Visual Studio Code, IntelliJ IDEA Community, Emacs y Antigravity.
- **`database_tools.sh`**: Instala clientes visuales de bases de datos como DBeaver y pgAdmin4.
- **`c_cpp.sh`**: Instala compiladores y herramientas de construcción para C/C++ (gcc, g++, gdb, make, cmake, clang, ninja, valgrind).
- **`java.sh`**: Configura el ecosistema Java (OpenJDK 17, OpenJDK 21 y Maven).
- **`python.sh`**: Configura el ecosistema Python (Python 3, pip, venv, pipx, black, flake8, ipython y frameworks como Django, Flask, FastAPI).
- **`dotnet.sh`**: Instala el SDK de .NET para desarrollo en C#.
- **`node.sh`**: Instala Node.js LTS, npm y herramientas relacionadas al ecosistema JavaScript/TypeScript.
- **`databases.sh`**: Instala los motores de bases de datos locales (PostgreSQL, SQLite, etc.).
- **`docker.sh`**: Instala Docker Engine, Docker Compose y configura los permisos correctos para el usuario local.
- **`git.sh`**: Instala control de versiones con Git, Git LFS y la interfaz de línea de comandos de GitHub (GitHub CLI).
- **`terminal.sh`**: Configura utilidades de terminal productivas (Zsh, tmux, htop, btop, curl, wget, ripgrep, fd, fzf, jq, bat, etc.) y descompresores.
- **`editors.sh`**: Instala editores de texto rápidos para la línea de comandos (nano, vim, neovim).
- **`browsers.sh`**: Instala navegadores web alternativos (Brave, Firefox).
- **`multimedia.sh`**: Instala software para consumir o crear contenido multimedia (VLC y OBS Studio).
- **`cpp_libraries.sh`**: Instala bibliotecas comunes para desarrollo de juegos y gráficos en C++ (SDL2, SFML, OpenGL, GLFW, GLEW).
- **`frameworks.sh`**: Instala frameworks, SDKs y herramientas de diagramación (Flutter SDK, Dart SDK, Jflap, plantillas UML).
- **`extras.sh`**: Instala programas ofimáticos y herramientas adicionales (LibreOffice, evince).
- **`appearance.sh`**: Configura la apariencia del entorno de escritorio, ajustando temas y modos oscuros para el ambiente de desarrollo.
- **`easter_eggs.sh`**: Instala utilidades divertidas, huevos de pascua o chistes internos para la terminal.
- **`verify_installation.sh`**: Es el script final. Verifica que todas las herramientas binarias respondan correctamente, establece el fondo de pantalla oficial (marca de agua de Rookie Linux) y crea una marca para indicar que la instalación fue completada con éxito.
- **`build_exe.py`**: Es un script en Python (ajeno al instalador de Linux) que utiliza PyInstaller para empaquetar el frontend (la aplicación en Windows) y todas sus dependencias/carpetas anexas en un único archivo ejecutable (`.zip` con el `.exe` adentro) para su fácil distribución.

## 📦 Construcción del Ejecutable de la Herramienta

Si deseas compilar la aplicación GUI de Windows:

1. Asegúrate de tener Python instalado en tu sistema Windows.
2. Ejecuta en tu terminal o símbolo del sistema: `python scripts/build_exe.py`
3. El script automáticamente instalará las dependencias necesarias de Python, compilará la aplicación en un `.exe` con interfaz gráfica de usuario y empaquetará todas las carpetas (`builder`, `scripts`, `templates`, etc.) en un archivo final llamado `Rookie-Linux-Builder-Release.zip` en tu Escritorio.

## ⚙️ Ecosistema Resultante

Cualquier sistema instalado a través de una ISO generada por Rookie Linux Builder contendrá por defecto, listo para usarse, un ecosistema de desarrollo moderno y altamente productivo con todo el stack mencionado en los scripts.
