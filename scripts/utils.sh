#!/bin/bash
# ==========================================
# Funciones Utilitarias para Instalacion Robusta
# ==========================================

# Asegura que apt no haga preguntas interactivas
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a
export NEEDRESTART_SUSPEND=1

# ==========================================
# Deteccion de Sistema Operativo
# ==========================================
if [ -f /etc/os-release ]; then
    . /etc/os-release
    export OS=$ID
else
    echo "No se pudo detectar el sistema operativo."
    export OS="unknown"
fi

# Detectar la "familia" del SO para usar el gestor de paquetes correcto
case "$OS" in
    ubuntu|debian|linuxmint|pop)
        export OS_FAMILY="debian"
        ;;
    fedora|rhel|centos|rocky|almalinux)
        export OS_FAMILY="redhat"
        ;;
    arch|manjaro|endeavouros)
        export OS_FAMILY="arch"
        ;;
    opensuse*)
        export OS_FAMILY="suse"
        ;;
    *)
        export OS_FAMILY="unknown"
        ;;
esac

# Helpers para chequeos rapidos
is_debian() { [ "$OS_FAMILY" = "debian" ]; }
is_fedora() { [ "$OS_FAMILY" = "redhat" ]; }
is_arch() { [ "$OS_FAMILY" = "arch" ]; }
is_suse() { [ "$OS_FAMILY" = "suse" ]; }

# ==========================================
# Gestor de Paquetes Generico
# ==========================================

pkg_update() {
    if is_debian; then
        safe_apt_update
    elif is_fedora; then
        sudo dnf check-update || true
    elif is_arch; then
        sudo pacman -Sy --noconfirm
    elif is_suse; then
        sudo zypper refresh
    else
        echo "[!] OS_FAMILY $OS_FAMILY no soportado para pkg_update"
    fi
}

pkg_install() {
    local packages="$*"
    if is_debian; then
        safe_apt_install $packages
    elif is_fedora; then
        echo ">>> Intentando instalar (DNF): $packages"
        sudo dnf install -y $packages || true
    elif is_arch; then
        echo ">>> Intentando instalar (Pacman): $packages"
        sudo pacman -S --noconfirm --needed $packages || true
    elif is_suse; then
        echo ">>> Intentando instalar (Zypper): $packages"
        sudo zypper install -y $packages || true
    else
        echo "[!] OS_FAMILY $OS_FAMILY no soportado para pkg_install ($packages)"
    fi
}

wait_for_network() {
    echo ">>> Verificando conectividad a internet..."
    for i in {1..15}; do
        ping -c 1 8.8.8.8 >/dev/null 2>&1 && return 0
        echo "    Esperando red... ($i/15)"
        sleep 2
    done
    echo "[!] Problemas de conectividad. Forzando DNS de Google..."
    echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf >/dev/null || true
}

wait_for_dpkg_lock() {
    echo ">>> Verificando bloqueos de dpkg/apt..."
    while sudo fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1 || sudo fuser /var/lib/apt/lists/lock >/dev/null 2>&1 || sudo fuser /var/lib/dpkg/lock >/dev/null 2>&1; do
        echo "    Esperando a que otro proceso libere apt/dpkg..."
        sleep 5
    done
}

fix_dpkg_errors() {
    echo "[!] Detectado error en apt/dpkg. Intentando autoreparacion..."
    sudo dpkg --configure -a || true
    sudo apt-get --fix-broken install -y || true
}

safe_apt_update() {
    wait_for_network
    wait_for_dpkg_lock
    if ! sudo DEBIAN_FRONTEND=noninteractive apt-get update; then
        echo "[!] Fallo al actualizar repositorios, pero continuaremos..."
    fi
}

safe_apt_install() {
    local package="$*"
    wait_for_dpkg_lock
    echo ">>> Intentando instalar: $package"
    if ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y $package; then
        fix_dpkg_errors
        # Segundo intento
        if ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y $package; then
            echo "[ERROR] Fallo critico instalando: $package. Saltando..."
        fi
    fi
}

safe_snap_install() {
    local package="$1"
    local flags="$2"
    echo ">>> Intentando instalar snap: $package"
    for i in {1..5}; do
        if sudo snap install $package $flags; then
            return 0
        fi
        echo "    Fallo instalacion de snap. Esperando a que snapd responda... ($i/5)"
        sleep 5
    done
    echo "[ERROR] No se pudo instalar el snap $package."
}

safe_flatpak_install() {
    local remote="$1"
    local package="$2"
    echo ">>> Intentando instalar flatpak: $package"
    if ! timeout 60 flatpak remote-add --if-not-exists $remote https://dl.flathub.org/repo/flathub.flatpakrepo; then
        echo "[!] No se pudo anadir el remote $remote"
    fi
    if ! sudo timeout 300 flatpak install -y $remote $package; then
        echo "[ERROR] No se pudo instalar el flatpak $package."
    fi
}

safe_curl() {
    local url="$1"
    local out="$2"
    echo ">>> Descargando: $url"
    for i in {1..3}; do
        if curl -fsSL --connect-timeout 10 "$url" -o "$out"; then
            return 0
        fi
        echo "    Reintentando descarga... ($i/3)"
        sleep 3
    done
    echo "[ERROR] Fallo la descarga de $url"
}
