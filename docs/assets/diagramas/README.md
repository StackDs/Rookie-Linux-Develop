# Diagramas de Arquitectura

Esta carpeta almacena diagramas y esquemas visuales de la arquitectura del proyecto.

## Diagrama de flujo general (texto)

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO FINAL                        │
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
│  download_iso.sh ──► Descarga ISO oficial               │
│                                   │                     │
│                                   ▼                     │
│  build_iso.sh ────► Inyecta preseed/kickstart           │
│                  ──► Copia scripts/                      │
│                  ──► Reempaqueta con xorriso             │
│                                   │                     │
│                                   ▼                     │
│                     output/{distro}/imagen.iso          │
└─────────────────────────────────────────────────────────┘
                       │ JSON temporal polling
                       ▼
┌─────────────────────────────────────────────────────────┐
│           FLASHER WORKER (Proceso elevado)              │
│                                                         │
│  flasher_worker_linux.py  ──► wipefs + parted + dd      │
│  flasher_worker_windows.py ─► DISKPART + dd             │
│                                                         │
│  Comunica progreso vía: /tmp/rookie_flash_progress.json │
└─────────────────────────────────────────────────────────┘
```

## Relación entre módulos

```
main.py
  └── App (CTk)
        ├── Banner (botones globales)
        └── Container (pantallas apiladas)
              ├── StartScreen
              ├── OptionSelectionScreen
              ├── InfoScreen
              ├── ExplanationScreen
              ├── DistroSelectionScreen ──► distro_var (estado compartido)
              ├── DistroInfoScreen     ◄─── lee distro_var
              ├── BuildProgressScreen  ◄─── lee distro_var
              │     └── lanza: download_iso.sh → build_iso.sh
              ├── UsbFlashScreen
              │     └── lanza: flasher_worker_{os}.py (elevado)
              ├── BasicConceptsScreen
              ├── VirtualMachineScreen
              ├── CleanInstallationScreen
              ├── BitlockerScreen
              ├── WslInstallScreen
              ├── InstructionsScreen
              ├── DocumentationScreen
              └── AboutScreen
```

## Agregar nuevos diagramas

Para agregar diagramas visuales (PNG, SVG, etc.) a esta carpeta, nómbralos descriptivamente:

- `flujo-iso-ubuntu.png` — Flujo específico para Ubuntu
- `arquitectura-general.svg` — Diagrama SVG de la arquitectura completa
- `navegacion-pantallas.png` — Captura del mapa de navegación
