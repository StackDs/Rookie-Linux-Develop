#!/bin/bash

set -e

source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"

UBUNTU_VERSION="24.04"
ISO_NAME="ubuntu-24.04.4-desktop-amd64.iso"
ISO_URL="https://releases.ubuntu.com/${UBUNTU_VERSION}/${ISO_NAME}"
DOWNLOAD_DIR="$PROJECT_ROOT/downloads/iso"

echo "=== Descarga de ISO ==="

create_directories
check_command wget

if [ -f "$DOWNLOAD_DIR/$ISO_NAME" ]; then
    info "La ISO $ISO_NAME ya existe en $DOWNLOAD_DIR."
else
    download_file "$ISO_URL" "$DOWNLOAD_DIR/$ISO_NAME"
fi