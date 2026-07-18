#!/bin/bash
set -e

# ==========================================
# Script de instalacion de IDEs y Editores
# ==========================================

# Detectar la distribucion de Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando IDEs para: $OS"
echo "=========================================="

# Funcion para instalar Visual Studio Code
install_vscode() {
    echo ">>> Instalando Visual Studio Code..."
    case "$OS" in
        ubuntu|linuxmint|pop)
            wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
            sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
            sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
            rm -f packages.microsoft.gpg
            sudo apt-get update
            sudo apt-get install -y code
            echo "  [OK] Visual Studio Code instalado exitosamente."
            ;;
        fedora)
            sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
            sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
            sudo dnf check-update || true
            sudo dnf install -y code
            echo "  [OK] Visual Studio Code instalado exitosamente."
            ;;
    esac
}

# Funcion para instalar IntelliJ IDEA Community
install_intellij() {
    echo ">>> Instalando IntelliJ IDEA Community..."
    # Usaremos Flatpak para una instalacion universal y limpia en todas estas distros.
    case "$OS" in
        ubuntu|linuxmint|pop)
            # Asegurarse de que flatpak este instalado
            sudo apt-get install -y flatpak
            # En Ubuntu puede ser necesario el plugin de software
            if [ "$OS" = "ubuntu" ]; then
                sudo apt-get install -y gnome-software-plugin-flatpak || true
            fi
            ;;
        fedora)
            # Flatpak suele venir preinstalado en Fedora, pero por si acaso
            sudo dnf install -y flatpak
            ;;
    esac

    # Anadir repositorio de Flathub
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    
    # Instalar IntelliJ
    flatpak install -y flathub com.jetbrains.IntelliJ-IDEA-Community
    echo "  [OK] IntelliJ IDEA Community instalado exitosamente."
}

# Funcion para instalar Emacs
install_emacs() {
    echo ">>> Instalando Emacs..."
    case "$OS" in
        ubuntu|linuxmint|pop)
            sudo DEBIAN_FRONTEND=noninteractive apt-get install -y emacs
            echo "  [OK] Emacs instalado exitosamente."
            ;;
        fedora)
            sudo dnf install -y emacs
            echo "  [OK] Emacs instalado exitosamente."
            ;;
    esac
}

# Funcion para instalar Antigravity
install_antigravity() {
    echo ">>> Instalando Antigravity..."
    case "$OS" in
        ubuntu|linuxmint|pop)
            sudo mkdir -p /etc/apt/keyrings
            curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/antigravity-repo-key.gpg
            echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | sudo tee /etc/apt/sources.list.d/antigravity.list > /dev/null
            sudo apt-get update
            sudo apt-get install -y antigravity
            echo "  [OK] Antigravity instalado exitosamente."
            ;;
        fedora)
            echo "[!] Antigravity actualmente usa un repositorio APT. No disponible en Fedora."
            ;;
    esac
}

# Ejecutar las funciones
install_vscode
install_intellij
install_emacs
install_antigravity

echo "=========================================="
echo "Instalacion de IDEs completada."
echo "=========================================="
