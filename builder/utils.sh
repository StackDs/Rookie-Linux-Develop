#!/bin/bash

# ==========================================
# Rookie-Linux-Develop
# Utilidades generales del Builder
# ==========================================


# Colores
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m"


# Directorio raíz del proyecto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"


# Directorio de logs
LOG_DIR="$PROJECT_ROOT/logs"


# Archivo de log principal
LOG_FILE="$LOG_DIR/build.log"



# ==========================================
# Crear directorios necesarios
# ==========================================

create_directories(){

    mkdir -p "$LOG_DIR"
    mkdir -p "$PROJECT_ROOT/downloads/iso"
    mkdir -p "$PROJECT_ROOT/downloads/sha256"
    mkdir -p "$PROJECT_ROOT/work"
    mkdir -p "$PROJECT_ROOT/output"

}



# ==========================================
# Sistema de logs
# ==========================================

write_log(){

    mkdir -p "$LOG_DIR"

    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"

}



# ==========================================
# Mensajes
# ==========================================


info(){

    echo -e "${BLUE}[INFO]${NC} $1"
    write_log "[INFO] $1"

}


success(){

    echo -e "${GREEN}[OK]${NC} $1"
    write_log "[OK] $1"

}


warning(){

    echo -e "${YELLOW}[WARNING]${NC} $1"
    write_log "[WARNING] $1"

}


error(){

    echo -e "${RED}[ERROR]${NC} $1"
    write_log "[ERROR] $1"

}



# ==========================================
# Comprobar comandos
# ==========================================

check_command(){

    if ! command -v "$1" &> /dev/null
    then
        error "El comando '$1' no está instalado"
        exit 1
    fi

}



# ==========================================
# Descargar archivos
# ==========================================

download_file(){

    URL=$1
    OUTPUT=$2


    info "Descargando:"
    echo "$URL"


    wget \
        --progress=bar \
        -O "$OUTPUT" \
        "$URL"


    if [ $? -eq 0 ]
    then
        success "Descarga completada"
    else
        error "Falló la descarga"
        exit 1
    fi

}