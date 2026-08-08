#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

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

# Unity Hub
echo ">>> Instalando Unity Hub..."
if is_debian; then
    wget -qO - https://hub.unity3d.com/linux/keys/public | gpg --dearmor | sudo tee /usr/share/keyrings/Unity_Technologies_ApS.gpg > /dev/null
    sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/Unity_Technologies_ApS.gpg] https://hub.unity3d.com/linux/repos/deb stable main" > /etc/apt/sources.list.d/unityhub.list'
    sudo apt-get update > /dev/null 2>&1
    pkg_install unityhub
    echo "  [OK] Unity Hub instalado exitosamente (APT)."
else
    # Fallback para no-Debian usando AppImage
    if is_fedora; then
        pkg_install fuse fuse-libs || true
    fi
    sudo mkdir -p /opt/unity
    safe_curl "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage" "/opt/unity/UnityHub.AppImage" || true
    if [ -f /opt/unity/UnityHub.AppImage ]; then
        sudo chmod +x /opt/unity/UnityHub.AppImage
        sudo ln -sf /opt/unity/UnityHub.AppImage /usr/local/bin/unityhub
        
        # Crear acceso directo de escritorio
        sudo tee /usr/share/applications/unityhub.desktop > /dev/null <<EOF
[Desktop Entry]
Name=Unity Hub
Exec=/opt/unity/UnityHub.AppImage %U
Terminal=false
Type=Application
Icon=unityhub
Categories=Development;
StartupNotify=true
EOF
        echo "  [OK] Unity Hub instalado exitosamente (.AppImage)."
    else
        echo "  [-] Error al descargar Unity Hub."
    fi
fi
