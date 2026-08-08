#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

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
    packages=(gcc g++ gdb make cmake clang ninja-build valgrind)
elif is_fedora; then
    packages=(gcc gcc-c++ gdb make cmake clang ninja-build valgrind)
else
    packages=(gcc gdb make cmake clang ninja valgrind)
fi

for p in "${packages[@]}"; do
    pkg_install "$p"
done

echo "  [OK] Cadena de herramientas C/C++ instalada exitosamente."

echo "=========================================="
echo "Instalacion de Herramientas C/C++ completada."
echo "=========================================="
