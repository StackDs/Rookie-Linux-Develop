#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Motores de bases de datos locales
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Motores de BD para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        safe_apt_update
        safe_apt_install postgresql postgresql-contrib sqlite3
        echo "  [OK] PostgreSQL y SQLite instalados exitosamente."
        ;;
    fedora)
        sudo dnf install -y postgresql-server postgresql-contrib sqlite || true
        # Fedora requiere inicializar el cluster de BD manualmente
        sudo postgresql-setup --initdb || true
        sudo systemctl enable --now postgresql || true
        echo "  [OK] PostgreSQL y SQLite instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac

