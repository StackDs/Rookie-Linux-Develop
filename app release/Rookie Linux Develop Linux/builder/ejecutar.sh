#!/bin/bash
set -e

# Por defecto, en Docker el proyecto se monta en /workspace
PROJECT_ROOT="/workspace"

echo "=========================================="
echo "Bienvenido al ISO Builder de Rookie Linux"
echo "=========================================="

# Aceptar parametro o variable de entorno (por defecto ubuntu)
export ISO_DISTRO="${1:-${ISO_DISTRO:-ubuntu}}"

echo "-> Paso 1: Obteniendo ISO original de ${ISO_DISTRO}..."
"$PROJECT_ROOT/builder/download_iso.sh" "$ISO_DISTRO"

echo "-> Paso 2: Destripando e Inyectando Scripts (Constructor ISO)..."
"$PROJECT_ROOT/builder/build_iso.sh"

echo "=========================================="
echo "Proceso general de construccion finalizado."
echo "=========================================="
