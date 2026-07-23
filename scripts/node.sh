#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Ecosistema JavaScript / TypeScript
# ==========================================

echo "=========================================="
echo "Instalando JavaScript/TypeScript para: $OS"
echo "=========================================="

if is_debian; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - || true
    pkg_update
    packages=(nodejs)
    # En caso de que NodeSource falle, nodejs de Ubuntu no incluye npm
    if ! command -v npm &> /dev/null; then
        packages+=(npm)
    fi
elif is_fedora; then
    curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
    pkg_update
    packages=(nodejs)
else
    pkg_update
    packages=(nodejs npm)
fi

for p in "${packages[@]}"; do
    pkg_install "$p"
done

# Instalar herramientas globales de JS/TS
sudo npm install -g typescript eslint prettier || true
echo "  [OK] Node.js LTS, npm, TS, ESLint y Prettier instalados exitosamente."
