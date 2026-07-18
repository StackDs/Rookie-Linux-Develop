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
chmod +x "$SCRIPT_DIR/database_tools.sh"
chmod +x "$SCRIPT_DIR/c_cpp.sh"
chmod +x "$SCRIPT_DIR/java.sh"
chmod +x "$SCRIPT_DIR/python.sh"
chmod +x "$SCRIPT_DIR/dotnet.sh"

# Ejecutar script de actualizacion y dependencias
echo "-> Paso 1: Actualizando el sistema..."
"$SCRIPT_DIR/update.sh"

# Ejecutar script de IDEs
echo "-> Paso 2: Instalando IDEs y Editores..."
"$SCRIPT_DIR/ide.sh"

# Ejecutar script de herramientas de Base de Datos
echo "-> Paso 3: Instalando herramientas de Base de Datos..."
"$SCRIPT_DIR/database_tools.sh"

# Ejecutar script de herramientas C/C++
echo "-> Paso 4: Instalando compiladores y herramientas C/C++..."
"$SCRIPT_DIR/c_cpp.sh"

# Ejecutar script de ecosistema Java
echo "-> Paso 5: Instalando ecosistema Java..."
"$SCRIPT_DIR/java.sh"

# Ejecutar script de ecosistema Python
echo "-> Paso 6: Instalando ecosistema Python..."
"$SCRIPT_DIR/python.sh"

# Ejecutar script de .NET SDK
echo "-> Paso 7: Instalando .NET SDK..."
"$SCRIPT_DIR/dotnet.sh"

echo "=========================================="
echo "Todo el proceso de instalacion ha finalizado exitosamente!"
echo "=========================================="
