#!/bin/bash
set -e

# ==========================================
# Ecosistema Python
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Ecosistema Python para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
            python3 python3-pip python3-venv pipx \
            black flake8 ipython3 jupyter \
            python3-numpy python3-pandas python3-matplotlib python3-scipy \
            python3-requests python3-flask python3-django python3-fastapi
        echo "  [OK] Python 3, herramientas CLI y librerias instaladas exitosamente."
        ;;
    fedora)
        sudo dnf install -y \
            python3 python3-pip pipx \
            black python3-flake8 python3-ipython jupyterlab \
            python3-numpy python3-pandas python3-matplotlib python3-scipy \
            python3-requests python3-flask python3-django python3-fastapi
        echo "  [OK] Python 3, herramientas CLI y librerias instaladas exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
