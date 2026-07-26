#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Contenedores (Docker)
# ==========================================

echo "=========================================="
echo "Instalando Docker para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    pkg_install docker.io docker-compose
elif is_fedora; then
    sudo curl -fsSL https://download.docker.com/linux/fedora/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
    pkg_install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl enable docker || true
else
    # Fallback
    pkg_install docker docker-compose
fi

sudo usermod -aG docker develop || true
echo "  [OK] Docker Engine y Compose instalados exitosamente."
