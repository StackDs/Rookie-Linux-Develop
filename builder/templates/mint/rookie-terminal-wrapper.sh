#!/bin/bash
# Wrapper para lanzar un script en la terminal disponible

SCRIPT="${1:-/opt/rookie-scripts/rookie-firstboot.sh}"

if command -v gnome-terminal >/dev/null 2>&1; then
    # GNOME (Ubuntu, Pop!_OS 22.04, Mint con metapaquete GNOME)
    gnome-terminal -- bash -c "$SCRIPT; exec bash"
elif command -v x-terminal-emulator >/dev/null 2>&1; then
    # Fallback genérico Debian/Ubuntu/Mint (suele apuntar a xterm o nemo-terminal)
    x-terminal-emulator -e "bash -c '$SCRIPT; exec bash'"
elif command -v xterm >/dev/null 2>&1; then
    # xterm como último recurso
    xterm -e "bash -c '$SCRIPT; exec bash'"
else
    # Si todo falla, ejecutar directamente en el proceso actual
    bash -c "$SCRIPT"
fi
