#!/bin/bash
# Wrapper para lanzar la instalación en la terminal disponible (Fedora)

SCRIPT="/opt/rookie-scripts/rookie-firstboot.sh"

if command -v ptyxis >/dev/null 2>&1; then
    # Ptyxis (Fedora 40+ Workstation)
    ptyxis -e "$SCRIPT"
elif command -v kgx >/dev/null 2>&1; then
    # GNOME Console (Fedora 39 y anteriores)
    kgx -e "$SCRIPT"
elif command -v gnome-terminal >/dev/null 2>&1; then
    # GNOME Terminal (fallback)
    gnome-terminal -- "$SCRIPT"
elif command -v xterm >/dev/null 2>&1; then
    xterm -e "$SCRIPT"
else
    # Ultimo recurso: ejecutar directamente
    bash "$SCRIPT"
fi
