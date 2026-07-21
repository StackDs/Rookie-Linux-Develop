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

if [ "$ISO_DISTRO" = "ubuntu" ]; then
    echo "=> Preparando configuracion Cloud-Init (Subiquity)..."
    cp "$TEMPLATES_DIR/user-data" "$EXTRACT_DIR/nocloud/"
    cp "$TEMPLATES_DIR/meta-data" "$EXTRACT_DIR/nocloud/"
    
    echo "=> Preparando scripts y recursos (Rookie-Linux-Develop)..."
    cp -r "$WORKSPACE/scripts" "$EXTRACT_DIR/custom_scripts/"
    cp -r "$WORKSPACE/assets" "$EXTRACT_DIR/custom_scripts/"

    echo "=> Convirtiendo finales de linea Windows (CRLF) a Linux (LF)..."
    find "$EXTRACT_DIR/custom_scripts/scripts/" -type f -name "*.sh" -exec sed -i 's/\r$//' {} + 2>/dev/null || true
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
fi

# 3. Reempaquetar inyectando los archivos directamente en la ISO clonada
OUTPUT_ISO="$BUILD_DIR/custom-$ISO_NAME"
echo "=> Generando nueva ISO inyectada ($OUTPUT_ISO)..."

XORRISO_ARGS=(
    -indev "$ISO_PATH"
    -outdev "$OUTPUT_ISO"
)

if [ "$ISO_DISTRO" = "ubuntu" ]; then
    XORRISO_ARGS+=(
        -map "$EXTRACT_DIR/nocloud" "/nocloud"
        -map "$EXTRACT_DIR/custom_scripts" "/custom_scripts"
    )
    if [ -f "$EXTRACT_DIR/grub.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/grub.cfg" "/boot/grub/grub.cfg" )
    fi
    if [ -f "$EXTRACT_DIR/loopback.cfg" ]; then
        XORRISO_ARGS+=( -map "$EXTRACT_DIR/loopback.cfg" "/boot/grub/loopback.cfg" )
    fi
fi

# Clona el sector de arranque exacto de la ISO original
XORRISO_ARGS+=( -boot_image any replay )

xorriso "${XORRISO_ARGS[@]}"

echo "=========================================="
echo "ISO GENERADA EXITOSAMENTE:"
echo "$OUTPUT_ISO"
echo "=========================================="
