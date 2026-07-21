#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Ecosistema Java
# ==========================================

echo "=========================================="
echo "Instalando Ecosistema Java para: $OS"
echo "=========================================="

pkg_update

if is_debian; then
    pkg_install openjdk-17-jdk openjdk-21-jdk maven
elif is_fedora; then
    pkg_install java-17-openjdk-devel java-21-openjdk-devel maven
else
    # Fallback
    pkg_install jdk17-openjdk jdk21-openjdk maven
fi

echo "  [OK] Java (OpenJDK 17 y 21) y Maven instalados exitosamente."
