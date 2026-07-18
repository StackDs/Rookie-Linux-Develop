#!/bin/bash
set -e

# ==========================================
# Git y GitHub
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Git y GitHub CLI para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        # Añadir repositorio oficial de GitHub CLI
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
        sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git git-lfs gh
        echo "  [OK] Git, Git LFS y GitHub CLI instalados exitosamente."
        ;;
    fedora)
        # Fedora ya incluye gh en sus repositorios por defecto
        sudo dnf install -y git git-lfs gh
        echo "  [OK] Git, Git LFS y GitHub CLI instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
