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

# Unity Hub (Via AppImage universal)
echo ">>> Instalando Unity Hub..."
pkg_install fuse libfuse2 || true
sudo mkdir -p /opt/unity
safe_curl "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage" "/opt/unity/UnityHub.AppImage"
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
