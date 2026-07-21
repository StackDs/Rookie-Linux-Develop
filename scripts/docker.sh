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
    pkg_install docker docker-compose
    sudo systemctl enable --now docker || true
else
    # Fallback
    pkg_install docker docker-compose
fi

sudo usermod -aG docker developer || true
echo "  [OK] Docker Engine y Compose instalados exitosamente."
