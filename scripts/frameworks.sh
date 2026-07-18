#!/bin/bash
set -e

# ==========================================
# Frameworks y motores
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Frameworks y Motores para: $OS"
echo "=========================================="

# Flutter y Dart SDK (Instalacion manual via Git en /opt)
echo ">>> Instalando Flutter SDK (incluye Dart)..."
if [ ! -d "/opt/flutter" ]; then
    sudo git clone https://github.com/flutter/flutter.git -b stable /opt/flutter
    sudo chmod -R 777 /opt/flutter
    sudo ln -sf /opt/flutter/bin/flutter /usr/local/bin/flutter
    sudo ln -sf /opt/flutter/bin/dart /usr/local/bin/dart
    echo "  [OK] Flutter SDK y Dart SDK instalados exitosamente en /opt/flutter."
else
    echo "  [-] Flutter SDK ya esta instalado."
fi

# Unity Hub (Via Flatpak universal)
echo ">>> Instalando Unity Hub..."
case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y flatpak
        if [ "$OS" = "ubuntu" ]; then
            sudo apt-get install -y gnome-software-plugin-flatpak || true
        fi
        ;;
    fedora)
        sudo dnf install -y flatpak
        ;;
esac
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub com.unity.UnityHub
echo "  [OK] Unity Hub instalado exitosamente."
