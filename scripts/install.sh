#!/bin/bash
set -e

# ==========================================
# Script Principal de Instalacion
# ==========================================

# Asegurarse de que el script se esta ejecutando desde el directorio correcto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Bienvenido a la instalacion del sistema"
echo "=========================================="

# Dar permisos de ejecucion a los demas scripts
chmod +x "$SCRIPT_DIR/update.sh"
chmod +x "$SCRIPT_DIR/ide.sh"

# Ejecutar script de actualizacion y dependencias
echo "-> Paso 1: Actualizando el sistema..."
"$SCRIPT_DIR/update.sh"

# Ejecutar script de IDEs
echo "-> Paso 2: Instalando IDEs y Editores..."
"$SCRIPT_DIR/ide.sh"

echo "=========================================="
echo "Todo el proceso de instalacion ha finalizado exitosamente!"
echo "=========================================="
