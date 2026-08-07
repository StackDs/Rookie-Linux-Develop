#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Motores de bases de datos locales
# ==========================================

echo "=========================================="
echo "Instalando Motores de BD para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    packages=(postgresql postgresql-contrib sqlite3)
elif is_fedora; then
    packages=(postgresql-server postgresql-contrib sqlite)
else
    packages=(postgresql sqlite)
fi

for p in "${packages[@]}"; do
    pkg_install "$p"
done

if is_fedora; then
    # Fedora requiere inicializar el cluster de BD manualmente
    sudo postgresql-setup --initdb || true
    sudo systemctl enable postgresql || true
fi

echo "  [OK] PostgreSQL y SQLite instalados exitosamente."
