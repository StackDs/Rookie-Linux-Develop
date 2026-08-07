# Entorno de Desarrollo

## Requisitos previos

| Requisito | Versión mínima | Instalación |
|---|---|---|
| Python | 3.10+ | `sudo apt install python3` |
| pip | Incluido con Python | — |
| Git | Cualquiera | `sudo apt install git` |
| Tkinter | Incluido con Python | `sudo apt install python3-tk` |

> **En Windows**: Se requiere Python 3.10+ desde [python.org](https://www.python.org/downloads/) y WSL instalado para la parte de construcción de ISOs.

---

## Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Rookie-Linux-Develop.git
cd Rookie-Linux-Develop
```

---

## Instalar dependencias Python

```bash
pip install customtkinter pillow
```

O si usas un entorno virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install customtkinter pillow
```

---

## Ejecutar la aplicación

La aplicación debe lanzarse desde la **raíz del proyecto** ya que `utils.get_project_root()` determina la ruta raíz usando la posición relativa de `main.py`:

```bash
# Desde la raíz del proyecto:
python3 frontend/main.py
```

> ⚠️ **No ejecutes desde dentro de `frontend/`**. Las rutas a `assets/`, `builder/`, y `scripts/` se calculan relativas a la raíz del proyecto.

---

## Estructura que necesitas conocer

```
Rookie-Linux-Develop/
├── frontend/
│   ├── main.py              ← Punto de entrada de la GUI
│   ├── utils.py             ← Utilidades (rutas, efectos visuales)
│   ├── custom_messagebox.py ← Sistema de diálogos modales
│   └── screens/             ← Todas las pantallas de la aplicación
├── assets/                  ← Imágenes, wallpaper, icono
├── builder/                 ← Scripts de descarga y construcción
├── scripts/                 ← Scripts de instalación post-arranque
├── configs/                 ← Configuración global (opcional)
├── downloads/iso/           ← ISOs descargadas (ignorado por git)
├── output/                  ← ISOs generadas (ignorado por git)
└── logs/                    ← Registros (ignorado por git)
```

---

## Verificar que todo funciona

Al lanzar `frontend/main.py` debería aparecer la ventana de la aplicación con:
- Fondo negro estilo terminal
- Banner superior con "⌂ Menú Principal" y "Pantalla de Inicio ⏻"
- Pantalla de bienvenida con animación de texto

Si aparece un error de importación, verifica:

```bash
python3 -c "import customtkinter; print('OK')"
python3 -c "from PIL import Image; print('OK')"
python3 -c "import tkinter; print('OK')"
```

---

## Problemas comunes

### `No module named 'tkinter'`
```bash
sudo apt install python3-tk
```

### Imágenes que no se muestran
Verifica que existan en `assets/`:
```bash
ls assets/
# Debe haber: welcome.jpg, dualboot.jpg, bitlocker.jpg, maquinaVirtual.jpg, onlyLinux.jpg
```

### La ventana aparece en esquina o sin contenido (Linux)
Es un problema de mapeo del gestor de ventanas. El mecanismo `withdraw/deiconify` ya lo mitiga; si persiste, prueba ejecutar con otro gestor de ventanas o actualiza CustomTkinter:
```bash
pip install --upgrade customtkinter
```

---

## Agregar una pantalla nueva (resumen rápido)

1. Crea `frontend/screens/categoria/mi_pantalla.py` con una clase que herede de `ctk.CTkFrame`.
2. En `frontend/main.py`, importa la clase y agrégala al bucle de inicialización de frames.
3. Navega hacia ella con `self.controller.show_frame("MiPantalla")`.

Consulta la [guía completa de pantallas](../reference/estructura-de-pantallas.md) para más detalles.
