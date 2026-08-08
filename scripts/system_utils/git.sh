#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

# ==========================================
# Git y GitHub
# ==========================================

echo "=========================================="
echo "Instalando Git y GitHub CLI para: $OS"
echo "=========================================="

if is_debian; then
    # Añadir repositorio oficial de GitHub CLI
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
    sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    
    pkg_update
    pkg_install git git-lfs gh
elif is_fedora; then
    sudo curl -fsSL https://cli.github.com/packages/rpm/gh-cli.repo -o /etc/yum.repos.d/gh-cli.repo
    pkg_install git git-lfs gh
else
    # Fallback
    pkg_install git git-lfs gh
fi

echo "  [OK] Git, Git LFS y GitHub CLI instalados exitosamente."
