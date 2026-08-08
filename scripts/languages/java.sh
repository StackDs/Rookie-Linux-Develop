#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

# ==========================================
# Ecosistema Java
# ==========================================

echo "=========================================="
echo "Instalando Ecosistema Java para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    packages=(openjdk-17-jdk openjdk-21-jdk maven)
elif is_fedora; then
    packages=(java-17-openjdk-devel java-21-openjdk-devel maven)
else
    packages=(jdk17-openjdk jdk21-openjdk maven)
fi

for p in "${packages[@]}"; do
    pkg_install "$p"
done

echo "  [OK] Java (OpenJDK 17 y 21) y Maven instalados exitosamente."
