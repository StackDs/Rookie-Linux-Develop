#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Script de actualizacion de sistema
# y dependencias basicas
# ==========================================

# Detectar la distribucion de Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Iniciando actualizacion para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        echo "Verificando conexion a internet en chroot..."
        for i in {1..15}; do ping -c 1 8.8.8.8 >/dev/null 2>&1 && break || sleep 2; done
        if ! curl -s --connect-timeout 5 https://google.com >/dev/null; then
            echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf >/dev/null || true
        fi

        # Fix for Ubuntu installation: remove cdrom from sources list to prevent apt-get update from failing
        sudo sed -i 's/^deb cdrom:/# deb cdrom:/g' /etc/apt/sources.list || true
        sudo sed -i 's/^URIs: cdrom:/# URIs: cdrom:/g' /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || true

        echo "Actualizando repositorios y paquetes (APT)..."
        while sudo fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1 || sudo fuser /var/lib/apt/lists/lock >/dev/null 2>&1; do echo "Esperando lock de apt..."; sleep 3; done
        safe_apt_update || true

        echo "Instalando dependencias basicas..."
        safe_apt_install curl wget git software-properties-common apt-transport-https gnupg2
        echo "  [OK] Dependencias basicas instaladas exitosamente."
        ;;
    
    fedora)
        echo "Actualizando paquetes (DNF)..."
        sudo dnf update -y

        echo "Instalando dependencias basicas..."
        sudo dnf install -y curl wget git || true
        echo "  [OK] Dependencias basicas instaladas exitosamente."
        ;;
    
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

echo "=========================================="
echo "Actualizacion del sistema completada."
echo "=========================================="

