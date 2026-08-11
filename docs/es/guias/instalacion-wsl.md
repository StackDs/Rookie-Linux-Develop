# Instalador de WSL (Windows Subsystem for Linux)

Esta guía explica cómo funciona el flujo de instalación de WSL integrado en la aplicación (pantalla `WslInstallScreen`) para los usuarios de Windows que necesitan construir ISOs.

---

## ¿Por qué un instalador de WSL?

Rookie Linux Develop requiere herramientas exclusivas de Linux (`xorriso` y `squashfs-tools`) para manipular y reconstruir la imagen ISO. Para permitir que los usuarios de Windows generen la ISO directamente desde su sistema operativo principal, la aplicación instala y configura de forma automatizada un subsistema Linux (Ubuntu) usando WSL (Windows Subsystem for Linux).

## Arquitectura de la Instalación: El Flujo en Dos Fases

Instalar WSL en un sistema Windows limpio requiere un reinicio obligatorio del sistema operativo después de habilitar las características subyacentes (Plataforma de máquina virtual). Por lo tanto, el proceso de instalación se dividió en dos fases secuenciales, controladas enteramente por el frontend:

### Fase 1: Habilitación de características
1. El usuario hace clic en "Instalar WSL".
2. La aplicación ejecuta de forma silenciosa e interactiva el comando:
   ```powershell
   wsl --install --no-distribution
   ```
3. Acto seguido, se invoca PowerShell para habilitar la característica "VirtualMachinePlatform":
   ```powershell
   Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
   ```
4. La aplicación informa al usuario que **debe reiniciar su PC** y le proporciona un botón para hacerlo inmediatamente o posponerlo.

### Fase 2: Instalación de la distribución (Post-Reinicio)
Una vez que el usuario reinicia su máquina y vuelve a abrir la aplicación:
1. La pantalla de instalación verifica el estado de WSL ejecutando `wsl --status`.
2. Si detecta que las características ya están activadas pero no hay sistema, inicia automáticamente la segunda fase, que descarga e instala la distribución "Ubuntu":
   ```powershell
   wsl --install -d Ubuntu
   ```
3. Finalmente, la aplicación ejecuta comandos dentro del nuevo entorno WSL para actualizar repositorios (`apt update`) e instalar las dependencias clave para la app (`xorriso` y `squashfs-tools`).

---

## Validaciones Automáticas y Monitoreo

Para asegurar que la instalación no falle o se quede colgada, el sistema ejecuta verificaciones en tiempo real:

- **Detección de comandos:** Antes de empezar, verifica si el comando `wsl` está disponible en el `PATH` del usuario.
- **Monitoreo de estado (`is_wsl_installed()`)**: Ejecuta un polling continuo que revisa si la distribución predeterminada está configurada y si responde a comandos básicos.
- **Ejecución asíncrona (Background Threads):** Todos los comandos de PowerShell y WSL se ejecutan en un thread separado (`threading.Thread`). Esto captura `stdout` y `stderr` mediante `subprocess.Popen`, evitando bloquear la interfaz gráfica (GUI) de `CustomTkinter` y permitiendo imprimir una consola en tiempo real en la pantalla.
