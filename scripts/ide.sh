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
    # Usaremos Flatpak para una instalacion universal y limpia en todas estas distros.
    pkg_install flatpak
    if is_debian; then
        pkg_install gnome-software-plugin-flatpak || true
    fi

    # Anadir repositorio de Flathub
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    
    # Instalar IntelliJ
    safe_flatpak_install flathub com.jetbrains.IntelliJ-IDEA-Community
    echo "  [OK] IntelliJ IDEA Community instalado exitosamente."
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
