# How to add installation scripts

This guide explains how to add new tools, IDEs, or languages to the software catalog that is automatically installed on the first boot of the generated Linux system.

---

## Script Architecture

All installation scripts live in `scripts/` and are organized in modules by category:

```
scripts/
├── install.sh              ← Orchestrator: calls all modules
├── verify_installation.sh  ← Verifies the installation result
├── core/
│   ├── utils.sh            ← Logging and utility functions (log_info, log_error, etc.)
│   ├── update.sh           ← System update (apt update/upgrade)
│   └── rookie-verify.sh    ← Post-installation verification
├── ide_tools/              ← Text editors and IDEs
├── languages/              ← Programming languages and compilers
└── system_utils/           ← System utilities, Docker, git, terminal
```

---

## Step 1: Choose the correct category

| I want to add... | Folder |
|---|---|
| A new IDE or text editor | `scripts/ide_tools/` |
| A programming language or compiler | `scripts/languages/` |
| A system tool (git, docker, etc.) | `scripts/system_utils/` |
| A database or client | `scripts/ide_tools/database_tools.sh` |
| A web browser | `scripts/system_utils/browsers.sh` |
| Multimedia software | `scripts/system_utils/multimedia.sh` |

---

## Step 2: Write the script

Create a new `.sh` file in the corresponding folder or edit an existing one.

### Recommended structure of a script:

```bash
#!/bin/bash
# Description: Installs [Tool Name]
# Part of: scripts/category/

# Load logging utilities
source "$(dirname "${BASH_SOURCE[0]}")/../core/utils.sh"

install_my_tool() {
    log_info "Installing My Tool..."
    
    # Check if it's already installed
    if command -v my-tool &>/dev/null; then
        log_info "My Tool is already installed. Skipping."
        return 0
    fi
    
    # Install from official repository
    if command -v apt &>/dev/null; then
        # Debian/Ubuntu/Mint
        sudo apt-get install -y my-package || log_error "Failed to install My Tool"
    elif command -v dnf &>/dev/null; then
        # Fedora
        sudo dnf install -y my-package || log_error "Failed to install My Tool"
    fi
    
    log_info "My Tool successfully installed."
}

# Call the main function
install_my_tool
```

### Best Practices

- ✅ Always check if the tool already exists before installing (`command -v` or `which`).
- ✅ Support multiple package managers (`apt`, `dnf`).
- ✅ Use the logging functions from `utils.sh` (`log_info`, `log_error`, `log_warning`).
- ✅ Never use `set -e`. Handle errors explicitly so that an individual failure doesn't stop the entire installation.
- ✅ For tools that require downloading `.deb` or `.tar.gz`, verify the checksum if the provider offers it.

---

## Step 3: Register the script in `install.sh`

The `scripts/install.sh` file is the one that calls all modules. Add a `source` line in the corresponding section:

```bash
# In scripts/install.sh, "IDEs and Editors" section:
source "$SCRIPTS_DIR/ide_tools/my_new_script.sh"
```

Or if you added the function to an existing file, simply call it:

```bash
# If you added install_my_tool() to ide.sh:
install_my_tool
```

---

## Step 4: Update the information screen

The `InfoScreen` screen (`frontend/screens/info_manuals/info_screen.py`) shows a list of what the ISO includes. Add your tool in the corresponding text:

```python
self.info_text = (
    ...
    "[+] IDEs and EDITORS\n"
    "    - Visual Studio Code\n"
    "    - My New Tool\n"  # ← Add here
    ...
)
```

And if applicable, also update the `DocumentationScreen` with a link to the official documentation.

---

## Step 5: Update the script catalog

Document the new tool in the reference:
→ [`reference/script-catalog.md`](../reference/script-catalog.md)

---

## Complete Example: Adding Neovim

```bash
# scripts/ide_tools/editors.sh (add to existing file)

install_neovim() {
    log_info "Installing Neovim..."
    
    if command -v nvim &>/dev/null; then
        log_info "Neovim is already installed."
        return 0
    fi
    
    NVIM_VERSION="0.10.0"
    NVIM_URL="https://github.com/neovim/neovim/releases/download/v${NVIM_VERSION}/nvim-linux64.tar.gz"
    
    wget -q -O /tmp/nvim.tar.gz "$NVIM_URL"
    tar -xzf /tmp/nvim.tar.gz -C /opt/
    ln -sf /opt/nvim-linux64/bin/nvim /usr/local/bin/nvim
    rm /tmp/nvim.tar.gz
    
    log_info "Neovim successfully installed."
}

install_neovim
```
