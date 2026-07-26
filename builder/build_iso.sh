#!/bin/bash
set -e

echo "=========================================="
echo "Iniciando Constructor de ISO (Docker)"
echo "=========================================="

WORKSPACE="/workspace"
ISO_DISTRO="${ISO_DISTRO:-ubuntu}"

# Normalizar variantes de Pop!_OS para rutas de templates
POP_DISTRO_ORIGINAL="$ISO_DISTRO"
case "$ISO_DISTRO" in
    popos_nvidia|popos_amd|pop-nvidia|pop-os|pop)
        TEMPLATES_DISTRO="popos"
        ;;
    *)
        TEMPLATES_DISTRO="$ISO_DISTRO"
        ;;
esac

DOWNLOAD_DIR="$WORKSPACE/downloads/iso/$ISO_DISTRO"

BUILD_DIR="$WORKSPACE/output/$ISO_DISTRO"
EXTRACT_DIR="/tmp/iso_unpacked"
TEMPLATES_DIR="$WORKSPACE/builder/templates/$TEMPLATES_DISTRO"

mkdir -p "$BUILD_DIR"

# 1. Encontrar la ISO
if [ -z "$ISO_NAME" ]; then
    ISO_PATH=$(ls -1 "$DOWNLOAD_DIR"/*.iso 2>/dev/null | head -n 1 || true)
    if [ -z "$ISO_PATH" ]; then
        echo "[ERROR] No se encontro ninguna ISO en $DOWNLOAD_DIR"
        exit 1
    fi
    ISO_NAME=$(basename "$ISO_PATH")
else
    ISO_PATH="$DOWNLOAD_DIR/$ISO_NAME"
fi

if [ ! -f "$ISO_PATH" ]; then
    echo "[ERROR] El archivo ISO no existe: $ISO_PATH"
    exit 1
fi

echo "=> Procesando ISO: $ISO_NAME"

# 2. Preparar los archivos a inyectar
rm -rf "$EXTRACT_DIR"
mkdir -p "$EXTRACT_DIR/nocloud"
mkdir -p "$EXTRACT_DIR/custom_scripts"

echo "=> Preparando scripts y recursos (Rookie-Linux-Develop)..."
cp -r "$WORKSPACE/scripts" "$EXTRACT_DIR/custom_scripts/"
cp -r "$WORKSPACE/assets" "$EXTRACT_DIR/custom_scripts/"

echo "=> Convirtiendo finales de linea Windows (CRLF) a Linux (LF)..."
find "$EXTRACT_DIR/custom_scripts/scripts/" -type f -name "*.sh" -exec sed -i 's/\r$//' {} + 2>/dev/null || true

if [ "$ISO_DISTRO" = "ubuntu" ]; then
    echo "=> Preparando configuracion Cloud-Init (Subiquity)..."
    cp "$TEMPLATES_DIR/user-data" "$EXTRACT_DIR/nocloud/"
    cp "$TEMPLATES_DIR/meta-data" "$EXTRACT_DIR/nocloud/"
    find "$EXTRACT_DIR/nocloud/" -type f -exec sed -i 's/\r$//' {} + 2>/dev/null || true

    echo "=> Extrayendo configuracion GRUB original de la ISO..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/grub.cfg "$EXTRACT_DIR/grub.cfg" 2>/dev/null || true
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/loopback.cfg "$EXTRACT_DIR/loopback.cfg" 2>/dev/null || true
    
    chmod +w "$EXTRACT_DIR/grub.cfg" "$EXTRACT_DIR/loopback.cfg" 2>/dev/null || true

    echo "=> Modificando menu de arranque GRUB (autoinstall)..."
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        sed -i 's/---/autoinstall ds=nocloud\\;s=\/cdrom\/nocloud\/ ---/g' "$EXTRACT_DIR/grub.cfg" || true
        sed -i 's/"Try or Install Ubuntu"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        sed -i 's/---/autoinstall ds=nocloud\\;s=\/cdrom\/nocloud\/ ---/g' "$EXTRACT_DIR/loopback.cfg" || true
        sed -i 's/"Try or Install Ubuntu"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/loopback.cfg" || true
    fi
elif [ "$ISO_DISTRO" = "fedora" ]; then
    echo "=> Preparando configuracion Kickstart (Anaconda)..."
    cp "$TEMPLATES_DIR/ks.cfg" "$EXTRACT_DIR/ks.cfg"
    sed -i 's/\r$//' "$EXTRACT_DIR/ks.cfg"

    echo "=> Extrayendo configuracion GRUB original de la ISO..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /EFI/BOOT/grub.cfg "$EXTRACT_DIR/efi_grub.cfg" 2>/dev/null || true
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub2/grub.cfg "$EXTRACT_DIR/grub2_grub.cfg" 2>/dev/null || true
    xorriso -osirrox on -indev "$ISO_PATH" -extract /isolinux/isolinux.cfg "$EXTRACT_DIR/isolinux.cfg" 2>/dev/null || true
    
    echo "=> Extrayendo imagenes de arranque ocultas (El Torito)..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract_boot_images "$EXTRACT_DIR/boot_images" 2>/dev/null || true
    
    chmod +w "$EXTRACT_DIR/efi_grub.cfg" "$EXTRACT_DIR/grub2_grub.cfg" "$EXTRACT_DIR/isolinux.cfg" 2>/dev/null || true

    echo "=> Modificando menu de arranque GRUB (autoinstall)..."
    for grubfile in "$EXTRACT_DIR/efi_grub.cfg" "$EXTRACT_DIR/grub2_grub.cfg"; do
        if [ -f "$grubfile" ]; then
            # Reemplazo dinamico: si usa LABEL, le pasamos el ks usando el mismo LABEL (ideal para USBs).
            sed -i 's/\(inst\.stage2=hd:LABEL=\([^ ]*\)\)/\1 inst.ks=hd:LABEL=\2:\/ks.cfg/g' "$grubfile" || true
            # Fallback por si usa cdrom
            sed -i 's/\(inst\.stage2=cdrom[^ ]*\)/\1 inst.ks=cdrom:\/ks.cfg/g' "$grubfile" || true
            
            sed -E -i "s/menuentry ['\"]Install Fedora[^'\"]*['\"]/menuentry 'Instalador Automatico de Rookie Linux'/g" "$grubfile" || true
            sed -E -i "s/title .*Install Fedora.*/title Instalador Automatico de Rookie Linux/g" "$grubfile" || true
        fi
    done
    
    if [ -f "$EXTRACT_DIR/isolinux.cfg" ]; then
        sed -i 's/\(inst\.stage2=hd:LABEL=\([^ ]*\)\)/\1 inst.ks=hd:LABEL=\2:\/ks.cfg/g' "$EXTRACT_DIR/isolinux.cfg" || true
        sed -i 's/\(inst\.stage2=cdrom[^ ]*\)/\1 inst.ks=cdrom:\/ks.cfg/g' "$EXTRACT_DIR/isolinux.cfg" || true
        
        sed -E -i "s/menu label \^?Install Fedora.*/menu label ^Instalador Automatico de Rookie Linux/g" "$EXTRACT_DIR/isolinux.cfg" || true
    fi
    
    if [ -f "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" ] && command -v mcopy >/dev/null; then
        echo "=> Inyectando GRUB parcheado en la imagen FAT EFI (eltorito_img2_uefi.img)..."
        mcopy -D o -i "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" "$EXTRACT_DIR/efi_grub.cfg" ::/EFI/BOOT/grub.cfg || true
        mcopy -D o -i "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" "$EXTRACT_DIR/efi_grub.cfg" ::/EFI/BOOT/GRUB.CFG || true
    fi
elif [ "$ISO_DISTRO" = "mint" ]; then
    echo "=> Modificando menu de arranque GRUB..."
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        sed -i 's/"Start Linux Mint[^"]*"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        sed -i 's/"Start Linux Mint[^"]*"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/loopback.cfg" || true
    fi
    
    echo "=> Extrayendo y modificando ISOLINUX (Legacy)..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /isolinux/live.cfg "$EXTRACT_DIR/live.cfg" 2>/dev/null || true
    chmod +w "$EXTRACT_DIR/live.cfg" 2>/dev/null || true
    if [ -f "$EXTRACT_DIR/live.cfg" ]; then
        sed -i 's/menu label Start Linux Mint.*/menu label Instalador Automatico de Rookie Linux/g' "$EXTRACT_DIR/live.cfg" || true
    fi
