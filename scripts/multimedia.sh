#!/bin/bash
set -e

# ==========================================
# Multimedia
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Multimedia para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y vlc obs-studio
        echo "  [OK] VLC y OBS Studio instalados exitosamente."
        ;;
    fedora)
        # Pueden requerir RPM Fusion (non-free), si no lo encuentra, continua
        sudo dnf install -y vlc obs-studio || true
        echo "  [OK] VLC y OBS Studio instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
