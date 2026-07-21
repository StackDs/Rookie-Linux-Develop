#!/bin/bash

# Evitar que se ejecute más de una vez por usuario
if [ -f "$HOME/.config/rookie_verified" ]; then
    exit 0
fi

# Forzar la configuración del fondo de pantalla en el primer inicio (workaround GNOME)
if command -v gsettings &> /dev/null; then
    gsettings set org.gnome.desktop.background picture-uri "file:///usr/share/backgrounds/rookie-wallpaper.png"
    gsettings set org.gnome.desktop.background picture-uri-dark "file:///usr/share/backgrounds/rookie-wallpaper.png"
    gsettings set org.gnome.desktop.background picture-options "zoom"
    gsettings set org.gnome.desktop.background primary-color "#000000"
    gsettings set org.gnome.desktop.background secondary-color "#000000"
    gsettings set org.gnome.desktop.background color-shading-type "solid"
    gsettings set org.gnome.desktop.screensaver picture-uri "file:///usr/share/backgrounds/rookie-wallpaper.png"
    gsettings set org.gnome.desktop.screensaver picture-options "zoom"
fi

echo -e "\e[1;36m====================================================\e[0m"
echo -e "\e[1;36m  Verificando TODO el software de Rookie Linux\e[0m"
echo -e "\e[1;36m====================================================\e[0m"
echo ""

# Comandos binarios directos (agrupados por categorías)
commands=(
    # IDEs y Editores
    "code" "emacs" "antigravity" "nano" "vim" "nvim"
    # Bases de Datos
    "dbeaver-ce" "psql" "sqlite3"
    # C/C++ y compiladores
    "gcc" "g++" "gdb" "make" "cmake" "clang" "clang++" "ninja" "valgrind"
    # Java y .NET
    "java" "javac" "mvn" "dotnet"
    # Python
    "python3" "pip3" "pipx" "black" "flake8" "ipython3" "jupyter"
    # Node y TypeScript
    "node" "npm" "tsc" "eslint" "prettier"
    # Contenedores
    "docker" "docker-compose"
    # Git
    "git" "git-lfs" "gh"
    # Terminal
    "zsh" "tmux" "htop" "btop" "tree" "curl" "wget" "unzip" "zip" "7z" "rar" "unrar" "jq" "rg" "fd" "bat" "fzf" "ncdu"
    # Navegadores, Ofimática y Multimedia
    "brave-browser" "firefox" "chromium-browser" "libreoffice" "evince" "vlc" "obs"
    # Frameworks SDK
    "flutter" "dart"
)

for cmd in "${commands[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        echo -e "[\e[1;32m OK \e[0m] $cmd"
    else
        echo -e "[\e[1;31mFALLO\e[0m] $cmd"
    fi
done

echo ""
echo -e "\e[1;33m--- Bibliotecas C/C++ ---\e[0m"
cpp_libs=("libsdl2-dev" "libsfml-dev" "libgl1-mesa-dev" "libglfw3-dev" "libglew-dev")
for lib in "${cpp_libs[@]}"; do
    if dpkg -l | grep -q "^ii  $lib"; then
        echo -e "[\e[1;32m OK \e[0m] $lib"
    else
        echo -e "[\e[1;31mFALLO\e[0m] $lib"
    fi
done

echo ""
echo -e "\e[1;33m--- Módulos Python ---\e[0m"
# Verificando modulos internos y de librerías
py_modules=("venv" "numpy" "pandas" "matplotlib" "scipy" "requests" "flask" "django" "fastapi")
for mod in "${py_modules[@]}"; do
    if python3 -c "import $mod" &> /dev/null; then
        echo -e "[\e[1;32m OK \e[0m] python-$mod"
    else
        echo -e "[\e[1;31mFALLO\e[0m] python-$mod"
    fi
done

echo ""
echo -e "\e[1;33m--- Instalaciones Especiales ---\e[0m"

# JFLAP
if [ -s "/opt/jflap/JFLAP.jar" ] && command -v jflap &> /dev/null; then
    echo -e "[\e[1;32m OK \e[0m] jflap"
else
    echo -e "[\e[1;31mFALLO\e[0m] jflap"
fi

# IntelliJ IDEA (Flatpak)
if command -v flatpak &> /dev/null && flatpak list | grep -q "com.jetbrains.IntelliJ-IDEA-Community"; then
    echo -e "[\e[1;32m OK \e[0m] intellij-idea-community"
else
    echo -e "[\e[1;31mFALLO\e[0m] intellij-idea-community"
fi

# pgAdmin4
if [ -d "/usr/pgadmin4" ] || command -v pgadmin4 &> /dev/null; then
    echo -e "[\e[1;32m OK \e[0m] pgadmin4-desktop"
else
    echo -e "[\e[1;31mFALLO\e[0m] pgadmin4-desktop"
fi

echo ""
echo -e "\e[1;36m====================================================\e[0m"
echo "Verificación finalizada."
echo "Presiona Enter para cerrar esta ventana..."
read

# Registrar que ya se verificó para no mostrar de nuevo al reiniciar
mkdir -p "$HOME/.config"
touch "$HOME/.config/rookie_verified"