elif [[ "$ISO_DISTRO" == popos* ]] || [[ "$ISO_DISTRO" == pop* ]]; then
    # 6. Modificar GRUB
    echo "=> Modificando menú de arranque GRUB..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/grub.cfg "$EXTRACT_DIR/grub.cfg" 2>/dev/null || true
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/loopback.cfg "$EXTRACT_DIR/loopback.cfg" 2>/dev/null || true
    chmod +w "$EXTRACT_DIR/grub.cfg" "$EXTRACT_DIR/loopback.cfg" 2>/dev/null || true
    
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        sed -i 's/"Pop_OS"/"Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
        sed -i 's/"Install Pop_OS"/"Instalador de Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
        sed -i 's/"Try or Install Pop_OS"/"Instalador de Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
    fi
fi

if [[ "$ISO_DISTRO" == popos* ]] || [[ "$ISO_DISTRO" == pop* ]] || [ "$ISO_DISTRO" = "mint" ]; then
    echo "=> Preparando configuración (Firstboot via squashfs)..."
    
    SQUASH_WORK="/tmp/squashfs_work"
    rm -rf "$SQUASH_WORK"
    mkdir -p "$SQUASH_WORK"
    
    # 1. Extraer squashfs de la ISO
    echo "=> [1/6] Extrayendo filesystem.squashfs de la ISO..."
    CASPER_DIR=$(xorriso -indev "$ISO_PATH" -find / -name "casper*" -type d 2>/dev/null | grep -i casper | head -n 1 | tr -d "'")
    if [ -z "$CASPER_DIR" ]; then
        CASPER_DIR="/casper"
    fi
    echo "   Directorio casper detectado: $CASPER_DIR"
    
    xorriso -osirrox on -indev "$ISO_PATH" -extract "$CASPER_DIR/filesystem.squashfs" "$SQUASH_WORK/filesystem.squashfs" 2>/dev/null
    
    # 2. Desempaquetar squashfs
    echo "=> [2/6] Desempaquetando squashfs (esto puede tardar varios minutos)..."
    stdbuf -o0 unsquashfs -d "$SQUASH_WORK/root" "$SQUASH_WORK/filesystem.squashfs"
    rm -f "$SQUASH_WORK/filesystem.squashfs"
    
    # 3. Inyectar scripts de Rookie Linux
    echo "=> [3/6] Inyectando scripts de Rookie Linux en el sistema..."
    mkdir -p "$SQUASH_WORK/root/opt/rookie-scripts"
    cp -r "$EXTRACT_DIR/custom_scripts/scripts" "$SQUASH_WORK/root/opt/rookie-scripts/"
    cp -r "$EXTRACT_DIR/custom_scripts/assets" "$SQUASH_WORK/root/opt/rookie-scripts/"
    find "$SQUASH_WORK/root/opt/rookie-scripts/scripts/" -type f -name "*.sh" -exec chmod +x {} +
    
    # 4. Inyectar ejecutable de primer arranque
    echo "=> [4/6] Configurando instalador post-arranque..."
    cp "$TEMPLATES_DIR/rookie-firstboot.sh" "$SQUASH_WORK/root/opt/rookie-scripts/"
    chmod +x "$SQUASH_WORK/root/opt/rookie-scripts/rookie-firstboot.sh"
    sed -i 's/\r$//' "$SQUASH_WORK/root/opt/rookie-scripts/rookie-firstboot.sh"
    
    cp "$TEMPLATES_DIR/rookie-terminal-wrapper.sh" "$SQUASH_WORK/root/opt/rookie-scripts/"
    chmod +x "$SQUASH_WORK/root/opt/rookie-scripts/rookie-terminal-wrapper.sh"
    sed -i 's/\r$//' "$SQUASH_WORK/root/opt/rookie-scripts/rookie-terminal-wrapper.sh"
    
    mkdir -p "$SQUASH_WORK/root/etc/xdg/autostart"
    cp "$TEMPLATES_DIR/rookie-firstboot.desktop" "$SQUASH_WORK/root/etc/xdg/autostart/"
    chmod 644 "$SQUASH_WORK/root/etc/xdg/autostart/rookie-firstboot.desktop"
    sed -i 's/\r$//' "$SQUASH_WORK/root/etc/xdg/autostart/rookie-firstboot.desktop"
    
    # 5. Reempaquetar squashfs
    echo "=> [5/6] Reempaquetando squashfs (esto puede tardar varios minutos)..."
    stdbuf -o0 mksquashfs "$SQUASH_WORK/root" "$SQUASH_WORK/filesystem.squashfs" -comp xz -b 1M
    rm -rf "$SQUASH_WORK/root"
