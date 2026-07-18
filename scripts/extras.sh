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

# JFLAP
echo ">>> Instalando JFLAP..."
if [ ! -f "/opt/jflap/JFLAP.jar" ]; then
    sudo mkdir -p /opt/jflap
    # Descargar version 7.1 de JFLAP
    sudo wget -qO /opt/jflap/JFLAP.jar https://www.jflap.org/jflaptmp/july10-18/JFLAP7.1.jar || sudo wget -qO /opt/jflap/JFLAP.jar https://www.jflap.org/jflaptmp/july10-18/JFLAP7.1.jar
    
    # Crear un script en bin para ejecutar JFLAP desde cualquier lado
    echo '#!/bin/bash' | sudo tee /usr/local/bin/jflap > /dev/null
    echo 'java -jar /opt/jflap/JFLAP.jar "$@"' | sudo tee -a /usr/local/bin/jflap > /dev/null
    sudo chmod +x /usr/local/bin/jflap
    
    echo "  [OK] JFLAP instalado exitosamente. Puedes ejecutarlo escribiendo 'jflap' en tu terminal."
else
    echo "  [-] JFLAP ya se encuentra instalado."
fi

