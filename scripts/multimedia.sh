#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Multimedia
# ==========================================

echo "=========================================="
echo "Instalando Multimedia para: $OS"
echo "=========================================="

pkg_update
pkg_install vlc obs-studio

echo "  [OK] VLC y OBS Studio instalados exitosamente."
