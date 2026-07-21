#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Ecosistema Python
# ==========================================

echo "=========================================="
echo "Instalando Ecosistema Python para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    pkg_install \
        python3 python3-pip python3-venv pipx \
        black flake8 ipython3 jupyter \
        python3-numpy python3-pandas python3-matplotlib python3-scipy \
        python3-requests python3-flask python3-django python3-fastapi
elif is_fedora; then
    pkg_install \
        python3 python3-pip pipx \
        black python3-flake8 python3-ipython jupyterlab \
        python3-numpy python3-pandas python3-matplotlib python3-scipy \
        python3-requests python3-flask python3-django python3-fastapi
else
    # Fallback generico
    pkg_install python3 python3-pip pipx
fi

echo "  [OK] Python 3, herramientas CLI y librerias instaladas exitosamente."
