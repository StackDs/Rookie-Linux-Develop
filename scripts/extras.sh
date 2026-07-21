#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# ==========================================
# Programas adicionales
# ==========================================

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    exit 1
fi

echo "=========================================="
echo "Instalando Programas Adicionales para: $OS"
echo "=========================================="

# LibreOffice
echo ">>> Instalando LibreOffice..."
case "$OS" in
    ubuntu|linuxmint|pop)
        safe_apt_install libreoffice
        ;;
    fedora)
        sudo dnf install -y libreoffice || true
        ;;
esac
echo "  [OK] LibreOffice instalado exitosamente."

# JFLAP
echo ">>> Instalando JFLAP..."
if [ ! -f "/opt/jflap/JFLAP.jar" ]; then
    sudo mkdir -p /opt/jflap
    # Descargar version 7.1 de JFLAP
    sudo wget -qO /opt/jflap/JFLAP.jar https://www.jflap.org/jflaptmp/july27-18/JFLAP7.1.jar || sudo wget -qO /opt/jflap/JFLAP.jar https://www.jflap.org/jflaptmp/july27-18/JFLAP7.1.jar

    
    # Crear un script en bin para ejecutar JFLAP desde cualquier lado
    echo '#!/bin/bash' | sudo tee /usr/local/bin/jflap > /dev/null
    echo 'java -jar /opt/jflap/JFLAP.jar "$@"' | sudo tee -a /usr/local/bin/jflap > /dev/null
    sudo chmod +x /usr/local/bin/jflap
    
    echo "  [OK] JFLAP instalado exitosamente. Puedes ejecutarlo escribiendo 'jflap' en tu terminal."
else
    echo "  [-] JFLAP ya se encuentra instalado."
fi

# Verificador de Instalación (Primer Inicio)
echo ">>> Configurando verificador interactivo..."
sudo cp "$SCRIPT_DIR/verify_installation.sh" /usr/local/bin/verify-rookie
sudo chmod +x /usr/local/bin/verify-rookie

sudo mkdir -p /etc/xdg/autostart
cat << 'EOF' | sudo tee /etc/xdg/autostart/verify-rookie.desktop > /dev/null
[Desktop Entry]
Type=Application
Name=Rookie Verifier
Exec=gnome-terminal -- bash -c "/usr/local/bin/verify-rookie"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
echo "  [OK] Verificador configurado exitosamente."
