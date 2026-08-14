# Instalador de WSL (Windows Subsystem for Linux)

Esta guía explica cómo funciona el flujo de instalación de WSL integrado en la aplicación para los usuarios de Windows. Debido a la evolución de la aplicación, el sistema de instalación se ha dividido en dos modos distintos accesibles desde la pantalla `WslInstallScreen`.

---

## ¿Por qué un instalador de WSL?

Rookie Linux Develop requiere herramientas exclusivas de Linux (`xorriso`, `squashfs-tools`, etc.) para manipular y reconstruir la imagen ISO. Para permitir que los usuarios de Windows generen la ISO de manera nativa sin máquinas virtuales complejas, la aplicación se apoya en un subsistema Linux usando WSL. 

## Los Dos Modos de Instalación

El sistema ahora ofrece dos enfoques, separados en dos pantallas independientes:

### Modo 1: Instalación para usar la app (`WslAppInstallScreen`)
Este es un flujo simplificado, ideal para usuarios que solo quieren construir su imagen ISO de Rookie Linux y no les interesa usar Linux en Windows para otras cosas.
Se divide en dos pasos manuales (debido a la necesidad de reiniciar):

1. **Fase 1: Habilitar WSL**: Ejecuta de forma silenciosa e interactiva el comando:
   ```powershell
   wsl --install --no-distribution
   ```
   Tras esto, la app advierte mediante un cuadro de diálogo que **se debe reiniciar la PC**.

2. **Fase 2: Instalar Distro (Post-Reinicio)**: Una vez reiniciado, el usuario usa este segundo paso para instalar la distribución base (Ubuntu) necesaria para las operaciones del backend sin lanzar consolas molestas.
   ```powershell
   wsl --install -d Ubuntu --no-launch
   ```

Las instalaciones cuentan con ventanas de confirmación para alertar sobre la necesidad de permisos de administrador y el tiempo requerido.

### Modo 2: WSL como sistema principal (`WslMainInstallScreen`)
Este es un panel de control avanzado para usuarios que desean explorar WSL más a fondo. 

1. **Estado del Sistema**: Muestra de forma asíncrona si WSL, WSL 2 y la virtualización están habilitados en el sistema, detectando la versión predeterminada mediante `wsl --status`.
2. **Habilitación Global**: Permite instalar WSL con un clic.
3. **Gestión de Distribuciones**: Escanea dinámicamente (`wsl -l -o` y `wsl -l -v`) para listar todas las distribuciones disponibles y aquellas ya instaladas. 
4. Permite seleccionar una o múltiples distribuciones y ponerlas en cola de instalación visual con barras de progreso interactivas basadas en simulación e hilos (threads).

---

## Validaciones Automáticas y Monitoreo

Para asegurar que la instalación sea fluida, ambas pantallas implementan mecanismos modernos:

- **Ventanas de confirmación (msg_ask_yes_no)**: Previenen acciones destructivas o instalaciones accidentales.
- **Redirección automática**: Tras completar los procesos en el Modo App, el usuario es devuelto al menú principal para evitar interacciones vacías.
- **Ejecución asíncrona (Background Threads)**: Todos los comandos de PowerShell (con `RunAs` o `Start-Process`) se ejecutan en un thread separado, evitando que la GUI de `CustomTkinter` se congele durante instalaciones prolongadas.
