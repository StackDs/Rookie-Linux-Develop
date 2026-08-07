#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Script de instalacion de IDEs y Editores
# ==========================================

echo "=========================================="
echo "Instalando IDEs para: $OS"
echo "=========================================="

# Funcion para instalar Visual Studio Code
install_vscode() {
    echo ">>> Instalando Visual Studio Code..."
    if is_debian; then
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
        sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
        sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
        rm -f packages.microsoft.gpg
        pkg_update
        pkg_install code
    elif is_fedora || is_suse; then
        sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
        sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
        pkg_update
        pkg_install code
    elif is_arch; then
        pkg_install code
    fi
    echo "  [OK] Visual Studio Code instalado exitosamente."
}

# Funcion para instalar IntelliJ IDEA Community
install_intellij() {
    echo ">>> Instalando IntelliJ IDEA Community..."
    sudo mkdir -p /opt/idea
    safe_curl "https://download.jetbrains.com/product?code=IIC&latest=true&distribution=linux" "/tmp/idea.tar.gz"
    sudo tar -xzf /tmp/idea.tar.gz -C /opt/idea --strip-components=1
    rm -f /tmp/idea.tar.gz
    
    # Crear enlace simbolico
    sudo ln -sf /opt/idea/bin/idea.sh /usr/local/bin/idea
    
    # Crear acceso directo de escritorio
    sudo tee /usr/share/applications/intellij-idea-community.desktop > /dev/null <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=IntelliJ IDEA Community Edition
Icon=/opt/idea/bin/idea.svg
Exec="/opt/idea/bin/idea.sh" %f
Comment=Capable and Ergonomic IDE for JVM
Categories=Development;IDE;
Terminal=false
StartupWMClass=jetbrains-idea-ce
EOF

    echo "  [OK] IntelliJ IDEA Community instalado exitosamente (.tar.gz)."
}

# Funcion para instalar Emacs
install_emacs() {
    echo ">>> Instalando Emacs..."
    pkg_install emacs
    echo "  [OK] Emacs instalado exitosamente."
}

# Funcion para instalar Antigravity
install_antigravity() {
    echo ">>> Instalando Antigravity..."
    if is_debian; then
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/antigravity-repo-key.gpg
        echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | sudo tee /etc/apt/sources.list.d/antigravity.list > /dev/null
        pkg_update
        pkg_install antigravity
        echo "  [OK] Antigravity instalado exitosamente."
    else
        echo "[!] Antigravity actualmente usa un repositorio APT. No soportado nativamente en $OS."
    fi
}

# Ejecutar las funciones
install_vscode
install_intellij
install_emacs
install_antigravity

echo "=========================================="
echo "Instalacion de IDEs completada."
echo "=========================================="
