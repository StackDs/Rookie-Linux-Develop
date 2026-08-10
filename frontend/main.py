import sys
import os
import traceback

# =============================================================================
# LOGGER DE ERRORES FATALES (debe estar antes de cualquier import que pueda fallar)
# Cuando el .exe corra en modo --windowed, cualquier excepción se pierde
# silenciosamente. Este bloque la captura y la escribe en un archivo de log.
# =============================================================================
def _get_log_path():
    """Retorna la ruta del log junto al ejecutable o en el escritorio como fallback."""
    try:
        base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, "rookie_error.log")
    except Exception:
        return os.path.join(os.path.expanduser("~"), "rookie_error.log")

def _fatal_error_handler(exc_type, exc_value, exc_tb):
    """Escribe el traceback completo a un archivo de log y lo muestra en pantalla."""
    log_path = _get_log_path()
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("=== ROOKIE LINUX BUILDER - ERROR FATAL ===\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"Platform: {sys.platform}\n")
            f.write(f"Frozen: {getattr(sys, 'frozen', False)}\n\n")
            f.write(error_msg)
    except Exception:
        pass
        
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showerror("Rookie Linux - Error Fatal", 
                             f"La aplicación ha colapsado. Se ha guardado el log en:\n{log_path}\n\nDetalles del error:\n{error_msg[-600:]}")
        root.destroy()
    except Exception:
        pass

# Redirigir stdout y stderr para evitar crashes en modo --windowed
class _LoggerWriter:
    def __init__(self, is_err=False):
        self.is_err = is_err
        self.log_path = _get_log_path()
        self.encoding = 'utf-8'
    def write(self, message):
        if message:
            try:
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(message)
            except Exception:
                pass
    def flush(self):
        pass
    def isatty(self):
        return False

sys.stdout = _LoggerWriter(is_err=False)
sys.stderr = _LoggerWriter(is_err=True)

sys.excepthook = _fatal_error_handler

import tkinter as tk

def _tk_error_handler(exc_type, exc_value, exc_tb):
    _fatal_error_handler(exc_type, exc_value, exc_tb)

tk.Tk.report_callback_exception = _tk_error_handler
# Importar utils UI sólo después del logger
from custom_messagebox import msg_show_error, msg_ask_yes_no, register_app_window

# Worker hook para flasheo como Admin (debe ir antes de otros imports pesados)
if "--worker-windows" in sys.argv:
    try:
        from screens.installation_tools import flasher_worker_windows
        flasher_worker_windows.main()
    except Exception as e:
        _fatal_error_handler(type(e), e, e.__traceback__)
    sys.exit(0)

if "--worker-linux" in sys.argv:
    try:
        from screens.installation_tools import flasher_worker_linux
        flasher_worker_linux.main()
    except Exception as e:
        _fatal_error_handler(type(e), e, e.__traceback__)
    sys.exit(0)

try:
    import customtkinter as ctk
except ImportError:
    import tkinter.messagebox as messagebox
    import tkinter as tk_temp
    root = tk_temp.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Faltan librerías. Ejecuta 'pip install customtkinter pillow'.")
    sys.exit(1)

from screens.core.start_screen import StartScreen
from screens.core.option_selection_screen import OptionSelectionScreen
from screens.info_manuals.info_screen import InfoScreen
from screens.info_manuals.explanation_screen import ExplanationScreen
from screens.linux_concepts.distro_selection_screen import DistroSelectionScreen
from screens.linux_concepts.distro_info_screen import DistroInfoScreen
from screens.installation_tools.build_progress_screen import BuildProgressScreen
from screens.installation_tools.usb_flash_screen import UsbFlashScreen
from screens.linux_concepts.basic_concepts_screen import BasicConceptsScreen
from screens.info_manuals.bitlocker_screen import BitlockerScreen
from screens.installation_tools.wsl_install_screen import WslInstallScreen
from screens.info_manuals.instructions_screen import InstructionsScreen
from screens.linux_concepts.virtual_machine_screen import VirtualMachineScreen
from screens.linux_concepts.clean_installation_screen import CleanInstallationScreen
from screens.info_manuals.documentation_screen import DocumentationScreen
from screens.info_manuals.about_screen import AboutScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rookie Linux Develop")
        self.geometry("900x600")
        
        # Cargar icono de la ventana (si existe)
        import os
        from utils import get_project_root
        icon_path = os.path.join(get_project_root(), "assets", "Utils", "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(default=icon_path)
            except: pass
            
        self.resizable(False, False)
        self.minsize(900, 600)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Banner superior
        self.banner = ctk.CTkFrame(self, height=40, fg_color="#0a0a0a", corner_radius=0)
        self.banner.grid(row=0, column=0, sticky="ew")
        
        from utils import apply_glow_effect
        self.btn_global_home = ctk.CTkButton(self.banner, text="⌂ Menú Principal", command=lambda: self.request_navigation("OptionSelectionScreen"),
                                      width=120, height=30, fg_color="transparent", text_color="#00FF00", 
                                      hover_color="#003300", font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        self.btn_global_home.pack(side="left", padx=15, pady=5)
        apply_glow_effect(self.btn_global_home, default_text="⌂ Menú Principal", hover_text="⌂ Menú Principal")

        self.btn_start_screen = ctk.CTkButton(self.banner, text="Pantalla de Inicio ⏻", command=lambda: self.request_navigation("StartScreen"),
                                      width=120, height=30, fg_color="transparent", text_color="#00FF00", 
                                      hover_color="#003300", font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        self.btn_start_screen.pack(side="right", padx=15, pady=5)
        apply_glow_effect(self.btn_start_screen, default_text="Pantalla de Inicio ⏻", hover_text="Pantalla de Inicio ⏻")

        # Fondo negro sólido estilo terminal para toda la app
        self.container = ctk.CTkFrame(self, fg_color="#0a0a0a")
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartScreen, OptionSelectionScreen, InfoScreen, ExplanationScreen, DistroSelectionScreen, DistroInfoScreen, BuildProgressScreen, UsbFlashScreen, BasicConceptsScreen, BitlockerScreen, WslInstallScreen, InstructionsScreen, VirtualMachineScreen, CleanInstallationScreen, DocumentationScreen, AboutScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def request_navigation(self, page_name):
        build_screen = self.frames.get("BuildProgressScreen")
        if build_screen and getattr(build_screen, "is_building", False):
            if not msg_ask_yes_no("Proceso activo", "Hay una construcción de ISO en curso.\n¿Estás seguro de que deseas cancelarla y salir?"):
                return
            build_screen.cancel_process(ask_confirm=False)
            
        flash_screen = self.frames.get("UsbFlashScreen")
        if flash_screen and getattr(flash_screen, "is_flashing", False):
            if not msg_ask_yes_no("Proceso activo", "Hay un flasheo de USB en curso.\nSi sales ahora, se cancelará y tu USB podría quedar corrupto.\n¿Estás seguro de que deseas salir?"):
                return
            flash_screen.cancel_flash(ask_confirm=False)
            
        wsl_screen = self.frames.get("WslInstallScreen")
        if wsl_screen and getattr(wsl_screen, "is_installing", False):
            msg_show_error("Proceso activo", "La instalación de WSL está en curso. Por favor espera a que termine.")
            return

        self.show_frame(page_name)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    try:
        app = App()
        register_app_window(app)  # Registrar ventana para centrar diálogos correctamente
        app.mainloop()
    except Exception as e:
        _fatal_error_handler(type(e), e, e.__traceback__)
        sys.exit(1)
