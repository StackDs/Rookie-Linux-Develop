#!/bin/bash
set -e

echo "=========================================="
echo "Iniciando Constructor de ISO (Docker)"
echo "=========================================="

WORKSPACE="/workspace"
ISO_DISTRO="${ISO_DISTRO:-ubuntu}"
DOWNLOAD_DIR="$WORKSPACE/downloads/iso/$ISO_DISTRO"
BUILD_DIR="$WORKSPACE/output/$ISO_DISTRO"
EXTRACT_DIR="/tmp/iso_unpacked"
TEMPLATES_DIR="$WORKSPACE/builder/templates/$ISO_DISTRO"

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
        sed -i 's/---/autoinstall ds=nocloud\\;s=\/cdrom\/nocloud\/ nomodeset ---/g' "$EXTRACT_DIR/grub.cfg" || true
        sed -i 's/"Try or Install Ubuntu"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        sed -i 's/---/autoinstall ds=nocloud\\;s=\/cdrom\/nocloud\/ nomodeset ---/g' "$EXTRACT_DIR/loopback.cfg" || true
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
    echo "=> Preparando configuracion Preseed (Ubiquity)..."
    cp "$TEMPLATES_DIR/preseed.cfg" "$EXTRACT_DIR/preseed.cfg"
    sed -i 's/\r$//' "$EXTRACT_DIR/preseed.cfg"

    echo "=> Extrayendo configuracion GRUB original de la ISO..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/grub.cfg "$EXTRACT_DIR/grub.cfg" 2>/dev/null || true
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/loopback.cfg "$EXTRACT_DIR/loopback.cfg" 2>/dev/null || true
    
    chmod +w "$EXTRACT_DIR/grub.cfg" "$EXTRACT_DIR/loopback.cfg" 2>/dev/null || true

    echo "=> Modificando menu de arranque GRUB (autoinstall)..."
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        sed -i 's/--/file=\/cdrom\/preseed.cfg --/g' "$EXTRACT_DIR/grub.cfg" || true
        sed -i 's/"Start Linux Mint"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/grub.cfg" || true
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        sed -i 's/--/file=\/cdrom\/preseed.cfg --/g' "$EXTRACT_DIR/loopback.cfg" || true
        sed -i 's/"Start Linux Mint"/"Instalador Automatico de Rookie Linux"/g' "$EXTRACT_DIR/loopback.cfg" || true
    fi
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
elif [ "$ISO_DISTRO" = "mint" ]; then
    XORRISO_ARGS+=( -map "$EXTRACT_DIR/preseed.cfg" "/preseed.cfg" )
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/grub.cfg" "/boot/grub/grub.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/loopback.cfg" "/boot/grub/loopback.cfg" )
    fi
fi

# Clona el sector de arranque exacto de la ISO original
XORRISO_ARGS+=( -boot_image any replay )

if [ "$ISO_DISTRO" = "fedora" ] && [ -f "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" ]; then
    XORRISO_ARGS+=( -append_partition 2 0xef "$EXTRACT_DIR/boot_images/eltorito_img2_uefi.img" )
    XORRISO_ARGS+=( -boot_image any efi_path=--interval:appended_partition_2:all:: )
fi

xorriso "${XORRISO_ARGS[@]}"

echo "=========================================="
echo "ISO GENERADA EXITOSAMENTE:"
echo "$OUTPUT_ISO"
echo "=========================================="
