#!/bin/bash

set -e

source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"

ISO_DISTRO="${1:-${ISO_DISTRO:-ubuntu}}"
ISO_DISTRO="$(printf '%s' "$ISO_DISTRO" | tr '[:upper:]' '[:lower:]')"

ISO_NAME="${ISO_NAME:-}"
ISO_URL="${ISO_URL:-}"
DOWNLOAD_DIR="$PROJECT_ROOT/downloads/iso/$ISO_DISTRO"

# Resuelve el nombre y la URL segun la distro elegida.
resolve_iso_source(){

    case "$1" in
        ubuntu)
            # Ubuntu: toma la ultima imagen desktop disponible para la version pedida.
            UBUNTU_VERSION="${UBUNTU_VERSION:-24.04}"
            UBUNTU_FLAVOR="${UBUNTU_FLAVOR:-desktop}"
            UBUNTU_ARCH="${UBUNTU_ARCH:-amd64}"

            UBUNTU_MIRROR="${UBUNTU_MIRROR:-https://releases.ubuntu.com/${UBUNTU_VERSION}/}"

            if [ -z "$ISO_NAME" ]; then
                UBUNTU_INDEX="$(wget -qO- "$UBUNTU_MIRROR" 2>/dev/null || true)"
                ISO_NAME="$(printf '%s\n' "$UBUNTU_INDEX" \
                    | grep -oE "ubuntu-${UBUNTU_VERSION}\\.[0-9]+-${UBUNTU_FLAVOR}-${UBUNTU_ARCH}\\.iso" \
                    | sort -V \
                    | tail -n1)"
            fi

            if [ -z "$ISO_NAME" ]; then
                error "No se pudo resolver una ISO de Ubuntu para ${UBUNTU_VERSION}/${UBUNTU_FLAVOR}/${UBUNTU_ARCH}"
                echo "Puedes definir ISO_URL o ISO_NAME manualmente."
                exit 1
            fi

            ISO_URL="${ISO_URL:-${UBUNTU_MIRROR}${ISO_NAME}}"
            ;;
        mint)
            # Mint: usa una ruta estable basada en version y edicion.
            MINT_VERSION="${MINT_VERSION:-22.1}"
            MINT_EDITION="${MINT_EDITION:-cinnamon}"
            MINT_ARCH="${MINT_ARCH:-64bit}"

            ISO_NAME="${ISO_NAME:-linuxmint-${MINT_VERSION}-${MINT_EDITION}-${MINT_ARCH}.iso}"
            ISO_URL="${ISO_URL:-https://mirrors.edge.kernel.org/linuxmint/stable/${MINT_VERSION}/${ISO_NAME}}"
            ;;
        fedora)
            # Fedora: Para soportar Kickstart con scripts %post, no podemos usar ISOs Live.
            # Usamos la edicion "Server" (netinst) que realiza una instalacion real por paquetes y soporta el grupo Workstation.
            FEDORA_VERSION="${FEDORA_VERSION:-41}"
            FEDORA_PRODUCT="${FEDORA_PRODUCT:-Server}"
            FEDORA_ARCH="${FEDORA_ARCH:-x86_64}"
            FEDORA_MIRROR="${FEDORA_MIRROR:-https://download.fedoraproject.org/pub/fedora/linux/releases/${FEDORA_VERSION}/${FEDORA_PRODUCT}/${FEDORA_ARCH}/iso/}"

            if [ -z "$ISO_NAME" ]; then
                FEDORA_INDEX="$(wget -qO- "$FEDORA_MIRROR" 2>/dev/null || true)"
                ISO_NAME="$(printf '%s\n' "$FEDORA_INDEX" \
                    | grep -oE 'href="[^"]+\.iso"' \
                    | sed -E 's/^href="//; s/"$//' \
                    | grep "Fedora-${FEDORA_PRODUCT}" \
                    | grep "${FEDORA_VERSION}" \
                    | grep "${FEDORA_ARCH}" \
                    | grep "netinst" \
                    | sort -V \
                    | tail -n1)"
            fi

            if [ -z "$ISO_NAME" ]; then
                echo "[WARN] No se pudo resolver dinámicamente la ISO. Usando fallback por defecto."
                ISO_NAME="Fedora-Server-netinst-x86_64-41-1.4.iso"
            fi

            ISO_URL="${ISO_URL:-${FEDORA_MIRROR}${ISO_NAME}}"
            ;;
        pop|popos|pop-os|pop-nvidia|popos-nvidia|pop_nvidia|popos_amd|pop_amd|popos_*)
            # Pop!_OS: intenta resolver desde el mirror; si cambia el layout, usa ISO_URL/ISO_NAME.
            POP_VERSION="${POP_VERSION:-24.04}"
            POP_ARCH="${POP_ARCH:-amd64}"

            # Si el argumento contiene 'nvidia', forzamos esa variante a menos que ya este definida.
            if [[ "$1" == *nvidia* ]]; then
                POP_VARIANT="${POP_VARIANT:-nvidia}"
            else
                POP_VARIANT="${POP_VARIANT:-generic}"
            fi

            case "$POP_VARIANT" in
                intel|amd64|generic)
                    POP_VARIANT="generic"
                    ;;
                nvidia)
                    POP_VARIANT="nvidia"
                    ;;
                *)
                    error "Pop!_OS solo soporta ahora variantes intel/amd y nvidia"
                    echo "Usa POP_VARIANT=generic o POP_VARIANT=nvidia"
                    exit 1
                    ;;
            esac

            POP_API_URL="${POP_API_URL:-https://api.pop-os.org/builds/${POP_VERSION}/${POP_VARIANT}?arch=${POP_ARCH}}"

            if [ -z "$ISO_URL" ]; then
                POP_JSON="$(wget -qO- "$POP_API_URL" 2>/dev/null || true)"
                ISO_URL="$(printf '%s\n' "$POP_JSON" | grep -oE '"url":"[^"]+"' | cut -d'"' -f4)"
            fi

            if [ -z "$ISO_URL" ]; then
                error "No se pudo resolver una ISO de Pop!_OS para ${POP_VERSION}/${POP_ARCH}/${POP_VARIANT}"
                echo "Intentado con la API: ${POP_API_URL}"
                echo "Puedes definir ISO_URL o ISO_NAME manualmente."
                exit 1
            fi

            if [ -z "$ISO_NAME" ]; then
                ISO_NAME="${ISO_URL##*/}"
            fi
            ;;
        *)
            error "Distro no soportada: $1"
            echo "Uso: $0 [ubuntu|mint|fedora|pop|pop-nvidia]"
            echo "Variables opcionales: ISO_URL, ISO_NAME, ISO_DISTRO"
            echo "Ubuntu: UBUNTU_VERSION, UBUNTU_FLAVOR, UBUNTU_ARCH, UBUNTU_MIRROR"
            echo "Mint: MINT_VERSION, MINT_EDITION, MINT_ARCH"
            echo "Fedora: FEDORA_VERSION, FEDORA_PRODUCT, FEDORA_ARCH, FEDORA_MIRROR"
            echo "Pop!_OS: POP_VERSION, POP_ARCH, POP_VARIANT, POP_DOWNLOAD_PAGE"
            exit 1
            ;;
    esac

}

echo "=== Descargando imagen ISO de ${ISO_DISTRO} ==="

create_directories
# Dar 1 segundo a Docker Desktop para Windows para sincronizar la carpeta creada por Python
sleep 1
mkdir -p "$DOWNLOAD_DIR"
check_command wget
check_command curl

resolve_iso_source "$ISO_DISTRO"

mkdir -p "$DOWNLOAD_DIR"

if [ -f "$DOWNLOAD_DIR/$ISO_NAME" ]; then
    info "La ISO $ISO_NAME ya existe en $DOWNLOAD_DIR."
else
    download_file "$ISO_URL" "$DOWNLOAD_DIR/$ISO_NAME"
fi