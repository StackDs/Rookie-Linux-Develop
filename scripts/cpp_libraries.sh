#!/bin/bash
set -e

# ==========================================
# Bibliotecas C/C++
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Bibliotecas C/C++ para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
            libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-net-dev \
            libsfml-dev libgl1-mesa-dev libglu1-mesa-dev libglfw3-dev libglew-dev
        echo "  [OK] Bibliotecas C/C++ (SDL2, SFML, OpenGL, GLFW, GLEW) instaladas exitosamente."
        ;;
    fedora)
        sudo dnf install -y \
            SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel SDL2_net-devel \
            SFML-devel mesa-libGL-devel mesa-libGLU-devel glfw-devel glew-devel
        echo "  [OK] Bibliotecas C/C++ (SDL2, SFML, OpenGL, GLFW, GLEW) instaladas exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
