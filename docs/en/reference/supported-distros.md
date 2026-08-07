# Supported Distributions

## Summary

| Distribution | Default Version | Installer | Automation Method | Variants |
|---|---|---|---|---|
| **Ubuntu** | 24.04 LTS | Subiquity | Cloud-Init (autoinstall) | Desktop (amd64) |
| **Linux Mint** | 22.1 | Ubiquity/Calamares | preseed.cfg | Cinnamon (64bit) |
| **Fedora** | 41 | Anaconda | Kickstart (ks.cfg) | Workstation Live (x86_64) |
| **Pop!_OS** | 24.04 | System76 Installer | Cloud-Init (autoinstall) | Generic (Intel/AMD), NVIDIA |

---

## Ubuntu

### Technical details

| Field | Value |
|---|---|
| Default Version | 24.04 LTS (Noble Numbat) |
| Flavor | Desktop |
| Architecture | amd64 |
| Download mirror | `https://releases.ubuntu.com/24.04/` |
| URL Resolution | Dynamic scraping of the mirror index |
| Installer type | Subiquity (the new installer since Ubuntu 20.04) |
| Automation | Cloud-Init (`ds=nocloud`, `user-data` and `meta-data` files) |
| GRUB modification | `grub.cfg` + `loopback.cfg` (both must be modified) |
| First-boot scripts | ✅ Yes (via `rookie-firstboot.desktop`) |

### Configuration variables

```bash
UBUNTU_VERSION="24.04"    # Ubuntu version
UBUNTU_FLAVOR="desktop"   # Flavor: desktop, server, etc.
UBUNTU_ARCH="amd64"       # Architecture
UBUNTU_MIRROR="https://releases.ubuntu.com/24.04/"
```

### Special notes

- Ubuntu detects Cloud-Init during boot if the kernel parameter includes `autoinstall ds=nocloud\;s=/cdrom/nocloud/`.
- The `/cdrom/nocloud/` directory is mapped to the ISO root when booting from USB.
- The `user-data` file must include the `late-commands` section to copy the installation scripts to the target system before the first boot.

---

## Linux Mint

### Technical details

| Field | Value |
|---|---|
| Default Version | 22.1 |
| Edition | Cinnamon |
| Architecture | 64bit |
| Download mirror | `https://mirrors.edge.kernel.org/linuxmint/stable/` |
| URL Resolution | Static URL built with version variables |
| Installer type | Ubiquity (derived from Debian Installer) |
| Automation | preseed.cfg |
| GRUB modification | `grub.cfg` (add `preseed/file=/cdrom/preseed.cfg`) |
| First-boot scripts | ✅ Yes (via cron or preseed `late_command`) |

### Configuration variables

```bash
MINT_VERSION="22.1"       # Mint version
MINT_EDITION="cinnamon"   # Edition: cinnamon, mate, xfce
MINT_ARCH="64bit"         # Architecture
```

### Special notes

- Mint ISOs have a predictable filename: `linuxmint-{VERSION}-{EDITION}-{ARCH}.iso`.
- Mint's preseed is compatible with Ubuntu/Debian's, though some Ubiquity-specific options may differ.

---

## Fedora

### Technical details

| Field | Value |
|---|---|
| Default Version | 41 |
| Edition | Workstation Live |
| Architecture | x86_64 |
| Download mirror | `https://download.fedoraproject.org/pub/fedora/linux/releases/41/` |
| URL Resolution | Dynamic scraping of the mirror directory |
| Installer type | Anaconda |
| Automation | Kickstart (ks.cfg) |
| GRUB modification | `grub.cfg`, `grub2/grub.cfg`, `isolinux.cfg` + EFI FAT image |
| First-boot scripts | ✅ Yes (via `%post` section of kickstart) |

### Configuration variables

```bash
FEDORA_VERSION="41"
FEDORA_PRODUCT="Workstation"
FEDORA_ARCH="x86_64"
FEDORA_MIRROR="https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/"
```

### Special notes

> ⚠️ **Fedora is the most complex distribution to automate** due to:
> 1. It has three bootloader files that must be modified: `grub.cfg`, `grub2/grub.cfg`, and `isolinux.cfg`.
> 2. The EFI FAT image (`eltorito_img2_uefi.img`) must also be patched with `mcopy`.
> 3. The `inst.ks=` parameter must correctly reference the disk LABEL, which can vary.

---

## Pop!_OS

### Technical details

| Field | Value |
|---|---|
| Default Version | 24.04 |
| Architecture | amd64 |
| Download source | JSON API from `api.pop-os.org` |
| Installer type | System76 Installer (based on Subiquity) |
| Automation | Cloud-Init (compatible with Ubuntu) |
| NVIDIA Variant | Separate ISO with pre-installed NVIDIA drivers |
| First-boot scripts | ✅ Yes |

### Configuration variables

```bash
POP_VERSION="24.04"
POP_ARCH="amd64"
POP_VARIANT="generic"  # or "nvidia"
POP_API_URL="https://api.pop-os.org/builds/24.04/generic?arch=amd64"
```

### Variants

- **Generic**: Compatible with Intel and AMD. Recommended for most computers.
- **NVIDIA**: Includes proprietary NVIDIA drivers. Selectable in the GUI via a dialog.

The GUI asks the user if they have an NVIDIA card before starting the download and adjusts the `POP_VARIANT` variable accordingly.

---

## Add or modify versions

To change a distribution's default version, modify the variables in `builder/download_iso.sh`:

```bash
# Example: change Ubuntu to 24.10
UBUNTU_VERSION="${UBUNTU_VERSION:-24.10}"
```

The variables can be overridden from the environment, allowing you to change versions without modifying the script.
