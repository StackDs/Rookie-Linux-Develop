#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

# ==========================================
# Navegadores Web
# ==========================================

echo "=========================================="
echo "Instalando Navegadores para: $OS"
echo "=========================================="

if is_debian; then
    # Repositorio de Brave
    sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list > /dev/null
    
    pkg_update
    pkg_install firefox brave-browser
elif is_fedora; then
    # Repositorio de Brave
    sudo curl -fsSL https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo -o /etc/yum.repos.d/brave-browser.repo
    sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc || true
    
    pkg_update
    pkg_install firefox brave-browser
else
    # Fallback
    pkg_update
    pkg_install firefox brave-browser || true
fi

echo "  [OK] Firefox y Brave instalados exitosamente."
