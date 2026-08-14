# Estructura de Pantallas del Frontend

Mapa completo de todas las pantallas (screens) de la aplicación, sus responsabilidades y las transiciones de navegación entre ellas.

---

## Árbol de archivos

```
frontend/
├── main.py                          Punto de entrada, clase App
├── utils.py                         Funciones de utilidad (rutas, efectos)
├── custom_messagebox.py             Sistema de diálogos modales
└── screens/
    ├── core/                        Pantallas principales de navegación
    │   ├── start_screen.py
    │   └── option_selection_screen.py
    ├── info_manuals/                Pantallas informativas y manuales
    │   ├── info_screen.py
    │   ├── explanation_screen.py
    │   ├── instructions_screen.py
    │   ├── documentation_screen.py
    │   ├── about_screen.py
    │   └── bitlocker_screen.py
    ├── linux_concepts/              Pantallas educativas sobre Linux
    │   ├── distro_selection_screen.py
    │   ├── distro_info_screen.py
    │   ├── basic_concepts_screen.py
    │   ├── virtual_machine_screen.py
    │   └── clean_installation_screen.py
    └── installation_tools/          Pantallas de herramientas de instalación
        ├── build_progress_screen.py
        ├── usb_flash_screen.py
        ├── wsl_install_screen.py
        ├── wsl_app_install_screen.py
        ├── wsl_main_install_screen.py
        ├── flasher_worker_linux.py
        └── flasher_worker_windows.py
```

---

## Descripción detallada por pantalla

### `core/` — Navegación principal

#### `StartScreen`
- **Propósito**: Pantalla de bienvenida con animación de tipeo estilo terminal.
- **Navega a**: `OptionSelectionScreen` (botón "Iniciar")
- **`on_show()`**: Sí — reinicia la animación de tipeo si ya se completó.
- **Notas**: Tiene un efecto de cursor parpadeante (`_`) después del texto.

#### `OptionSelectionScreen`
- **Propósito**: Menú principal con las 7 opciones de la aplicación.
- **Navega a**: Todas las pantallas del menú principal.
- **`on_show()`**: No.
- **Notas**: 
  - El botón de WSL está deshabilitado visualmente en Linux (modo `dimmed=True`) pero es clickeable y muestra un mensaje informativo.
  - Cada opción tiene una flecha `>` animada al hacer hover.

---

### `info_manuals/` — Pantallas informativas

#### `InfoScreen`
- **Propósito**: Manual de uso — lista de herramientas incluidas en la ISO.
- **Navega a**: `OptionSelectionScreen` (← Volver)
- **`on_show()`**: Sí — anima el texto si no se ha animado aún (lo marca con `has_animated`).
- **Notas**: Muestra el contenido con una animación de máquina de escribir.

#### `ExplanationScreen`
- **Propósito**: Hub de "Sobre Linux" con tres rutas: Dual Boot, Máquina Virtual, Instalación Limpia.
- **Navega a**: `BasicConceptsScreen`, `VirtualMachineScreen`, `CleanInstallationScreen`, `OptionSelectionScreen`.
- **`on_show()`**: No.

#### `InstructionsScreen`
- **Propósito**: Instrucciones paso a paso para usar el USB de instalación.
- **Navega a**: `OptionSelectionScreen` (← Volver)
- **`on_show()`**: No.

#### `DocumentationScreen`
- **Propósito**: Links a documentación oficial, organizados en pestañas por categoría.
- **Navega a**: `OptionSelectionScreen` (← Volver)
- **`on_show()`**: No.
- **Notas**: Usa `ctk.CTkTabview` con 6 pestañas: SO y Núcleo, Lenguajes, IDEs y Terminal, Bases de Datos, Librerías y Frameworks, Ofimática.

#### `AboutScreen`
- **Propósito**: Información sobre la aplicación, créditos e imagen de presentación.
- **Navega a**: `OptionSelectionScreen` (← Volver)
- **`on_show()`**: No.
- **Notas**: La imagen soporta zoom en una ventana emergente (`CTkToplevel`). La ventana emergente usa `root` como padre directo para evitar bugs de jerarquía en Linux con `CTkScrollableFrame`.

#### `BitlockerScreen`
- **Propósito**: Explicación de qué es BitLocker y cómo desactivarlo antes de instalar Linux.
- **Navega a**: `CleanInstallationScreen` (← Volver)
- **`on_show()`**: No.

---

### `linux_concepts/` — Educación sobre Linux

#### `DistroSelectionScreen`
- **Propósito**: Selector de distribución mediante radio buttons.
- **Navega a**: `DistroInfoScreen` (→ Ver Detalles), `OptionSelectionScreen` (← Volver)
- **`on_show()`**: No.
- **Estado compartido**: `self.distro_var` (StringVar) — leído por `DistroInfoScreen` y `BuildProgressScreen`.

#### `DistroInfoScreen`
- **Propósito**: Información detallada de la distro seleccionada con capturas de pantalla y texto animado.
- **Navega a**: `DistroSelectionScreen` (← Volver), `BuildProgressScreen` (Confirmar y Generar)
- **`on_show()`**: Sí — carga las imágenes y anima el texto si la distro cambió respecto a la última visita.
- **Notas**: Las imágenes soportan zoom. Guarda `self.last_distro` para detectar cambios. Incluye un diálogo de confirmación `msg_ask_yes_no` antes de iniciar el proceso de generación de imagen para prevenir descargas no intencionales.

#### `BasicConceptsScreen`
- **Propósito**: Qué es el Dual Boot. Incluye imagen explicativa.
- **Navega a**: `ExplanationScreen` (← Volver), `VirtualMachineScreen` (Siguiente →)
- **`on_show()`**: No.

