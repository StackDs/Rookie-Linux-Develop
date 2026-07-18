#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"

echo "=========================================="
echo "Instalando Comandos Personalizados"
echo "=========================================="

# Crear el script doc-stack en el path global
cat << 'EOF' > /usr/local/bin/doc-stack
#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source "$SCRIPT_DIR/utils.sh"
echo "> ./stack-doctor"
echo ""
echo "Initializing diagnostics..."
sleep 0.5
echo "Loading modules..."
sleep 0.5
echo "Please wait..."
sleep 1
echo ""
echo "Running diagnostics..."
echo ""
sleep 0.5
echo -e "CPU ............... \033[0;32mOK\033[0m"
sleep 0.3
echo -e "RAM ............... \033[0;32mOK\033[0m"
sleep 0.3
echo -e "Disk .............. \033[0;32mOK\033[0m"
sleep 0.3
echo -e "GPU ............... \033[0;32mOK\033[0m"
sleep 0.3
echo -e "Network ........... \033[0;32mOK\033[0m"
echo ""
sleep 1
echo "Checking neural activity..."
sleep 1
echo "..."
sleep 2
echo ""
echo -e "Brain ............. \033[0;31mNot detected\033[0m"
echo ""
sleep 1.5
echo "Generating diagnosis..."
sleep 0.8
echo "Analyzing results..."
sleep 0.8
echo "Consulting AI model..."
sleep 2
echo ""
echo "Diagnosis:"
echo "Yep, you're cooked bro."
EOF

# Darle permisos de ejecucion para todos los usuarios
chmod +x /usr/local/bin/doc-stack

echo "[OK] Comando 'doc-stack' instalado exitosamente."

