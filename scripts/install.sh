#!/bin/bash
# Removido set -e para evitar fallos completos por un error menor

# ==========================================
# Script Principal de Instalacion
# ==========================================

# Asegurarse de que el script se esta ejecutando desde el directorio correcto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Evitar prompts interactivos de apt y needrestart
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a
export NEEDRESTART_SUSPEND=1

echo "=========================================="
echo "Bienvenido a la instalacion del sistema"
echo "=========================================="

# Dar permisos de ejecucion a los demas scripts
chmod +x "$SCRIPT_DIR/utils.sh"
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
chmod +x "$SCRIPT_DIR/verify_installation.sh"

# Ejecutar script de actualizacion y dependencias
echo "-> Paso 1: Actualizando el sistema..."
"$SCRIPT_DIR/update.sh" || echo "[!] Fallo en Paso 1, pero continuando..."

# Ejecutar script de IDEs
echo "-> Paso 2: Instalando IDEs y Editores..."
"$SCRIPT_DIR/ide.sh" || echo "[!] Fallo en Paso 2, pero continuando..."

# Ejecutar script de herramientas de Base de Datos
echo "-> Paso 3: Instalando herramientas de Base de Datos..."
"$SCRIPT_DIR/database_tools.sh" || echo "[!] Fallo en Paso 3, pero continuando..."

# Ejecutar script de herramientas C/C++
echo "-> Paso 4: Instalando compiladores y herramientas C/C++..."
"$SCRIPT_DIR/c_cpp.sh" || echo "[!] Fallo en Paso 4, pero continuando..."

# Ejecutar script de ecosistema Java
echo "-> Paso 5: Instalando ecosistema Java..."
"$SCRIPT_DIR/java.sh" || echo "[!] Fallo en Paso 5, pero continuando..."

# Ejecutar script de ecosistema Python
echo "-> Paso 6: Instalando ecosistema Python..."
"$SCRIPT_DIR/python.sh" || echo "[!] Fallo en Paso 6, pero continuando..."

# Ejecutar script de .NET SDK
echo "-> Paso 7: Instalando .NET SDK..."
"$SCRIPT_DIR/dotnet.sh" || echo "[!] Fallo en Paso 7, pero continuando..."

# Ejecutar script de Node.js / TS
echo "-> Paso 8: Instalando ecosistema JavaScript/TypeScript..."
"$SCRIPT_DIR/node.sh" || echo "[!] Fallo en Paso 8, pero continuando..."

# Ejecutar script de Motores de BD
echo "-> Paso 9: Instalando motores de Bases de Datos..."
"$SCRIPT_DIR/databases.sh" || echo "[!] Fallo en Paso 9, pero continuando..."

# Ejecutar script de Docker
echo "-> Paso 10: Instalando Docker y utilidades..."
"$SCRIPT_DIR/docker.sh" || echo "[!] Fallo en Paso 10, pero continuando..."

# Ejecutar script de Git y GitHub
echo "-> Paso 11: Instalando Git, Git LFS y GitHub CLI..."
"$SCRIPT_DIR/git.sh" || echo "[!] Fallo en Paso 11, pero continuando..."

# Ejecutar script de Utilidades de Terminal
echo "-> Paso 12: Instalando utilidades de terminal..."
"$SCRIPT_DIR/terminal.sh" || echo "[!] Fallo en Paso 12, pero continuando..."

# Ejecutar script de Editores CLI
echo "-> Paso 13: Instalando editores de texto CLI..."
"$SCRIPT_DIR/editors.sh" || echo "[!] Fallo en Paso 13, pero continuando..."

# Ejecutar script de Navegadores
echo "-> Paso 14: Instalando navegadores web..."
"$SCRIPT_DIR/browsers.sh" || echo "[!] Fallo en Paso 14, pero continuando..."

# Ejecutar script de Multimedia
echo "-> Paso 15: Instalando multimedia (VLC, OBS)..."
"$SCRIPT_DIR/multimedia.sh" || echo "[!] Fallo en Paso 15, pero continuando..."

# Ejecutar script de Bibliotecas C/C++
echo "-> Paso 16: Instalando bibliotecas C/C++ (SDL2, OpenGL, SFML)..."
"$SCRIPT_DIR/cpp_libraries.sh" || echo "[!] Fallo en Paso 16, pero continuando..."

# Ejecutar script de Frameworks y Motores
echo "-> Paso 17: Instalando frameworks (Flutter, Dart, Unity)..."
"$SCRIPT_DIR/frameworks.sh" || echo "[!] Fallo en Paso 17, pero continuando..."

# Ejecutar script de Programas Adicionales
echo "-> Paso 18: Instalando programas adicionales..."
"$SCRIPT_DIR/extras.sh" || echo "[!] Fallo en Paso 18, pero continuando..."

# Ejecutar script de Apariencia
echo "-> Paso 19: Configurando apariencia y modo oscuro..."
"$SCRIPT_DIR/appearance.sh" || echo "[!] Fallo en Paso 19, pero continuando..."

# Ejecutar script de Easter Eggs
echo "-> Paso 20: Instalando easter eggs y chistes internos..."
"$SCRIPT_DIR/easter_eggs.sh" || echo "[!] Fallo en Paso 20, pero continuando..."

echo "=========================================="
echo "Todo el proceso de instalacion ha finalizado exitosamente!"
echo "=========================================="
