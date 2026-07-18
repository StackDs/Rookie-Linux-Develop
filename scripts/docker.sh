#!/bin/bash
set -e

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
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io docker-compose
        sudo usermod -aG docker $USER || true
        echo "  [OK] Docker Engine y Compose instalados exitosamente."
        ;;
    fedora)
        sudo dnf install -y docker docker-compose
        sudo systemctl enable --now docker || true
        sudo usermod -aG docker $USER || true
        echo "  [OK] Docker Engine y Compose instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
