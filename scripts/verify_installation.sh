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

# ==========================================
# Verificador interactivo de instalacion
# ==========================================

if pgrep -f "scripts/install.sh" > /dev/null || systemctl is-active --quiet rookie-install.service 2>/dev/null || systemctl is-active --quiet rookie-firstboot.service 2>/dev/null; then
    echo -e "\e[1;33m====================================================\e[0m"
    echo -e "\e[1;33m La instalacion automatica sigue ejecutandose...\e[0m"
    echo -e "\e[1;33m Mostrando progreso en vivo (Ctrl+C cancela la vista):\e[0m"
    echo -e "\e[1;33m====================================================\e[0m"
    
    TAIL_PID=""
    if [ -f /var/log/rookie-install-firstboot.log ]; then
        tail -f /var/log/rookie-install-firstboot.log &
        TAIL_PID=$!
    elif [ -f /var/log/rookie-install.log ]; then
        tail -f /var/log/rookie-install.log &
        TAIL_PID=$!
    fi
    
    while pgrep -f "scripts/install.sh" > /dev/null || systemctl is-active --quiet rookie-install.service 2>/dev/null; do
        sleep 5
    done
    
    if [ -n "$TAIL_PID" ]; then
        kill $TAIL_PID 2>/dev/null || true
    fi
    
    echo -e "\n\e[1;32mLa instalacion en segundo plano ha finalizado.\e[0m"
    sleep 2
fi
echo -e "\nProcediendo con la verificacion final...\n"

echo -e "\e[1;36m====================================================\e[0m"
echo -e "\e[1;36m  Verificando TODO el software instalado\e[0m"
echo -e "\e[1;36m====================================================\e[0m"
echo ""

# Comandos binarios directos (agrupados por categorías)
commands=(
    # IDEs y Editores
    "code" "emacs" "nano" "vim" "nvim"
    # Bases de Datos
    "dbeaver-ce|dbeaver" "psql" "sqlite3"
    # C/C++ y compiladores
    "gcc" "g++" "gdb" "make" "cmake" "clang" "clang++" "ninja" "valgrind"
    # Java y .NET
    "java" "javac" "mvn" "dotnet"
    # Python
    "python3" "pip3" "pipx" "black" "flake8" "ipython3|ipython" "jupyter|jupyter-lab"
    # Node y TypeScript
    "node" "npm" "tsc" "eslint" "prettier"
    # Contenedores
    "docker" "docker-compose"
    # Git
    "git" "git-lfs" "gh"
    # Terminal
    "zsh" "tmux" "htop" "btop" "tree" "curl" "wget" "unzip" "zip" "7z" "rar|unrar" "jq" "rg" "fd" "bat" "fzf" "ncdu"
    # Navegadores, Ofimática y Multimedia
    "brave-browser" "firefox" "libreoffice" "evince" "vlc" "obs"
    # Frameworks SDK
    "flutter" "dart" "unityhub"
)

for cmd_group in "${commands[@]}"; do
    IFS='|' read -r -a alts <<< "$cmd_group"
    found=false
    for cmd in "${alts[@]}"; do
        if command -v "$cmd" &> /dev/null; then
            echo -e "[\e[1;32m OK \e[0m] $cmd"
            found=true
            break
        fi
    done
    if [ "$found" = false ]; then
        echo -e "[\e[1;31mFALLO\e[0m] ${alts[0]} (y alternativas)"
    fi
done

echo ""
echo -e "\e[1;33m--- Bibliotecas C/C++ ---\e[0m"
cpp_libs=("libsdl2-dev" "libsfml-dev" "libgl1-mesa-dev" "libglfw3-dev" "libglew-dev")
for lib in "${cpp_libs[@]}"; do
    if command -v dpkg &> /dev/null && dpkg -l | grep -q "^ii  $lib"; then
        echo -e "[\e[1;32m OK \e[0m] $lib"
    elif command -v rpm &> /dev/null; then
        # Fedora naming heuristic (libsdl2-dev -> SDL2-devel, etc.)
        fedora_pkg=$(echo "$lib" | sed -e 's/libsdl2-dev/SDL2-devel/i' -e 's/libsfml-dev/SFML-devel/i' -e 's/libgl1-mesa-dev/mesa-libGL-devel/i' -e 's/libglfw3-dev/glfw-devel/i' -e 's/libglew-dev/glew-devel/i')
        if rpm -qa | grep -iq "^${fedora_pkg%-devel}"; then
            echo -e "[\e[1;32m OK \e[0m] $fedora_pkg"
        else
            echo -e "[\e[1;31mFALLO\e[0m] $fedora_pkg"
        fi
    else
        echo -e "[\e[1;31mFALLO\e[0m] $lib (Gestor no soportado)"
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

# Antigravity (Solo Debian)
if command -v dpkg &> /dev/null; then
    if command -v antigravity &> /dev/null; then
        echo -e "[\e[1;32m OK \e[0m] antigravity"
    else
        echo -e "[\e[1;31mFALLO\e[0m] antigravity"
    fi
else
    echo -e "[\e[1;33mSALTADO\e[0m] antigravity (No soportado nativamente en este SO)"
fi

# IntelliJ IDEA
if command -v idea &> /dev/null; then
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

# Registrar que ya se verificó para no mostrar de nuevo al reiniciar
mkdir -p "$HOME/.config"
touch "$HOME/.config/rookie_verified"
