#!/bin/bash
set -e

# ==========================================
# Ecosistema Java
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Ecosistema Java para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y openjdk-17-jdk openjdk-21-jdk maven
        echo "  [OK] Java (OpenJDK 17 y 21) y Maven instalados exitosamente."
        ;;
    fedora)
        sudo dnf install -y java-17-openjdk-devel java-21-openjdk-devel maven
        echo "  [OK] Java (OpenJDK 17 y 21) y Maven instalados exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
