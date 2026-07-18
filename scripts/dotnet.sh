#!/bin/bash
set -e

# ==========================================
# C# y .NET SDK
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando .NET SDK para: $OS"
echo "=========================================="

case "$OS" in
    ubuntu|linuxmint|pop)
        sudo DEBIAN_FRONTEND=noninteractive apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y dotnet-sdk-8.0
        echo "  [OK] .NET SDK 8.0 instalado exitosamente."
        ;;
    fedora)
        sudo dnf install -y dotnet-sdk-8.0
        echo "  [OK] .NET SDK 8.0 instalado exitosamente."
        ;;
    *)
        echo "Distribucion no soportada en este script: $OS"
        exit 1
        ;;
esac