fi

OUTPUT_ISO="$BUILD_DIR/custom-$ISO_NAME"
rm -f "$OUTPUT_ISO"
echo "=> Generando nueva ISO inyectada ($OUTPUT_ISO)..."

XORRISO_ARGS=(
    -indev "$ISO_PATH"
    -outdev "$OUTPUT_ISO"
)

XORRISO_ARGS+=( -map "$EXTRACT_DIR/custom_scripts" "/custom_scripts" )

if [ "$ISO_DISTRO" = "ubuntu" ]; then
    XORRISO_ARGS+=( -map "$EXTRACT_DIR/nocloud" "/nocloud" )
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/grub.cfg" "/boot/grub/grub.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/loopback.cfg" "/boot/grub/loopback.cfg" )
    fi
elif [ "$ISO_DISTRO" = "fedora" ]; then
    XORRISO_ARGS+=( -map "$EXTRACT_DIR/ks.cfg" "/ks.cfg" )
    if [ -f "$EXTRACT_DIR/efi_grub.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/efi_grub.cfg" "/EFI/BOOT/grub.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/grub2_grub.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/grub2_grub.cfg" "/boot/grub2/grub.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/isolinux.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/isolinux.cfg" "/isolinux/isolinux.cfg" )
    fi
elif [ "$ISO_DISTRO" = "mint" ] || [[ "$ISO_DISTRO" == popos* ]] || [[ "$ISO_DISTRO" == pop* ]]; then
    SQUASH_WORK="/tmp/squashfs_work"
    CASPER_DIR=$(xorriso -indev "$ISO_PATH" -find / -name "casper*" -type d 2>/dev/null | grep -i casper | head -n 1 | tr -d "'")
    if [ -z "$CASPER_DIR" ]; then
        CASPER_DIR="/casper"
    fi
    XORRISO_ARGS+=( -map "$SQUASH_WORK/filesystem.squashfs" "$CASPER_DIR/filesystem.squashfs" )
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/grub.cfg" "/boot/grub/grub.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/loopback.cfg" "/boot/grub/loopback.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/live.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/live.cfg" "/isolinux/live.cfg" )
    fi
