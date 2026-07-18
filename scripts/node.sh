#!/bin/bash
set -e

# ==========================================
# Ecosistema JavaScript / TypeScript
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando JavaScript/TypeScript para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
        ;;
    fedora)
        curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
        sudo dnf install -y nodejs
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

# Instalar herramientas globales de JS/TS
sudo npm install -g typescript eslint prettier
echo "  [OK] Node.js LTS, npm, TS, ESLint y Prettier instalados exitosamente."
