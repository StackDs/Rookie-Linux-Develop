#!/bin/bash
# ==========================================
# Rookie Linux - Fase 2: Verificación
# ==========================================

LOG="$HOME/rookie-install.log"

echo "=========================================="
echo " Bienvenido a Rookie Linux (Fase 2) "
echo "=========================================="
echo "Verificando instalación y configurando la"
echo "apariencia de tu nuevo entorno..."
echo "=========================================="
echo ""

if [ -f /opt/rookie-scripts/scripts/verify_installation.sh ]; then
    echo "-> Ejecutando scripts de verificación..." | tee -a "$LOG"
    sudo bash /opt/rookie-scripts/scripts/verify_installation.sh 2>&1 | tee -a "$LOG"
else
    echo "[ERROR] No se encontró verify_installation.sh" | tee -a "$LOG"
fi

echo ""
echo "=========================================="
echo " Configurando Apariencia "
echo "=========================================="
if [ -f /opt/rookie-scripts/scripts/appearance.sh ]; then
    sudo bash /opt/rookie-scripts/scripts/appearance.sh 2>&1 | tee -a "$LOG"
else
    echo "[ERROR] No se encontró appearance.sh" | tee -a "$LOG"
fi

echo ""
echo "=========================================="
echo "¡Todo el proceso ha finalizado con éxito!"
echo "Revisa $LOG si hubo algún error."
echo "Disfruta de Rookie Linux."
echo "=========================================="
read -p "Presiona Enter para cerrar esta ventana..."
