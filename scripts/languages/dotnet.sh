#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

# ==========================================
# C# y .NET SDK
# ==========================================

echo "=========================================="
echo "Instalando .NET SDK para: $OS"
echo "=========================================="

pkg_update
pkg_install dotnet-sdk-8.0

echo "  [OK] .NET SDK 8.0 instalado exitosamente."
