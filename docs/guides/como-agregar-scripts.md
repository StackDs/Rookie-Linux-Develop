# Cómo agregar scripts de instalación

Esta guía explica cómo añadir nuevas herramientas, IDEs o lenguajes al catálogo de software que se instala automáticamente en el primer arranque del sistema Linux generado.

---

## Arquitectura de los scripts

Todos los scripts de instalación viven en `scripts/` y están organizados en módulos por categoría:

```
scripts/
├── install.sh              ← Director de orquesta: llama a todos los módulos
├── verify_installation.sh  ← Verifica el resultado de la instalación
├── core/
│   ├── utils.sh            ← Funciones de logging y utilidad (log_info, log_error, etc.)
│   ├── update.sh           ← Actualización del sistema (apt update/upgrade)
│   └── rookie-verify.sh    ← Verificación post-instalación
├── ide_tools/              ← Editores e IDEs
├── languages/              ← Lenguajes de programación y compiladores
└── system_utils/           ← Utilidades del sistema, Docker, git, terminal
```

---

## Paso 1: Elegir la categoría correcta

| Quiero añadir... | Carpeta |
|---|---|
| Un nuevo IDE o editor de texto | `scripts/ide_tools/` |
| Un lenguaje de programación o compilador | `scripts/languages/` |
| Una herramienta del sistema (git, docker, etc.) | `scripts/system_utils/` |
| Una base de datos o cliente | `scripts/ide_tools/database_tools.sh` |
| Un navegador web | `scripts/system_utils/browsers.sh` |
| Software multimedia | `scripts/system_utils/multimedia.sh` |

---

## Paso 2: Escribir el script

Crea un nuevo archivo `.sh` en la carpeta correspondiente o edita uno existente.

### Estructura recomendada de un script:

```bash
#!/bin/bash
# Descripción: Instala [Nombre de la herramienta]
# Parte de: scripts/categoria/

# Cargar utilidades de logging
source "$(dirname "${BASH_SOURCE[0]}")/../core/utils.sh"

install_mi_herramienta() {
    log_info "Instalando Mi Herramienta..."
    
    # Verificar si ya está instalada
    if command -v mi-herramienta &>/dev/null; then
        log_info "Mi Herramienta ya está instalada. Omitiendo."
        return 0
    fi
    
    # Instalar desde repositorio oficial
    if command -v apt &>/dev/null; then
        # Debian/Ubuntu/Mint
        sudo apt-get install -y mi-paquete || log_error "Falló la instalación de Mi Herramienta"
    elif command -v dnf &>/dev/null; then
        # Fedora
        sudo dnf install -y mi-paquete || log_error "Falló la instalación de Mi Herramienta"
    fi
    
    log_info "Mi Herramienta instalada exitosamente."
}

# Llamar a la función principal
install_mi_herramienta
```

### Buenas prácticas

- ✅ Siempre verifica si la herramienta ya existe antes de instalar (`command -v` o `which`).
- ✅ Soporta múltiples gestores de paquetes (`apt`, `dnf`).
- ✅ Usa las funciones de logging de `utils.sh` (`log_info`, `log_error`, `log_warning`).
- ✅ Nunca uses `set -e`. Maneja los errores explícitamente para que un fallo individual no detenga toda la instalación.
- ✅ Para herramientas que requieren descarga de `.deb` o `.tar.gz`, verifica el checksum si el proveedor lo ofrece.

---

## Paso 3: Registrar el script en `install.sh`

El archivo `scripts/install.sh` es quien llama a todos los módulos. Añade una línea `source` en la sección correspondiente:

```bash
# En scripts/install.sh, sección "IDEs y Editores":
source "$SCRIPTS_DIR/ide_tools/mi_nuevo_script.sh"
```

O si añadiste la función a un archivo existente, simplemente llámala:

```bash
# Si añadiste install_mi_herramienta() a ide.sh:
install_mi_herramienta
```

---

## Paso 4: Actualizar la pantalla de información

La pantalla `InfoScreen` (`frontend/screens/info_manuals/info_screen.py`) muestra una lista de lo que incluye la ISO. Añade tu herramienta en el texto correspondiente:

```python
self.info_text = (
    ...
    "[+] IDEs y EDITORES\n"
    "    - Visual Studio Code\n"
    "    - Mi Nueva Herramienta\n"  # ← Añadir aquí
    ...
)
```

Y si corresponde, actualiza también la pantalla de `DocumentationScreen` con un link a la documentación oficial.

---

## Paso 5: Actualizar el catálogo de scripts

Documenta la nueva herramienta en la referencia:
→ [`reference/catalogo-de-scripts.md`](../reference/catalogo-de-scripts.md)

---

## Ejemplo completo: Añadir Neovim

```bash
# scripts/ide_tools/editors.sh (añadir a archivo existente)

install_neovim() {
    log_info "Instalando Neovim..."
    
    if command -v nvim &>/dev/null; then
        log_info "Neovim ya está instalado."
        return 0
    fi
    
    NVIM_VERSION="0.10.0"
    NVIM_URL="https://github.com/neovim/neovim/releases/download/v${NVIM_VERSION}/nvim-linux64.tar.gz"
    
    wget -q -O /tmp/nvim.tar.gz "$NVIM_URL"
    tar -xzf /tmp/nvim.tar.gz -C /opt/
    ln -sf /opt/nvim-linux64/bin/nvim /usr/local/bin/nvim
    rm /tmp/nvim.tar.gz
    
    log_info "Neovim $NVIM_VERSION instalado."
}

install_neovim
```
