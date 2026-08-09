#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/utils.sh"

echo "=========================================="
echo "Configurando Apariencia de Rookie Linux"
echo "=========================================="

# 1. Copiar el fondo de pantalla al sistema
echo "-> Copiando wallpaper al sistema..."
mkdir -p /usr/share/backgrounds
cp "$SCRIPT_DIR/../../assets/wallpaper.png" /usr/share/backgrounds/rookie-wallpaper.png
chmod 644 /usr/share/backgrounds/rookie-wallpaper.png

# 2. Registrar el wallpaper en el catalogo GNOME (necesario para Ubuntu/Pop! con GNOME/Mint-GNOME)
mkdir -p /usr/share/gnome-background-properties
cat << 'EOF' > /usr/share/gnome-background-properties/rookie-wallpaper.xml
<?xml version="1.0"?>
<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
<wallpapers>
  <wallpaper deleted="false">
    <name>Rookie Linux</name>
    <filename>/usr/share/backgrounds/rookie-wallpaper.png</filename>
    <filename-dark>/usr/share/backgrounds/rookie-wallpaper.png</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#000000</pcolor>
    <scolor>#000000</scolor>
  </wallpaper>
</wallpapers>
EOF

# 3. Configurar esquemas GLib segun el DE detectado
if [ -d /usr/share/glib-2.0/schemas ]; then

    # --- GNOME (Ubuntu, Mint con GNOME) ---
    cat << 'EOF' > /usr/share/glib-2.0/schemas/99_rookie_linux.gschema.override
[org.gnome.desktop.background]
picture-uri='file:///usr/share/backgrounds/rookie-wallpaper.png'
picture-uri-dark='file:///usr/share/backgrounds/rookie-wallpaper.png'
picture-options='zoom'
primary-color='#000000'
secondary-color='#000000'
color-shading-type='solid'

[org.gnome.desktop.screensaver]
picture-uri='file:///usr/share/backgrounds/rookie-wallpaper.png'
picture-options='zoom'
primary-color='#000000'
secondary-color='#000000'
color-shading-type='solid'

[org.gnome.desktop.interface]
color-scheme='prefer-dark'
EOF

    # --- Cinnamon (Linux Mint) ---
    if ls /usr/share/glib-2.0/schemas/ 2>/dev/null | grep -q "cinnamon"; then
        cat << 'EOF' >> /usr/share/glib-2.0/schemas/99_rookie_linux.gschema.override

[org.cinnamon.desktop.background]
picture-uri='file:///usr/share/backgrounds/rookie-wallpaper.png'
picture-options='zoom'

[org.cinnamon.desktop.screensaver]
picture-uri='file:///usr/share/backgrounds/rookie-wallpaper.png'
picture-options='zoom'
EOF
    fi

    echo "-> Compilando esquemas de GLib..."
    glib-compile-schemas /usr/share/glib-2.0/schemas/ 2>/dev/null || true
fi

# 4. Configurar wallpaper para Cosmic DE (Pop!_OS 24.04+)
# Cosmic no usa GLib schemas: usa archivos RON en ~/.config/cosmic/
# Se inyectan en /etc/skel para que el primer usuario creado los herede.
if command -v cosmic-settings >/dev/null 2>&1 || [ -d /usr/lib/cosmic ]; then
    echo "-> Configurando wallpaper para Cosmic DE (Pop!_OS 24.04+)..."
    COSMIC_BG_DIR="/etc/skel/.config/cosmic/com.system76.CosmicBackground/v1"
    mkdir -p "$COSMIC_BG_DIR"

    # Formato RON de Cosmic para el fondo de pantalla (aplica a todas las pantallas)
    cat << 'EOF' > "$COSMIC_BG_DIR/all"
Some(Entry(source: Path("/usr/share/backgrounds/rookie-wallpaper.png"), filter: Lanczos, scaling_mode: Zoom, rotation_frequency: 3600, color: None, colors: None, same_on_all: true, output: All))
EOF
    chmod 644 "$COSMIC_BG_DIR/all"

    # Tambien aplicar a root por si el script de verify corre como root
    ROOT_COSMIC_DIR="/root/.config/cosmic/com.system76.CosmicBackground/v1"
    mkdir -p "$ROOT_COSMIC_DIR"
    cp "$COSMIC_BG_DIR/all" "$ROOT_COSMIC_DIR/all"

    # Aplicar al usuario actual (SUDO_USER) porque el usuario ya fue creado
    if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then
        USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
        if [ -n "$USER_HOME" ]; then
            USER_COSMIC_DIR="$USER_HOME/.config/cosmic/com.system76.CosmicBackground/v1"
            mkdir -p "$USER_COSMIC_DIR"
            cp "$COSMIC_BG_DIR/all" "$USER_COSMIC_DIR/all"
            chown -R "$SUDO_USER:$SUDO_USER" "$USER_HOME/.config/cosmic"
        fi
    fi

    echo "   [OK] Config Cosmic creada en /etc/skel, /root y \$USER_HOME"
fi

# 5. Reemplazar wallpapers por defecto de las distros (fuerza bruta como fallback)
echo "-> Forzando el fondo de pantalla por defecto..."
for default_wp in \
    "/usr/share/backgrounds/warty-final-ubuntu.png" \
    "/usr/share/backgrounds/pop/nasa-108.png" \
    "/usr/share/backgrounds/linuxmint/linuxmint-logo-ring-warmgrey.png"; do
    if [ -f "$default_wp" ] || [ -L "$default_wp" ]; then
        rm -f "$default_wp"
        ln -s /usr/share/backgrounds/rookie-wallpaper.png "$default_wp"
        echo "   [OK] Reemplazado: $default_wp"
    fi
done

echo "[OK] Apariencia (Modo Oscuro + Wallpaper) configurada exitosamente."
