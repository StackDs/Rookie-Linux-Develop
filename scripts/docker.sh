#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Contenedores (Docker)
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Docker para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        safe_apt_update
        safe_apt_install docker.io docker-compose
        sudo usermod -aG docker developer || true
        echo "  [OK] Docker Engine y Compose instalados exitosamente."
        ;;
    fedora)
        sudo dnf install -y docker docker-compose || true
        sudo systemctl enable --now docker || true
        sudo usermod -aG docker developer || true
        echo "  [OK] Docker Engine y Compose instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

