#!/bin/bash
# Wrapper para lanzar un script en la terminal disponible

SCRIPT="${1:-/opt/rookie-scripts/rookie-firstboot.sh}"

if command -v cosmic-term >/dev/null 2>&1; then
    # Cosmic DE (Pop!_OS 24.04+)
    cosmic-term -e bash -c "$SCRIPT"
elif command -v gnome-terminal >/dev/null 2>&1; then
    # GNOME (Pop!_OS 22.04 y Ubuntu)
    gnome-terminal -- bash -c "$SCRIPT"
elif command -v ptyxis >/dev/null 2>&1; then
    # GNOME Fedora 40+ (Ptyxis)
    ptyxis -- bash -c "$SCRIPT"
elif command -v kgx >/dev/null 2>&1; then
    # GNOME Console (Fedora 39)
    kgx -e "bash -c '$SCRIPT'"
elif command -v x-terminal-emulator >/dev/null 2>&1; then
    # Fallback genérico Debian/Ubuntu
    x-terminal-emulator -e "bash -c '$SCRIPT'"
else
    # Si todo falla, intentar ejecutarlo de todas formas
    bash -c "$SCRIPT"
fi
