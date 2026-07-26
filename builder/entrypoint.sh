#!/bin/bash
# ==========================================
# Wrapper que limpia CRLF y ejecuta un script
# Uso: entrypoint.sh <script.sh> [args...]
# ==========================================

# Convertir todos los scripts del builder a LF (quitar \r de Windows)
find /workspace/builder -name "*.sh" -exec sed -i 's/\r$//' {} + 2>/dev/null || true
find /workspace/scripts -name "*.sh" -exec sed -i 's/\r$//' {} + 2>/dev/null || true

# Convertir templates (user-data, preseed, kickstart, service files)
find /workspace/builder/templates -type f -exec sed -i 's/\r$//' {} + 2>/dev/null || true

# Ejecutar el script solicitado con todos sus argumentos
SCRIPT="$1"
shift
exec bash "$SCRIPT" "$@"
