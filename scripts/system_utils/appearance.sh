#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

# Asegurarse de que el script se esta ejecutando desde el directorio correcto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Configurando Apariencia de Rookie Linux"
echo "=========================================="

# 1. Copiar el fondo de pantalla
echo "-> Copiando wallpaper al sistema..."
mkdir -p /usr/share/backgrounds
cp "$SCRIPT_DIR/../assets/wallpaper.png" /usr/share/backgrounds/rookie-wallpaper.png
chmod 644 /usr/share/backgrounds/rookie-wallpaper.png

# 2. Configurar el esquema por defecto para GNOME (Ubuntu)
echo "-> Modificando esquemas de GNOME..."
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

# 2.1 Registrar el wallpaper en GNOME (Evita bugs donde GNOME no carga fondos no registrados)
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

# 3. Recompilar los esquemas para que todos los nuevos usuarios hereden esta config
glib-compile-schemas /usr/share/glib-2.0/schemas/

# 4. Reemplazar fondo de pantalla de Ubuntu por fuerza bruta
echo "-> Forzando el fondo de pantalla por defecto de Ubuntu..."
UBUNTU_DEFAULT="/usr/share/backgrounds/warty-final-ubuntu.png"
if [ -f "$UBUNTU_DEFAULT" ] || [ -L "$UBUNTU_DEFAULT" ]; then
    rm -f "$UBUNTU_DEFAULT"
    ln -s /usr/share/backgrounds/rookie-wallpaper.png "$UBUNTU_DEFAULT"
fi

echo "[OK] Apariencia (Modo Oscuro + Wallpaper) configurada exitosamente."

