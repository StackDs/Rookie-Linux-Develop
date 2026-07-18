#!/bin/bash
set -e

# ==========================================
# Script de instalacion de compiladores y 
# herramientas C/C++
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
echo "Instalando Herramientas C/C++ para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        echo ">>> Instalando cadena de herramientas C/C++ (APT)..."
        # clang incluye clang++
        sudo apt-get update
        sudo apt-get install -y gcc g++ gdb make cmake clang ninja-build valgrind
        echo "  [OK] Cadena de herramientas C/C++ instalada exitosamente."
        ;;
    fedora)
        echo ">>> Instalando cadena de herramientas C/C++ (DNF)..."
        # gcc-c++ provee g++, clang provee clang++
        sudo dnf install -y gcc gcc-c++ gdb make cmake clang ninja-build valgrind
        echo "  [OK] Cadena de herramientas C/C++ instalada exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

echo "=========================================="
echo "Instalacion de Herramientas C/C++ completada."
echo "=========================================="
