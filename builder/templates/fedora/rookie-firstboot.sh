#!/bin/bash
# ==========================================
# Rookie Linux - Primer Arranque (Fedora)
# ==========================================
# Este script se ejecuta al iniciar sesión en el
# escritorio por primera vez (vía autostart).

# Si estamos en el Live USB, no ejecutar.
if [ "$USER" = "liveuser" ]; then
    exit 0
fi

# Si ya se ejecutó antes, no volver a correr.
if [ -f "$HOME/.rookie_installed" ]; then
    exit 0
fi

LOG="$HOME/rookie-install.log"

echo "=========================================="
echo " Bienvenido a Rookie Linux (Post-Install) "
echo "=========================================="
echo "Vamos a instalar todas tus herramientas de"
echo "desarrollo y configurar tu entorno..."
echo "=========================================="
echo ""

# Comprobación de internet
echo "Comprobando conexión a internet..."
while ! ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1 && ! curl -s --connect-timeout 3 https://google.com > /dev/null 2>&1; do
    echo "=========================================="
    echo "⚠️ NO SE DETECTÓ CONEXIÓN A INTERNET ⚠️"
    echo "Por favor, conéctate a una red Wi-Fi o"
    echo "cableada usando el menú superior derecho."
    echo "Reintentando en 5 segundos..."
    echo "=========================================="
    sleep 5
done
echo "¡Conexión a internet establecida!"
echo ""

echo "Se requieren permisos de administrador."
echo "Por favor, ingresa tu contraseña si se solicita:"
sudo -v

# Ejecutar la batería de scripts de instalación
if [ -d /opt/rookie-scripts/scripts ] && [ -f /opt/rookie-scripts/scripts/install.sh ]; then
    echo "Iniciando instalación..." | tee -a "$LOG"
    sudo chmod +x /opt/rookie-scripts/scripts/*.sh 2>/dev/null || true
    
    # Ejecutar el script (con sudo, pero manteniendo SUDO_USER para appearance.sh)
    sudo bash /opt/rookie-scripts/scripts/install.sh 2>&1 | tee -a "$LOG"
    
    echo "Fase 1 completada. Abriendo terminal para la Fase 2 (Verificación)..." | tee -a "$LOG"
    
    # Desactivar este script para que no vuelva a ejecutarse
    echo "Desactivando autostart de Rookie Linux..." | tee -a "$LOG"
    sudo rm -f /etc/xdg/autostart/rookie-firstboot.desktop
    
    # Lanzar la fase 2 en una nueva terminal
    sudo chmod +x /opt/rookie-scripts/scripts/rookie-verify.sh
    bash /opt/rookie-scripts/rookie-terminal-wrapper.sh "/opt/rookie-scripts/scripts/rookie-verify.sh" &
    exit 0
else
    echo "[ERROR] No se encontraron los scripts en /opt/rookie-scripts/scripts/" | tee -a "$LOG"
    sudo rm -f /etc/xdg/autostart/rookie-firstboot.desktop
    read -p "Presiona Enter para cerrar esta ventana..."
fi
