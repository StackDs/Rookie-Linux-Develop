#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

# ==========================================
# Utilidades de terminal
# ==========================================

echo "=========================================="
echo "Instalando Utilidades de terminal para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    packages=(zsh tmux htop btop tree curl wget unzip zip p7zip-full rar unrar jq ripgrep fd-find bat fzf ncdu)
elif is_fedora; then
    packages=(zsh tmux htop btop tree curl wget unzip zip p7zip p7zip-plugins unrar jq ripgrep fd-find bat fzf ncdu)
else
    packages=(zsh tmux htop btop tree curl wget unzip zip jq ripgrep fzf ncdu)
fi

for p in "${packages[@]}"; do
    pkg_install "$p"
done

if is_debian; then
    # Ubuntu instala fd como fdfind y bat como batcat, vamos a crear symlinks para ellos
    sudo ln -sf $(which fdfind) /usr/local/bin/fd || true
    sudo ln -sf $(which batcat) /usr/local/bin/bat || true
fi

echo "  [OK] Utilidades de terminal instaladas exitosamente."
