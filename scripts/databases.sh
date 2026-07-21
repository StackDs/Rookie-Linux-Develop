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
    pkg_install postgresql postgresql-contrib sqlite3
elif is_fedora; then
    pkg_install postgresql-server postgresql-contrib sqlite
    # Fedora requiere inicializar el cluster de BD manualmente
    sudo postgresql-setup --initdb || true
    sudo systemctl enable --now postgresql || true
else
    # Fallback
    pkg_install postgresql sqlite
fi

echo "  [OK] PostgreSQL y SQLite instalados exitosamente."
