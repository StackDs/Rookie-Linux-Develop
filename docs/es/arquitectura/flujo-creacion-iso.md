# Flujo de Creación de ISO

## Resumen

`build_iso.sh` transforma una ISO oficial de Linux en una ISO completamente automatizada. El proceso consiste en **inyectar archivos** dentro de la ISO sin desempaquetarla completamente, modificando solo los archivos necesarios con `xorriso`.

---

## Estrategias por distribución

Cada familia de distribuciones tiene un instalador distinto, por lo que se usan mecanismos de automatización diferentes:

| Distribución | Instalador | Mecanismo | Archivo de configuración |
|---|---|---|---|
| **Ubuntu** | Subiquity | Cloud-Init (autoinstall) | `user-data` + `meta-data` |
| **Linux Mint** | Ubiquity/Calamares | preseed (legacy) | `preseed.cfg` |
| **Fedora** | Anaconda | Kickstart | `ks.cfg` |
| **Pop!_OS** | Sistema76 Installer | Cloud-Init | `user-data` + `meta-data` |

---

## Flujo detallado por fase

### Fase 1: Preparación del contenido a inyectar

```
EXTRACT_DIR=/tmp/iso_unpacked/
├── nocloud/
│   ├── user-data    ← Configuración Cloud-Init (Ubuntu/Pop!_OS)
│   └── meta-data    ← Vacío pero requerido por Cloud-Init
├── custom_scripts/
│   ├── scripts/     ← Copia completa de scripts/ del proyecto
│   │   ├── install.sh
│   │   ├── core/
│   │   ├── ide_tools/
│   │   ├── languages/
│   │   └── system_utils/
│   └── assets/
│       └── wallpaper.png
└── [archivos de configuración del bootloader por distro]
```

### Fase 2: Modificación del bootloader

Para que la instalación sea desatendida, se modifica el menú de arranque GRUB para que pase los parámetros correctos al instalador.

#### Ubuntu (Cloud-Init / Subiquity)

Se modifican `grub.cfg` y `loopback.cfg` para añadir los parámetros de autoinstalación:

```
# Antes:
linux /casper/vmlinuz --- quiet splash

# Después:
linux /casper/vmlinuz autoinstall ds=nocloud\;s=/cdrom/nocloud/ --- quiet splash
```

El instalador Subiquity detecta el parámetro `ds=nocloud` y lee la configuración desde `/cdrom/nocloud/user-data`.

#### Fedora (Kickstart / Anaconda)

Se modifican `grub.cfg`, `grub2/grub.cfg`, `isolinux.cfg` y la imagen FAT de EFI para añadir el parámetro `inst.ks`:

```
# Antes:
inst.stage2=hd:LABEL=Fedora-WS-Live-41-x86_64

# Después:
inst.stage2=hd:LABEL=Fedora-WS-Live-41-x86_64 inst.ks=hd:LABEL=Fedora-WS-Live-41-x86_64:/ks.cfg
```

> ⚠️ La inyección en la imagen EFI FAT (`eltorito_img2_uefi.img`) requiere `mcopy` del paquete `mtools`. Sin esto, el arranque EFI de Fedora ignora el kickstart.

#### Linux Mint

Mint usa el instalador Ubiquity (derivado de Debian), que acepta archivos `preseed.cfg`. El bootloader se modifica para añadir:

```
preseed/file=/cdrom/preseed.cfg
```

#### Pop!_OS

Pop!_OS usa un instalador derivado de Subiquity, compatible con Cloud-Init. El flujo es idéntico al de Ubuntu con `ds=nocloud`.

---

### Fase 3: Inyección con xorriso

El reempaquetado de la ISO se realiza con `xorriso`, preservando las capacidades de arranque tanto BIOS (MBR) como UEFI.

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

> Las flags exactas varían por distribución. Pop!_OS requiere un proceso adicional de desempaquetado del squashfs para inyectar el wallpaper y los scripts de primer arranque.

---

### Fase 4: Scripts de primer arranque (Ubuntu/Pop!_OS)

Para Ubuntu y Pop!_OS, además de automatizar la instalación, se configuran "scripts de primer arranque" que se ejecutan la primera vez que el usuario inicia sesión en el sistema recién instalado.

**Archivos clave:**
- `rookie-firstboot.sh` — Script principal que llama a `install.sh` del sistema instalado.
- `rookie-terminal-wrapper.sh` — Abre una terminal visible para que el usuario vea el progreso.
- `rookie-firstboot.desktop` — Entrada de Autostart XDG que dispara el script al arranque.

El flujo del primer arranque es:
```
Login del usuario
       │
       ▼
XDG Autostart ejecuta rookie-firstboot.desktop
       │
       ▼
Abre terminal con rookie-terminal-wrapper.sh
       │
       ▼
Ejecuta rookie-firstboot.sh (Inicia loop keep-alive de sudo)
       │
       ▼
Ejecuta install.sh (instala IDEs, lenguajes, etc.)
       │
       ▼
Se elimina el .desktop para que no vuelva a ejecutarse
       │
       ▼
Ejecuta rookie-verify.sh en la MISMA terminal
       │
       ├──► appearance.sh (Aplica fondos y temas oscuros)
       │
       └──► verify_installation.sh (Confirma que todo está OK)
```

---

## Protocolos de reporte al frontend

El script de construcción usa `stdout` para comunicarse con el frontend Python. El frontend analiza cada línea buscando:

| Patrón en stdout | Acción en la GUI |
|---|---|
| `XX%` o `XX.X%` | Actualiza la barra de progreso al valor indicado |
| `Desempaquetando squashfs` | Fase 1/3, barra escala de 0% a 25% |
| `Reempaquetando squashfs` | Fase 2/3, barra escala de 25% a 75% |
| `Generando nueva ISO` | Fase 3/3, barra escala de 75% a 100% |
| `exitosa` | Proceso completado con éxito |
| `[FATAL_ERROR]` | Error crítico — mostrar popup de error |