fi

# Clona el sector de arranque exacto de la ISO original
XORRISO_ARGS+=( -boot_image any replay )

if [ "$ISO_DISTRO" = "fedora" ] && [ -f "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" ]; then
    XORRISO_ARGS+=( -append_partition 2 0xef "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" )
    XORRISO_ARGS+=( -boot_image any efi_path=--interval:appended_partition_2:all:: )
fi

xorriso "${XORRISO_ARGS[@]}"

# Hacer la ISO arrancable por USB (isohybrid MBR + UEFI)
# Esto es equivalente a lo que Rufus hace internamente.
# Sin esto, el USB puede no arrancar o arrancar con errores.
echo "=> Aplicando isohybrid (MBR + UEFI) a la ISO..."
if command -v isohybrid &>/dev/null; then
    isohybrid --uefi "$OUTPUT_ISO" 2>/dev/null || \
    isohybrid "$OUTPUT_ISO" 2>/dev/null || \
    echo "[WARNING] isohybrid falló, la ISO podría no arrancar correctamente desde USB."
else
    echo "[WARNING] isohybrid no está instalado. La ISO podría no arrancar correctamente desde USB."
fi

echo "=========================================="
echo "ISO GENERADA EXITOSAMENTE:"
echo "$OUTPUT_ISO"
echo "=========================================="
