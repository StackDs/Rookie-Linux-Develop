# ISO Creation Flow

## Summary

`build_iso.sh` transforms an official Linux ISO into a fully automated ISO. The process consists of **injecting files** into the ISO without unpacking it completely, modifying only the necessary files with `xorriso`.

---

## Strategies per distribution

Each distribution family has a different installer, so different automation mechanisms are used:

| Distribution | Installer | Mechanism | Configuration file |
|---|---|---|---|
| **Ubuntu** | Subiquity | Cloud-Init (autoinstall) | `user-data` + `meta-data` |
| **Linux Mint** | Ubiquity/Calamares | preseed (legacy) | `preseed.cfg` |
| **Fedora** | Anaconda | Kickstart | `ks.cfg` |
| **Pop!_OS** | System76 Installer | Cloud-Init | `user-data` + `meta-data` |

---

## Detailed flow by phase

### Phase 1: Preparing the content to inject

```
EXTRACT_DIR=/tmp/iso_unpacked/
├── nocloud/
│   ├── user-data    ← Cloud-Init config (Ubuntu/Pop!_OS)
│   └── meta-data    ← Empty but required by Cloud-Init
├── custom_scripts/
│   ├── scripts/     ← Full copy of scripts/ from the project
│   │   ├── install.sh
│   │   ├── core/
│   │   ├── ide_tools/
│   │   ├── languages/
│   │   └── system_utils/
│   └── assets/
│       └── wallpaper.png
└── [bootloader configuration files per distro]
```

### Phase 2: Bootloader modification

For the installation to be unattended, the GRUB boot menu is modified to pass the correct parameters to the installer.

#### Ubuntu (Cloud-Init / Subiquity)

`grub.cfg` and `loopback.cfg` are modified to add the autoinstall parameters:

```
# Before:
linux /casper/vmlinuz --- quiet splash

# After:
linux /casper/vmlinuz autoinstall ds=nocloud\;s=/cdrom/nocloud/ --- quiet splash
```

The Subiquity installer detects the `ds=nocloud` parameter and reads the configuration from `/cdrom/nocloud/user-data`.

#### Fedora (Kickstart / Anaconda)

`grub.cfg`, `grub2/grub.cfg`, `isolinux.cfg` and the EFI FAT image are modified to add the `inst.ks` parameter:

```
# Before:
inst.stage2=hd:LABEL=Fedora-WS-Live-41-x86_64

# After:
inst.stage2=hd:LABEL=Fedora-WS-Live-41-x86_64 inst.ks=hd:LABEL=Fedora-WS-Live-41-x86_64:/ks.cfg
```

> ⚠️ Injection into the EFI FAT image (`eltorito_img2_uefi.img`) requires `mcopy` from the `mtools` package. Without this, Fedora's EFI boot ignores the kickstart.

#### Linux Mint

Mint uses the Ubiquity installer (derived from Debian), which accepts `preseed.cfg` files. The bootloader is modified to add:

```
preseed/file=/cdrom/preseed.cfg
```

#### Pop!_OS

Pop!_OS uses a Subiquity-derived installer, compatible with Cloud-Init. The flow is identical to Ubuntu with `ds=nocloud`.

---

### Phase 3: Injection with xorriso

Repackaging the ISO is done with `xorriso`, preserving both BIOS (MBR) and UEFI boot capabilities.

```bash
xorriso -as mkisofs \
  -r -V "Rookie-Linux" \
  -o "output/distro/rookielinux.iso" \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
  -partition_offset 16 \
  -b isolinux/isolinux.bin -c isolinux/boot.cat \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
  -isohybrid-gpt-basdat \
  /tmp/iso_unpacked
```

> The exact flags vary by distribution. Pop!_OS requires an additional squashfs unpacking process to inject the wallpaper and first-boot scripts.

---

### Phase 4: First-boot scripts (Ubuntu/Pop!_OS)

For Ubuntu and Pop!_OS, in addition to automating the installation, "first-boot scripts" are configured to run the first time the user logs into the newly installed system.

**Key files:**
- `rookie-firstboot.sh` — Main script that calls `install.sh` on the installed system.
- `rookie-terminal-wrapper.sh` — Opens a visible terminal for the user to see the progress.
- `rookie-firstboot.desktop` — XDG Autostart entry that triggers the script at boot.

The first boot flow is:
```
User Login
       │
       ▼
XDG Autostart executes rookie-firstboot.desktop
       │
       ▼
Opens terminal with rookie-terminal-wrapper.sh
       │
       ▼
Executes install.sh (installs IDEs, languages, etc.)
       │
       ▼
verify_installation.sh confirms everything is OK
       │
       ▼
The .desktop is removed so it doesn't run again
```

---

## Reporting Protocols to Frontend

The build script uses `stdout` to communicate with the Python frontend. The frontend parses each line looking for:

| Pattern in stdout | Action in GUI |
|---|---|
| `XX%` or `XX.X%` | Updates the progress bar to the indicated value |
| `Desempaquetando squashfs` (Unpacking) | Phase 1/3, bar scales from 0% to 25% |
| `Reempaquetando squashfs` (Repackaging) | Phase 2/3, bar scales from 25% to 75% |
| `Generando nueva ISO` (Generating) | Phase 3/3, bar scales from 75% to 100% |
| `exitosa` (successful) | Process completed successfully |
| `[FATAL_ERROR]` | Critical error — show error popup |
