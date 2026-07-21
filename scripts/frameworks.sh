#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Frameworks y motores
# ==========================================

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
pkg_install flatpak
if is_debian; then
    pkg_install gnome-software-plugin-flatpak || true
fi

flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
safe_flatpak_install flathub com.unity.UnityHub
echo "  [OK] Unity Hub instalado exitosamente."
