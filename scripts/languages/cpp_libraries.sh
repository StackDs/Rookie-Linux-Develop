#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

# ==========================================
# Bibliotecas C/C++
# ==========================================

echo "=========================================="
echo "Instalando Bibliotecas C/C++ para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    packages=(libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-net-dev libsfml-dev libgl1-mesa-dev libglu1-mesa-dev libglfw3-dev libglew-dev mesa-utils)
elif is_fedora; then
    packages=(SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel SDL2_net-devel SFML-devel mesa-libGL-devel mesa-libGLU-devel glfw-devel glew-devel glx-utils)
else
    packages=(sdl2 sfml glfw-x11 glew mesa-demos)
fi

for p in "${packages[@]}"; do
    pkg_install "$p"
done

echo "  [OK] Bibliotecas C/C++ (SDL2, SFML, OpenGL, GLFW, GLEW) y utils instaladas exitosamente."
