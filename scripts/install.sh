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
chmod +x "$SCRIPT_DIR/node.sh"
chmod +x "$SCRIPT_DIR/databases.sh"
chmod +x "$SCRIPT_DIR/docker.sh"
chmod +x "$SCRIPT_DIR/git.sh"
chmod +x "$SCRIPT_DIR/terminal.sh"
chmod +x "$SCRIPT_DIR/editors.sh"
chmod +x "$SCRIPT_DIR/browsers.sh"
chmod +x "$SCRIPT_DIR/multimedia.sh"
chmod +x "$SCRIPT_DIR/cpp_libraries.sh"
chmod +x "$SCRIPT_DIR/frameworks.sh"
chmod +x "$SCRIPT_DIR/extras.sh"
chmod +x "$SCRIPT_DIR/appearance.sh"
chmod +x "$SCRIPT_DIR/easter_eggs.sh"

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

# Ejecutar script de Node.js / TS
echo "-> Paso 8: Instalando ecosistema JavaScript/TypeScript..."
"$SCRIPT_DIR/node.sh"

# Ejecutar script de Motores de BD
echo "-> Paso 9: Instalando motores de Bases de Datos..."
"$SCRIPT_DIR/databases.sh"

# Ejecutar script de Docker
echo "-> Paso 10: Instalando Docker y utilidades..."
"$SCRIPT_DIR/docker.sh"

# Ejecutar script de Git y GitHub
echo "-> Paso 11: Instalando Git, Git LFS y GitHub CLI..."
"$SCRIPT_DIR/git.sh"

# Ejecutar script de Utilidades de Terminal
echo "-> Paso 12: Instalando utilidades de terminal..."
"$SCRIPT_DIR/terminal.sh"

# Ejecutar script de Editores CLI
echo "-> Paso 13: Instalando editores de texto CLI..."
"$SCRIPT_DIR/editors.sh"

# Ejecutar script de Navegadores
echo "-> Paso 14: Instalando navegadores web..."
"$SCRIPT_DIR/browsers.sh"

# Ejecutar script de Multimedia
echo "-> Paso 15: Instalando multimedia (VLC, OBS)..."
"$SCRIPT_DIR/multimedia.sh"

# Ejecutar script de Bibliotecas C/C++
echo "-> Paso 16: Instalando bibliotecas C/C++ (SDL2, OpenGL, SFML)..."
"$SCRIPT_DIR/cpp_libraries.sh"

# Ejecutar script de Frameworks y Motores
echo "-> Paso 17: Instalando frameworks (Flutter, Dart, Unity)..."
"$SCRIPT_DIR/frameworks.sh"

# Ejecutar script de Programas Adicionales
echo "-> Paso 18: Instalando programas adicionales..."
"$SCRIPT_DIR/extras.sh"

# Ejecutar script de Apariencia
echo "-> Paso 19: Configurando apariencia y modo oscuro..."
"$SCRIPT_DIR/appearance.sh"

# Ejecutar script de Easter Eggs
echo "-> Paso 20: Instalando easter eggs y chistes internos..."
"$SCRIPT_DIR/easter_eggs.sh"

echo "=========================================="
echo "Todo el proceso de instalacion ha finalizado exitosamente!"
echo "=========================================="
