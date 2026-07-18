#!/bin/bash
set -e

# ==========================================
# Editores de texto CLI
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Editores de texto para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nano vim neovim
        echo "  [OK] nano, vim y neovim instalados exitosamente."
        ;;
    fedora)
        sudo dnf install -y nano vim neovim
        echo "  [OK] nano, vim y neovim instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
