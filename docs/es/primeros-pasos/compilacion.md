# Compilación y Distribución

## Visión general

El proyecto usa **PyInstaller** para generar ejecutables nativos de un solo archivo. Los scripts de compilación están en la carpeta `compile/` y generan el resultado final en la carpeta `app release/` (ignorada por git).

---

## Scripts disponibles

| Script | Plataforma | Ejecutar en |
|---|---|---|
| `compile/build_linux.py` | Linux (nativo) | Linux |
| `compile/build_windows.py` | Windows (x64) | Linux con Docker o directamente en Windows |

---

## Compilar para Linux

### Requisitos
- Python 3.10+
- pip

### Comando

```bash
# Desde la raíz del proyecto:
python3 compile/build_linux.py
```

El script automáticamente:
1. Instala `pyinstaller`, `customtkinter` y `pillow` si no están presentes.
2. Ejecuta PyInstaller sobre `frontend/main.py` con las flags correctas.
3. Mueve el ejecutable a una carpeta temporal `Rookie Linux Develop Linux/`.
4. Copia las carpetas necesarias: `assets/`, `builder/`, `templates/`, `configs/`, `scripts/`.
5. Crea las carpetas vacías necesarias: `downloads/iso/`, `output/`, `logs/`.
6. Empaqueta todo en `app release/Rookie Linux Develop Linux.rar` (o `.zip` si `rar` no está instalado).
7. Limpia los archivos temporales de compilación.

### Resultado

```
app release/
└── Rookie Linux Develop Linux.rar
    └── Rookie Linux Develop Linux/
        ├── Rookie-Linux-Builder    ← Ejecutable
        ├── assets/
        ├── builder/
        ├── scripts/
        ├── configs/
        ├── downloads/iso/          ← Vacía (se llena en uso)
        ├── output/                 ← Vacía (se llena en uso)
        └── logs/                   ← Vacía (se llena en uso)
```

---

## Compilar para Windows

### Requisitos
- Python 3.10+ **en el mismo Windows**

### Comando (ejecutar en Windows)

```powershell
python compile\build_windows.py
```

El flujo es idéntico al de Linux. El resultado es:

```
app release/
└── Rookie Linux Develop Win x64.rar
    └── Rookie Linux Develop Win x64/
        ├── Rookie-Linux-Builder.exe  ← Ejecutable
        ├── assets/
        ├── builder/
        ├── scripts/
        ├── configs/
        ├── downloads/iso/
        ├── output/
        └── logs/
```

---

## Flags de PyInstaller importantes

Ambos scripts usan las siguientes flags críticas:

```bash
pyinstaller \
  --noconfirm \
  --windowed \                          # Sin consola de terminal
  --name "Rookie-Linux-Builder" \
  --hidden-import PIL._tkinter_finder \ # Necesario para PIL en entornos empaquetados
  --collect-all customtkinter \         # Incluye todos los assets de CustomTkinter
  frontend/main.py
```

> ⚠️ **`--hidden-import PIL._tkinter_finder`** es obligatorio. Sin este flag, las imágenes no se cargan en el ejecutable empaquetado (error silencioso en Linux, crash en Windows).

> ⚠️ **`--collect-all customtkinter`** es obligatorio. CustomTkinter tiene archivos de tema JSON y assets que PyInstaller no detecta automáticamente.

---

## Agregar nuevas dependencias

Si añades una nueva librería Python al proyecto, debes incluirla en el script de compilación correspondiente. Agrega una línea al bloque de instalación de dependencias:

```python
subprocess.run([sys.executable, "-m", "pip", "install", "nueva-libreria", ...], check=False)
```

Y si PyInstaller no la detecta automáticamente, agrega el hidden import:

```python
"--hidden-import", "nueva_libreria.modulo_interno",
```

---

## Carpetas temporales de compilación

PyInstaller genera carpetas `build/` y `dist/` durante la compilación. Los scripts de `compile/` las limpian automáticamente al finalizar. Si el script falla a mitad de proceso, puedes eliminarlas manualmente:

```bash
rm -rf build/ dist/ *.spec
```
