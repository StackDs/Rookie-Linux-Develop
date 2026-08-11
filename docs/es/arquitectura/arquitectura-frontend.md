# Arquitectura del Frontend

## Visión general

El frontend está construido en **Python 3** usando la librería **CustomTkinter** (CTk), que extiende Tkinter con widgets modernos y soporte para modo oscuro. La estructura sigue un patrón de **pantallas apiladas** donde todas las vistas existen en memoria y se alternan elevando la pantalla activa al frente con `tkraise()`.

---

## Punto de entrada: `frontend/main.py`

El archivo `main.py` contiene la clase principal `App` que hereda de `ctk.CTk` (la ventana raíz). Sus responsabilidades son:

1. **Detección de modo worker**: Si se lanza con `--worker-windows` o `--worker-linux`, ejecuta el flasheador de USB como proceso elevado (administrador) y sale inmediatamente. Esto evita tener que empaquetar un ejecutable separado solo para el flasheo.

2. **Inicialización de pantallas**: Instancia todas las clases de pantalla en un bucle, las coloca en un grid apilado y guarda referencias en `self.frames = {}`.

3. **Anti-flickering en Linux**: La ventana principal se oculta con `self.withdraw()` mientras se crean todas las pantallas, y se muestra con `self.deiconify()` solo cuando todo está listo.

4. **Navegación global**: Expone el método `show_frame(page_name)` que toda pantalla puede llamar. Si la pantalla de destino tiene un método `on_show()`, se invoca automáticamente para resetear estado.

5. **Banner superior**: Un frame persistente con botones de navegación rápida a "Menú Principal" y "Pantalla de Inicio".

### Sistema de Captura de Errores Fatales (Error Logger)
Para evitar *crashes* silenciosos (especialmente al ejecutar el binario compilado de Windows con `--windowed`, donde no hay consola), `main.py` implementa un sistema global de logging antes de cualquier importación pesada:
- Redirige `sys.stdout` y `sys.stderr` mediante una clase proxy (`_LoggerWriter`) a un archivo local `rookie_error.log`.
- Sobrescribe `sys.excepthook` y el manejador global de Tkinter (`tk.Tk.report_callback_exception`) con la función `_fatal_error_handler`, la cual guarda el *traceback* completo en disco y dispara un messagebox crítico (con CustomTkinter/Tkinter) antes de abortar el proceso.

---

## Patrón de comunicación entre pantallas

Todas las pantallas reciben dos argumentos en su constructor:
- `parent`: el contenedor CTk donde se montan.
- `controller`: la instancia de `App`, que actúa como controlador centralizado.

Cualquier pantalla puede navegar a otra así:
```python
self.controller.show_frame("NombreDeLaPantalla")
```

Para leer datos de otra pantalla (por ejemplo, la distro seleccionada):
```python
distro = self.controller.frames["DistroSelectionScreen"].distro_var.get()
```

---

## Mapa de pantallas

```
App (main.py)
│
├── [Banner global]
│   ├── ⌂ Menú Principal  → OptionSelectionScreen
│   └── ⏻ Pantalla Inicio → StartScreen
│
└── [Contenedor de pantallas apiladas]
    │
    ├── core/
    │   ├── StartScreen               Pantalla de bienvenida con animación de tipeo
    │   └── OptionSelectionScreen     Menú principal con las 7 opciones
    │
    ├── info_manuals/
    │   ├── InfoScreen                Manual de uso (lista de herramientas instaladas)
    │   ├── ExplanationScreen         Hub de "Sobre Linux" con 3 sub-opciones
    │   ├── InstructionsScreen        Instrucciones de uso del USB/instalación
    │   ├── DocumentationScreen       Links a documentación oficial (tabview)
    │   ├── AboutScreen               Acerca de la app (imagen, info del autor)
    │   └── BitlockerScreen           Explicación y guía para desactivar BitLocker
    │
    ├── linux_concepts/
    │   ├── BasicConceptsScreen       Qué es el Dual Boot
    │   ├── VirtualMachineScreen      Qué es una Máquina Virtual
    │   ├── CleanInstallationScreen   Qué es una Instalación Limpia
    │   ├── DistroSelectionScreen     Selector de distribución (radio buttons)
    │   └── DistroInfoScreen          Info + capturas de pantalla de cada distro
    │
    └── installation_tools/
        ├── BuildProgressScreen       Progreso de descarga + construcción de ISO
        ├── UsbFlashScreen            Selector de USB + progreso de flasheo
        └── WslInstallScreen          Instalador de WSL (solo Windows)
```

---

## Ciclo de vida de una pantalla

```
1. __init__(parent, controller)
   └── Se crea una vez al arrancar la app.
       Construye todos los widgets del layout.

2. on_show()   [Opcional]
   └── Se llama cada vez que la pantalla se hace visible.
       Úsalo para resetear estado, limpiar campos o leer
       datos frescos de otras pantallas.

3. [Interacción del usuario]
   └── Eventos de botones, combos, etc.
       Pueden lanzar threads (para no bloquear la GUI).

4. Navegación
   └── self.controller.show_frame("OtraPantalla")
```

---

## Componentes reutilizables

### `custom_messagebox.py`
Sistema de diálogos modales con estética consistente. Expone:
- `msg_show_info(title, message)` — Información general
- `msg_show_error(title, message)` — Error (rojo)
- `msg_show_warning(title, message)` — Advertencia (naranja)
- `msg_ask_yes_no(title, message)` → `bool` — Diálogo de confirmación

Los modales están centrados en pantalla y son multiplataforma (Linux + Windows).

### `utils.py` (frontend)
- `apply_glow_effect(btn, default_text, hover_text)` — Aplica el efecto de "brillo" al pasar el mouse sobre botones.
- `get_project_root()` — Devuelve la ruta raíz del proyecto, compatible con ejecución normal y empaquetada (PyInstaller).

### `ProgressBarManager` (en `BuildProgressScreen`)
Abstracción sobre `ctk.CTkProgressBar` que permite cambiar entre modo indeterminado (animación de pulso) y determinado (barra de progreso con porcentaje) sin recrear el widget.

---

## Gestión de imágenes (PIL/CTkImage)

Para mostrar imágenes en las pantallas se usa `CTkImage` de CustomTkinter (wrapper sobre Pillow). 

**Regla crítica — Anti-Garbage Collection:**
Python puede liberar de memoria una `CTkImage` si no existe ninguna referencia "viva" apuntando a ella. Para evitar que las imágenes desaparezcan, siempre se almacena una referencia en el widget o en el frame que la contiene:

```python
ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
lbl = ctk.CTkLabel(parent, image=ctk_img, text="")
lbl.image_ref = ctk_img  # ← Referencia explícita para evitar GC
```

Para los visores de zoom (ventanas emergentes `CTkToplevel`):
```python
top.zoomed_img = ctk_img  # ← Se adjunta al objeto de la ventana
```
