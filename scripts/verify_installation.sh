#!/bin/bash

# Evitar que se ejecute más de una vez por usuario
if [ -f "$HOME/.config/rookie_verified" ]; then
    exit 0
fi

echo -e "\e[1;36m====================================================\e[0m"
echo -e "\e[1;36m  Verificando herramientas de Rookie Linux\e[0m"
echo -e "\e[1;36m====================================================\e[0m"
echo ""

commands=("git" "curl" "wget" "docker" "node" "npm" "python3" "gcc" "g++" "java" "dotnet" "tsc" "prettier" "fd" "libreoffice" "glxinfo")

for cmd in "${commands[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        echo -e "[\e[1;32m OK \e[0m] $cmd"
    else
        echo -e "[\e[1;31mFALLO\e[0m] $cmd no encontrado"
    fi
done

echo ""
echo -e "\e[1;36m====================================================\e[0m"
echo "Verificación finalizada."
echo "Presiona Enter para cerrar esta ventana..."
read

# Registrar que ya se verificó para no mostrar de nuevo al reiniciar
mkdir -p "$HOME/.config"
touch "$HOME/.config/rookie_verified"
