# Cómo agregar una nueva distribución

Esta guía explica los pasos necesarios para integrar una nueva distribución de Linux en Rookie Linux Develop.

---

## Paso 1: Decidir la estrategia de automatización

Antes de crear archivos, necesitas saber qué instalador usa la distro objetivo:

| Instalador | Configuración | Distros que lo usan |
|---|---|---|
| **Subiquity** | Cloud-Init (`user-data`) | Ubuntu 20.04+, Pop!_OS |
| **Ubiquity** | preseed.cfg | Ubuntu 18.04, Linux Mint (Cinnamon) |
| **Anaconda** | Kickstart (`ks.cfg`) | Fedora, RHEL, CentOS |
| **Calamares** | Script personalizado | Manjaro, Garuda, EndeavourOS |

> 💡 Si la distro usa Calamares, la automatización es más compleja y requiere modificar el archivo `settings.conf` de Calamares.

---

## Paso 2: Agregar la lógica de descarga

Edita `builder/download_iso.sh` y añade un nuevo `case` en la función `resolve_iso_source()`:

```bash
mi_distro)
    MI_DISTRO_VERSION="${MI_DISTRO_VERSION:-1.0}"
    ISO_NAME="${ISO_NAME:-mi-distro-${MI_DISTRO_VERSION}-x86_64.iso}"
    ISO_URL="${ISO_URL:-https://mirror.mi-distro.org/releases/${MI_DISTRO_VERSION}/${ISO_NAME}}"
    ;;
```

> 💡 Si la URL de descarga cambia con cada versión (como Ubuntu o Fedora), añade lógica de scraping. Consulta los bloques de `ubuntu` o `fedora` como referencia.

---

## Paso 3: Crear la carpeta de plantillas

Crea la carpeta de plantillas con el nombre exacto que usarás internamente:

```bash
mkdir builder/templates/mi_distro
```

### Para distribuciones basadas en Cloud-Init (Ubuntu/Pop!_OS):

Crea `builder/templates/mi_distro/user-data`:

```yaml
#cloud-config
autoinstall:
  version: 1
  locale: es_ES
  keyboard:
    layout: latam
  identity:
    hostname: rookie-linux
    username: developer
    password: "$6$..."  # Contraseña hasheada con openssl passwd -6
  storage:
    layout:
      name: lvm
  late-commands:
    - cp -r /cdrom/custom_scripts /target/opt/rookie
    - chmod +x /target/opt/rookie/install.sh
    - echo "@reboot root bash /opt/rookie/install.sh" >> /target/etc/cron.d/rookie-setup
```

Crea `builder/templates/mi_distro/meta-data` (puede estar vacío):

```yaml
instance-id: rookie-linux
```

### Para distribuciones con Kickstart (Fedora):

Crea `builder/templates/mi_distro/ks.cfg`:

```kickstart
#version=RHEL9
lang es_ES.UTF-8
keyboard --xlayouts='latam'
timezone America/Bogota --utc
rootpw --lock
user --name=developer --password=rookielinux --groups=wheel

%packages
@^workstation-product-environment
%end

%post
cp -r /run/install/repo/custom_scripts /opt/rookie
chmod +x /opt/rookie/install.sh
%end
```

---

## Paso 4: Agregar la lógica de construcción en `build_iso.sh`

Añade un nuevo bloque `elif` en `build_iso.sh` para manejar la inyección específica de tu distro:

```bash
elif [ "$ISO_DISTRO" = "mi_distro" ]; then
    echo "=> Preparando configuracion Cloud-Init para Mi Distro..."
    cp "$TEMPLATES_DIR/user-data" "$EXTRACT_DIR/nocloud/"
    cp "$TEMPLATES_DIR/meta-data" "$EXTRACT_DIR/nocloud/"
    
    echo "=> Extrayendo y modificando GRUB..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/grub.cfg "$EXTRACT_DIR/grub.cfg" 2>/dev/null || true
    sed -i 's/---/autoinstall ds=nocloud\\;s=\/cdrom\/nocloud\/ ---/g' "$EXTRACT_DIR/grub.cfg"
```

---

## Paso 5: Registrar la distro en el frontend

### 5a. En `DistroSelectionScreen`
Añade la nueva distro a la lista de opciones del radio button:

```python
# En frontend/screens/linux_concepts/distro_selection_screen.py
self.distros = ["Ubuntu", "Linux Mint", "Fedora", "Pop!_OS", "Mi Distro"]
```

### 5b. En `DistroInfoScreen`
Añade el texto informativo y el mapeo de carpeta:

```python
self.folder_map = {
    ...
    "Mi Distro": "mi_distro_screenshots",
}

self.distro_texts = {
    ...
    "Mi Distro": (
        "> Analizando: Mi Distro\n\n"
        "Descripción de la distro..."
    )
}
```

### 5c. En `BuildProgressScreen`
Añade el mapeo de nombre a identificador interno:

```python
distro_map = {
    ...
    "Mi Distro": "mi_distro",
}
```

---

## Paso 6: Agregar capturas de pantalla (opcional)

Crea la carpeta `assets/DistrosScreenShots/mi_distro/` y añade tres imágenes:
- `escritorio.png` — Vista del escritorio principal
- `gestor.png` — Gestor de paquetes o archivos
- `terminal.png` — Terminal abierta

Las imágenes se muestran en `DistroInfoScreen` cuando el usuario selecciona esta distro.

---

## Paso 7: Probar

1. Ejecuta `python3 frontend/main.py` y verifica que aparece la nueva distro en el selector.
2. Prueba el flujo completo con la descarga (puede tardar varios minutos).
3. Si tienes una VM disponible, arranca la ISO generada para verificar que la instalación desatendida funciona.
