#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Script de instalacion de compiladores y 
# herramientas C/C++
# ==========================================

echo "=========================================="
echo "Instalando Herramientas C/C++ para: $OS"
echo "=========================================="

echo ">>> Instalando cadena de herramientas C/C++..."
pkg_update

if is_debian; then
    pkg_install gcc g++ gdb make cmake clang ninja-build valgrind
elif is_fedora; then
    pkg_install gcc gcc-c++ gdb make cmake clang ninja-build valgrind
else
    # Nombres estandares
    pkg_install gcc gdb make cmake clang ninja valgrind
fi

echo "  [OK] Cadena de herramientas C/C++ instalada exitosamente."

echo "=========================================="
echo "Instalacion de Herramientas C/C++ completada."
echo "=========================================="
