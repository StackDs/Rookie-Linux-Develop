#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Navegadores Web
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Navegadores para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        # Repositorio de Brave
        sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list > /dev/null
        
        safe_apt_update
        safe_apt_install firefox chromium-browser brave-browser
        echo "  [OK] Firefox, Chromium y Brave instalados exitosamente."
        ;;
    fedora)
        # Repositorio de Brave
        sudo dnf install -y dnf-plugins-core || true
        sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo || true
        sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc || true
        
        sudo dnf install -y firefox chromium brave-browser || true
        echo "  [OK] Firefox, Chromium y Brave instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

