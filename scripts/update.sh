#!/bin/bash
set -e

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
        echo "Actualizando repositorios y paquetes (APT)..."
        sudo apt-get update
        sudo apt-get upgrade -y

        echo "Instalando dependencias basicas..."
        sudo apt-get install -y curl wget git software-properties-common apt-transport-https gnupg2
        ;;
    
    fedora)
        echo "Actualizando paquetes (DNF)..."
        sudo dnf update -y

        echo "Instalando dependencias basicas..."
        sudo dnf install -y curl wget git
        ;;
    
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

echo "=========================================="
echo "Actualizacion del sistema completada."
echo "=========================================="
