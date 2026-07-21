#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Editores de texto CLI
# ==========================================

echo "=========================================="
echo "Instalando Editores de texto para: $OS"
echo "=========================================="

pkg_update
pkg_install nano vim neovim

echo "  [OK] nano, vim y neovim instalados exitosamente."
