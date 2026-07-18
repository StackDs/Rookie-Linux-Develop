#!/bin/bash
set -e

# ==========================================
# Script de instalacion de herramientas
# para administrar bases de datos
# ==========================================

# Detectar la distribucion de Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    # Mint usa su propio CODENAME, pero proporciona UBUNTU_CODENAME para repositorios
    CODENAME=${UBUNTU_CODENAME:-$VERSION_CODENAME}
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Herramientas de BD para: $OS"
echo "=========================================="

# Funcion para instalar DBeaver
install_dbeaver() {
    echo ">>> Instalando DBeaver Community Edition..."
    case "$OS" in
        ubuntu|linuxmint|pop)
            sudo wget -O /usr/share/keyrings/dbeaver.gpg.key https://dbeaver.io/debs/dbeaver.gpg.key
            echo "deb [signed-by=/usr/share/keyrings/dbeaver.gpg.key] https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list > /dev/null
            sudo apt-get update
            sudo apt-get install -y dbeaver-ce
            echo "  [OK] DBeaver instalado exitosamente."
            ;;
        fedora)
            sudo wget -O /etc/yum.repos.d/dbeaver.repo https://dbeaver.io/debs/dbeaver.repo
            sudo dnf install -y dbeaver-ce
            echo "  [OK] DBeaver instalado exitosamente."
            ;;
    esac
}

# Funcion para instalar pgAdmin4 (Modo Escritorio)
install_pgadmin4() {
    echo ">>> Instalando pgAdmin4 (Escritorio)..."
    case "$OS" in
        ubuntu|linuxmint|pop)
            curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor --yes -o /usr/share/keyrings/packages-pgadmin-org.gpg
            echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$CODENAME pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list > /dev/null
            sudo apt-get update
            sudo apt-get install -y pgadmin4-desktop
            echo "  [OK] pgAdmin4 instalado exitosamente."
            ;;
        fedora)
            sudo rpm -i https://ftp.postgresql.org/pub/pgadmin/pgadmin4/yum/pgadmin4-fedora-repo-2-1.noarch.rpm || true
            sudo dnf install -y pgadmin4-desktop
            echo "  [OK] pgAdmin4 instalado exitosamente."
            ;;
    esac
}

install_dbeaver
install_pgadmin4

echo "=========================================="
echo "Instalacion de Herramientas de BD completada."
echo "=========================================="
