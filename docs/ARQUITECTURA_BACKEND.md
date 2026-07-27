# Arquitectura y Lógica de Negocio: Rookie Linux

Este documento detalla la estructura interna y la lógica de negocio detrás de la construcción de las imágenes ISO personalizadas de **Rookie Linux**. Se omite deliberadamente la capa de interfaz gráfica para centrarse exclusivamente en el motor de construcción (Builder), inyección de código y automatización post-instalación.

---

## 1. El Motor de Construcción (Directorio `/builder`)

Aquí es donde ocurre el proceso de desarmar una ISO oficial de Linux, inyectarle nuestros componentes y volverla a armar. Todo esto se ejecuta dentro de un contenedor Docker para aislar las dependencias y no contaminar el sistema host.

### `build_iso.sh`
Es el script maestro y el más complejo de todo el proyecto. Su flujo de trabajo es el siguiente:
1. **Identificación:** Detecta qué distribución se está construyendo (Ubuntu, Pop!_OS, Mint o Fedora).
2. **Extracción Base:** Usa `xorriso` para desarmar la ISO original y extraer los archivos de arranque (GRUB, ISOLINUX) y la imagen del sistema comprimido (`filesystem.squashfs`).
3. **Inyección en el Sistema de Archivos (SquashFS):** 
   - *Para Pop!_OS y Mint:* Descomprime el sistema de archivos principal (`unsquashfs`), copia silenciosamente todos nuestros scripts de instalación a `/opt/rookie-scripts/`, inyecta un acceso directo de inicio automático en `/etc/xdg/autostart/`, y vuelve a comprimir todo el sistema base (`mksquashfs`).
4. **Parcheo de Gestores de Arranque (GRUB):** Modifica los archivos `.cfg` del menú de arranque original. Reemplaza textos como "Install Fedora" o "Try Pop_OS" por "Instalador Automático de Rookie Linux".
5. **Reconstrucción (Remasterización):** Vuelve a empaquetar todos los archivos en un nuevo archivo `.iso` booteable compatible con UEFI y BIOS Legacy, inyectando las firmas de arranque (El Torito) para que la USB sea arrancable en cualquier PC moderno.

### `download_iso.sh`
Se encarga de descargar las ISOs originales desde los servidores oficiales de Ubuntu, System76 (Pop!_OS), Mint o Fedora si no se encuentran en la carpeta de descargas local.

### Directorio `/builder/templates`
Contiene las piezas de configuración específicas para "engañar" o automatizar el instalador de cada distribución:
* **`/mint`, `/popos` y `/ubuntu`:**
  * `rookie-firstboot.sh` y `rookie-terminal-wrapper.sh`: Scripts que se ejecutan automáticamente la primera vez que el usuario inicia sesión en el escritorio gráfico. Son los responsables de abrir una terminal transparente que pide la contraseña y lanza la instalación de software pesado (IDEs, Docker, lenguajes, etc.).
  * `rookie-firstboot.desktop`: El archivo que enlaza con el sistema de Auto-Arranque de GNOME/Cinnamon para invocar los scripts anteriores.
* **`/fedora`:**
  * `ks.cfg` (Kickstart): Fedora no permite desempaquetar su sistema base tan fácilmente, así que usamos este archivo de automatización. El archivo ha sido configurado meticulosamente para usar la orden `liveimg` (instalar usando la imagen USB local, no internet), iniciar el instalador de Anaconda en modo `graphical`, y en su bloque `%post` inyectar el sistema de auto-arranque gráfico al sistema recién instalado.

---

## 2. Los Scripts de Instalación (Directorio `/scripts`)

Una vez que el usuario ha instalado el sistema operativo en su disco duro y reinicia su computadora, la lógica de negocio pasa el control a este directorio. Estos scripts conforman la batería de instalación que convierte una distro "vainilla" en la "Rookie Linux Developer Edition".

### `install.sh`
El orquestador de software. Es llamado por la terminal de primer arranque y se encarga de ejecutar de manera secuencial (Paso 1, Paso 2, etc.) todos los demás scripts modulares de este directorio. Controla que no se detenga toda la instalación si una sola herramienta falla.

### Scripts Modulares (Archivos de Categoría)
* `appearance.sh`: Cambia temas, íconos (Papirus) y fuentes (Fira Code) para darle estética hacker.
* `git.sh`: Instala control de versiones y el CLI de GitHub.
* `python.sh`, `c_cpp.sh`, `node.sh`, `java.sh`, `dotnet.sh`: Instalan los compiladores, SDKs y gestores de paquetes para los diferentes lenguajes de programación.
* `ide.sh` y `editors.sh`: Descargan e instalan editores de código pesado como VS Code, IntelliJ IDEA, NeoVim, etc.
* `docker.sh`: Configura el motor de contenedores y añade al usuario al grupo `docker` para que no necesite usar `sudo` cada vez.
* `databases.sh` y `database_tools.sh`: Instalan motores (PostgreSQL, MySQL, MongoDB, Redis) y clientes visuales (pgAdmin, DBeaver, MongoDB Compass).

### `verify_installation.sh`
Es el último script en ejecutarse. Una vez finalizada la instalación técnica, este script hace dos cosas clave:
1. Comprueba una por una que todas las herramientas binarias (docker, node, python, etc.) respondan correctamente y genera un reporte en verde/rojo para el usuario.
2. Como se ejecuta con los privilegios del usuario local (sin `sudo`), se aprovecha de este contexto para cambiar el Wallpaper del escritorio usando las APIs de GNOME/Cinnamon (`gsettings`) y coloca la marca de agua oficial de Rookie Linux de fondo. Finalmente, crea un archivo oculto `.rookie_verified` para asegurarse de no volver a ejecutarse en el siguiente reinicio.

---

## Resumen del Ciclo de Vida de la Lógica de Negocio

1. **Construcción:** El código de Python levanta el Docker -> `build_iso.sh` extrae el SO original -> Inyecta las piezas de `/templates` y los instaladores de `/scripts` -> Empaqueta una ISO nueva.
2. **Despliegue USB:** El usuario escribe la ISO en una USB (flasher) sorteando las protecciones físicas del kernel de Windows.
3. **Instalación:** El usuario arranca la USB, el GRUB modificado inicia el instalador del sistema operativo, el usuario instala el SO en su disco duro local. Durante este proceso, los archivos de la carpeta `/scripts` y `/templates` son arrastrados inadvertidamente al nuevo disco duro.
4. **Día Cero:** El usuario enciende su PC nuevo e inicia sesión. El archivo `.desktop` inyectado detecta el inicio de sesión -> Lanza la terminal wrapper -> Ejecuta `install.sh` -> Ejecuta todos los módulos de programación -> Ejecuta `verify_installation.sh` -> El escritorio de Rookie Linux está listo para programar.
