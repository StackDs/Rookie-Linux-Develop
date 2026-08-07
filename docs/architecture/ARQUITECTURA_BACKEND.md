# Arquitectura del Backend

## Visión general

El backend de Rookie Linux Develop está compuesto íntegramente por scripts **Bash** que se ejecutan en un entorno Linux (nativo o vía WSL en Windows). El frontend Python actúa solo como orquestador: lanza los scripts, lee su stdout en tiempo real y actualiza la interfaz con el progreso.

---

## Árbol de archivos

```
builder/
├── download_iso.sh     Descarga la ISO oficial de cada distro
├── build_iso.sh        Modifica la ISO e inyecta todo el contenido
├── utils.sh            Funciones de utilidad compartidas (log, download_file, etc.)
├── ejecutar.sh         Script de prueba/desarrollo para lanzar el build manualmente
├── entrypoint.sh       Punto de entrada para contenedores Docker (modo Windows legacy)
└── templates/
    ├── ubuntu/         Plantillas Cloud-Init para Ubuntu
    ├── mint/           Plantillas preseed para Linux Mint
    ├── fedora/         Kickstart (ks.cfg) para Fedora
    └── popos/          Scripts y configuración para Pop!_OS

scripts/
├── install.sh              Script principal que llama a todos los módulos
├── verify_installation.sh  Verifica que la instalación fue exitosa
├── core/
│   ├── utils.sh            Funciones de logging y utilidad
│   ├── update.sh           Actualización del sistema (apt/dnf)
│   └── rookie-verify.sh    Script de verificación post-instalación
├── ide_tools/
│   ├── ide.sh              VSCode, IntelliJ, JetBrains Toolbox
│   ├── editors.sh          Emacs y otros editores
│   ├── databases.sh        DBeaver, pgAdmin4
│   └── database_tools.sh   Clientes de bases de datos adicionales
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
    ├── extras.sh           JFLAP, herramientas varias
    ├── appearance.sh       Wallpaper personalizado, tema visual
    └── easter_eggs.sh      Detalles y personalizaciones especiales
```

---

## Flujo de ejecución del backend

### Fase 1: Descarga (`download_iso.sh`)

1. Recibe el nombre de la distro como argumento (`ubuntu`, `mint`, `fedora`, `popos_nvidia`, etc.).
2. Llama a `resolve_iso_source()` que determina dinámicamente la URL de descarga.
   - **Ubuntu**: Scraping del índice de `releases.ubuntu.com` para obtener la última versión LTS.
   - **Mint**: URL estable basada en versión y edición configurables.
   - **Fedora**: Scraping del mirror de Fedora para obtener la última ISO Workstation Live.
   - **Pop!_OS**: Consulta la API JSON de `api.pop-os.org` para obtener la URL correcta según variante (generic/nvidia).
3. Descarga la ISO con `wget` o `aria2c` mostrando porcentaje al stdout para que Python actualice la barra.
4. La ISO se guarda en `downloads/iso/{distro}/`.

### Fase 2: Construcción (`build_iso.sh`)

1. **Localiza la ISO** descargada en `downloads/iso/{distro}/`.
2. **Prepara el contenido a inyectar**: copia todos los archivos de `scripts/` a `/tmp/iso_unpacked/custom_scripts/`.
3. **Copia el wallpaper** desde `assets/wallpaper.png` a la carpeta temporal.
4. **Por distribución**, aplica la estrategia de automatización correspondiente (ver [Flujo de creación de ISO](./flujo-creacion-iso.md)).
5. **Reempaqueta la ISO** usando `xorriso` con arranque EFI+BIOS preservado.
6. Guarda el resultado en `output/{distro}/`.

### Fase 3: Primer arranque (scripts post-instalación)

Los `scripts/` inyectados en la ISO se ejecutan la primera vez que el sistema arranca en el equipo del usuario. El script `install.sh` actúa como director de orquesta, llamando a todos los módulos en orden.

---

## Comunicación Frontend → Backend

```
frontend/screens/installation_tools/build_progress_screen.py
    │
    ├─ Crea un subprocess.Popen() con el script Bash
    ├─ Lee stdout línea a línea (char a char para mayor fluidez)
    ├─ Detecta patrones como "XX%" → actualiza barra de progreso
    ├─ Detecta palabras clave como "exitosa" → señal de éxito
    ├─ Detecta "[FATAL_ERROR]" → señal de error crítico
    └─ Al terminar el proceso → muestra popup de resultado
```

El script Bash nunca interactúa con la GUI directamente. Toda la comunicación es unidireccional a través de `stdout`.

---

## Variables de entorno del backend

| Variable | Script | Descripción |
|----------|--------|-------------|
| `ISO_DISTRO` | `download_iso.sh`, `build_iso.sh` | Distro objetivo (`ubuntu`, `mint`, `fedora`, `popos_nvidia`) |
| `CUSTOM_ISO_NAME` | `build_iso.sh` | Nombre personalizado incrustado en la ISO final |
| `UBUNTU_VERSION` | `download_iso.sh` | Versión de Ubuntu (por defecto: `24.04`) |
| `MINT_VERSION` | `download_iso.sh` | Versión de Mint (por defecto: `22.1`) |
| `FEDORA_VERSION` | `download_iso.sh` | Versión de Fedora (por defecto: `41`) |
| `POP_VARIANT` | `download_iso.sh` | Variante Pop!_OS (`generic` o `nvidia`) |
| `ISO_URL` | `download_iso.sh` | URL manual para sobrescribir la detección automática |
| `ISO_NAME` | `download_iso.sh` | Nombre de archivo manual para sobrescribir la detección |
