#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Script de instalacion de herramientas
# para administrar bases de datos
# ==========================================

echo "=========================================="
echo "Instalando Herramientas de BD para: $OS"
echo "=========================================="

# Funcion para instalar DBeaver
install_dbeaver() {
    echo ">>> Instalando DBeaver Community Edition..."
    if is_debian; then
        sudo wget -O /usr/share/keyrings/dbeaver.gpg.key https://dbeaver.io/debs/dbeaver.gpg.key
        echo "deb [signed-by=/usr/share/keyrings/dbeaver.gpg.key] https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list > /dev/null
        pkg_update
        pkg_install dbeaver-ce
    elif is_fedora; then
        sudo rpm -i https://dbeaver.io/files/dbeaver-ce-latest-stable.x86_64.rpm || true
        # Si falla (por estar instalado), actualizamos
        sudo dnf upgrade -y dbeaver-ce || true
    else
        echo "[!] Instalacion automatica de DBeaver no soportada en $OS_FAMILY"
    fi
    echo "  [OK] DBeaver instalado exitosamente."
}

# Funcion para instalar pgAdmin4 (Modo Escritorio)
install_pgadmin4() {
    echo ">>> Instalando pgAdmin4 (Escritorio)..."
    if is_debian; then
        CODENAME=${UBUNTU_CODENAME:-$VERSION_CODENAME}
        curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor --yes -o /usr/share/keyrings/packages-pgadmin-org.gpg
        echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$CODENAME pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list > /dev/null
        pkg_update
        pkg_install pgadmin4-desktop
    elif is_fedora; then
        sudo rpm -i https://ftp.postgresql.org/pub/pgadmin/pgadmin4/yum/pgadmin4-fedora-repo-2-1.noarch.rpm || true
        pkg_update
        pkg_install pgadmin4-desktop
    else
        echo "[!] Instalacion automatica de pgAdmin4 no soportada en $OS_FAMILY"
    fi
    echo "  [OK] pgAdmin4 instalado exitosamente."
}

install_dbeaver
install_pgadmin4

echo "=========================================="
echo "Instalacion de Herramientas de BD completada."
echo "=========================================="
