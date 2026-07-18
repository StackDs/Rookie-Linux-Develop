#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Utilidades de terminal
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Utilidades de terminal para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        safe_apt_update
        # fd = fd-find, 7zip = p7zip-full
        safe_apt_install \
            zsh tmux htop btop tree curl wget unzip zip p7zip-full \
            rar unrar jq ripgrep fd-find bat fzf ncdu
        echo "  [OK] Utilidades de terminal instaladas exitosamente."
        ;;
    fedora)
        # unrar puede requerir rpm-fusion, se permite fallo silencioso con || true
        sudo dnf install -y \ || true
            zsh tmux htop btop tree curl wget unzip zip p7zip p7zip-plugins \
            unrar jq ripgrep fd-find bat fzf ncdu || true
        echo "  [OK] Utilidades de terminal instaladas exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

