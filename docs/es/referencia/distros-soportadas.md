# Distribuciones Soportadas

## Resumen

| Distribución | Versión por defecto | Instalador | Método de automatización | Variantes |
|---|---|---|---|---|
| **Ubuntu** | 24.04 LTS | Subiquity | Cloud-Init (autoinstall) | Desktop (amd64) |
| **Linux Mint** | 22.1 | Ubiquity/Calamares | preseed.cfg | Cinnamon (64bit) |
| **Fedora** | 41 | Anaconda | Kickstart (ks.cfg) | Workstation Live (x86_64) |
| **Pop!_OS** | 24.04 | Sistema76 Installer | Cloud-Init (autoinstall) | Generic (Intel/AMD), NVIDIA |

---

## Ubuntu

### Detalles técnicos

| Campo | Valor |
|---|---|
| Versión por defecto | 24.04 LTS (Noble Numbat) |
| Sabor | Desktop |
| Arquitectura | amd64 |
| Mirror de descarga | `https://releases.ubuntu.com/24.04/` |
| Resolución de URL | Scraping dinámico del índice del mirror |
| Tipo de instalador | Subiquity (el nuevo instalador desde Ubuntu 20.04) |
| Automatización | Cloud-Init (`ds=nocloud`, archivos `user-data` y `meta-data`) |
| Modificación de GRUB | `grub.cfg` + `loopback.cfg` (ambos deben modificarse) |
| Scripts de primer arranque | ✅ Sí (via `rookie-firstboot.desktop`) |

### Variables de configuración

```bash
UBUNTU_VERSION="24.04"    # Versión de Ubuntu
UBUNTU_FLAVOR="desktop"   # Sabor: desktop, server, etc.
UBUNTU_ARCH="amd64"       # Arquitectura
UBUNTU_MIRROR="https://releases.ubuntu.com/24.04/"
```

### Notas especiales

- Ubuntu detecta Cloud-Init durante el arranque si el parámetro del kernel incluye `autoinstall ds=nocloud\;s=/cdrom/nocloud/`.
- El directorio `/cdrom/nocloud/` se mapea a la raíz de la ISO al arrancar desde USB.
- El archivo `user-data` debe incluir la sección `late-commands` para copiar los scripts de instalación al sistema objetivo antes del primer arranque.

---

## Linux Mint

### Detalles técnicos

| Campo | Valor |
|---|---|
| Versión por defecto | 22.1 |
| Edición | Cinnamon |
| Arquitectura | 64bit |
| Mirror de descarga | `https://mirrors.edge.kernel.org/linuxmint/stable/` |
| Resolución de URL | URL estática construida con variables de versión |
| Tipo de instalador | Ubiquity (derivado de Debian Installer) |
| Automatización | preseed.cfg |
| Modificación de GRUB | `grub.cfg` (añadir `preseed/file=/cdrom/preseed.cfg`) |
| Scripts de primer arranque | ✅ Sí (via cron o preseed `late_command`) |

### Variables de configuración

```bash
MINT_VERSION="22.1"       # Versión de Mint
MINT_EDITION="cinnamon"   # Edición: cinnamon, mate, xfce
MINT_ARCH="64bit"         # Arquitectura
```

### Notas especiales

- Las ISOs de Mint tienen un nombre de archivo predecible: `linuxmint-{VERSION}-{EDITION}-{ARCH}.iso`.
- El preseed de Mint es compatible con el de Ubuntu/Debian, aunque algunas opciones específicas de Ubiquity pueden diferir.

---

## Fedora

### Detalles técnicos

| Campo | Valor |
|---|---|
| Versión por defecto | 41 |
| Edición | Workstation Live |
| Arquitectura | x86_64 |
| Mirror de descarga | `https://download.fedoraproject.org/pub/fedora/linux/releases/41/` |
| Resolución de URL | Scraping dinámico del directorio del mirror |
| Tipo de instalador | Anaconda |
| Automatización | Kickstart (ks.cfg) |
| Modificación de GRUB | `grub.cfg`, `grub2/grub.cfg`, `isolinux.cfg` + imagen FAT EFI |
| Scripts de primer arranque | ✅ Sí (via sección `%post` del kickstart) |

### Variables de configuración

```bash
FEDORA_VERSION="41"
FEDORA_PRODUCT="Workstation"
FEDORA_ARCH="x86_64"
FEDORA_MIRROR="https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/"
```

### Notas especiales

> ⚠️ **Fedora es la distribución más compleja de automatizar** debido a:
> 1. Tiene tres archivos de bootloader que deben modificarse: `grub.cfg`, `grub2/grub.cfg`, e `isolinux.cfg`.
> 2. La imagen FAT de EFI (`eltorito_img2_uefi.img`) también debe ser parcheada con `mcopy`.
> 3. El parámetro `inst.ks=` debe referenciar correctamente el LABEL del disco, que puede variar.

---

## Pop!_OS

### Detalles técnicos

| Campo | Valor |
|---|---|
| Versión por defecto | 24.04 |
| Arquitectura | amd64 |
| Fuente de descarga | API JSON de `api.pop-os.org` |
| Tipo de instalador | Sistema76 Installer (basado en Subiquity) |
| Automatización | Cloud-Init (compatible con Ubuntu) |
| Variante NVIDIA | ISO separada con drivers NVIDIA preinstalados |
| Scripts de primer arranque | ✅ Sí |

### Variables de configuración

```bash
POP_VERSION="24.04"
POP_ARCH="amd64"
POP_VARIANT="generic"  # o "nvidia"
POP_API_URL="https://api.pop-os.org/builds/24.04/generic?arch=amd64"
```

### Variantes

- **Generic**: Compatible con Intel y AMD. Recomendado para la mayoría de equipos.
- **NVIDIA**: Incluye drivers NVIDIA propietarios. Seleccionable en la GUI mediante un diálogo.

La GUI pregunta al usuario si tiene tarjeta NVIDIA antes de iniciar la descarga y ajusta la variable `POP_VARIANT` en consecuencia.

---

## Agregar o modificar versiones

Para cambiar la versión por defecto de una distribución, modifica las variables en `builder/download_iso.sh`:

```bash
# Ejemplo: cambiar Ubuntu a 24.10
UBUNTU_VERSION="${UBUNTU_VERSION:-24.10}"
```

Las variables son sobreescribibles desde el entorno, lo que permite cambiar versiones sin modificar el script.