#### `VirtualMachineScreen`
- **Propósito**: Qué es una Máquina Virtual. Incluye imagen explicativa.
- **Navega a**: `BasicConceptsScreen` (← Volver), `CleanInstallationScreen` (Siguiente →)
- **`on_show()`**: No.

#### `CleanInstallationScreen`
- **Propósito**: Qué es una Instalación Limpia. Incluye imagen explicativa.
- **Navega a**: `VirtualMachineScreen` (← Volver), `BitlockerScreen` (Siguiente →)
- **`on_show()`**: No.

---

### `installation_tools/` — Herramientas de instalación

#### `BuildProgressScreen`
- **Propósito**: Orquesta la descarga de la ISO y la construcción de la imagen personalizada.
- **Navega a**: `DistroInfoScreen` (← Volver al terminar), `UsbFlashScreen` (botón que aparece al finalizar), `OptionSelectionScreen` (al completar con éxito)
- **`on_show()`**: Sí — resetea el estado y lanza `ejecutar_script()` automáticamente.
- **Estado interno**: Dos `ProgressBarManager` (descarga y generación), referencia al proceso actual (`self.current_process`), flag de cancelación (`self.is_cancelled`).
- **Notas**: Es la pantalla más compleja. Usa threads para no bloquear la GUI.

#### `UsbFlashScreen`
- **Propósito**: Selector de ISO y USB, con progreso de flasheo.
- **Navega a**: `OptionSelectionScreen` (← Volver), `OptionSelectionScreen` (al completar con éxito)
- **`on_show()`**: Sí — detecta automáticamente los USBs conectados.
- **Notas**: Lanza un proceso worker elevado (`pkexec` / `RunAs`) para escribir en el disco. El progreso se comunica via archivo JSON temporal.

#### `WslInstallScreen`
- **Propósito**: Menú de selección de modo de instalación de WSL (Solo relevante en Windows).
- **Navega a**: `OptionSelectionScreen` (← Volver), `WslAppInstallScreen` (Modo App), `WslMainInstallScreen` (Modo Main)
- **`on_show()`**: No.

#### `WslAppInstallScreen`
- **Propósito**: Instala un subsistema WSL básico y una distribución auxiliar (Ubuntu) para poder compilar imágenes ISO dentro de la herramienta.
- **Navega a**: `OptionSelectionScreen` (← Volver)
- **`on_show()`**: Sí — resetea el estado de la instalación.
- **Notas**: Incluye diálogos de confirmación antes de requerir permisos de administrador. Redirige automáticamente al menú al terminar con éxito.

#### `WslMainInstallScreen`
- **Propósito**: Tablero completo para instalar WSL y gestionar cualquier distribución de Linux disponible en la tienda de Microsoft como sistema principal.
- **Navega a**: `OptionSelectionScreen` (← Volver)
- **`on_show()`**: Sí — escanea de forma asíncrona el estado actual de WSL y las distribuciones instaladas.
- **Notas**: Usa pestañas (`CTkTabview`) para separar el estado del entorno y la gestión de distribuciones. Cuenta con diálogos de confirmación integrados.-

### Workers (no son pantallas)

#### `flasher_worker_linux.py`
- **Propósito**: Proceso separado con permisos de root que limpia el USB y escribe la ISO con `dd`.
- **No es una pantalla GUI** — se ejecuta como subproceso elevado.
- **Comunica progreso** via `/tmp/rookie_flash_progress.json`.

#### `flasher_worker_windows.py`
- **Propósito**: Equivalente al worker de Linux para Windows. Usa DISKPART y `dd` para Windows.
- **No es una pantalla GUI** — se ejecuta como subproceso elevado con `RunAs`.

---

## Mapa de navegación completo

```
StartScreen
    └─[Iniciar]→ OptionSelectionScreen
                     │
                     ├─[Manual de uso]────────→ InfoScreen
                     │                              └─[Volver]→ OptionSelectionScreen
                     │
                     ├─[Sobre Linux]───────────→ ExplanationScreen
                     │                              ├─[Dual Boot]→ BasicConceptsScreen
                     │                              │                  └─[Siguiente]→ VirtualMachineScreen
                     │                              │                                     └─[Siguiente]→ CleanInstallationScreen
                     │                              │                                                       └─[Siguiente]→ BitlockerScreen
                     │                              ├─[Máq. Virtual]→ VirtualMachineScreen
                     │                              └─[Inst. Limpia]→ CleanInstallationScreen
                     │
                     ├─[Crear imagen]──────────→ DistroSelectionScreen
                     │                              └─[Ver Detalles]→ DistroInfoScreen
                     │                                                    └─[Confirmar]→ BuildProgressScreen
                     │                                                                      ├─[Flash USB]→ UsbFlashScreen
                     │                                                                      └─[Éxito]→ OptionSelectionScreen
                     │
                     ├─[Montar imagen]─────────→ UsbFlashScreen
                     │                              └─[Éxito]→ OptionSelectionScreen
                     │
                     ├─[WSL (Windows)]─────────→ WslInstallScreen
                     │                              ├─[App Mode]→ WslAppInstallScreen
                     │                              │                └─[Éxito/Volver]→ OptionSelectionScreen
                     │                              └─[Main Mode]→ WslMainInstallScreen
                     │                                               └─[Volver]→ OptionSelectionScreen
                     │   [WSL (Linux)] → Popup informativo
                     │
                     ├─[Documentación]─────────→ DocumentationScreen
                     │                              └─[Volver]→ OptionSelectionScreen
                     │
                     └─[Acerca de]─────────────→ AboutScreen
                                                     └─[Volver]→ OptionSelectionScreen
```
