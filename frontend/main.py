import tkinter as tk
from custom_messagebox import msg_show_error, msg_ask_yes_no, register_app_window
import sys

# Worker hook para flasheo como Admin
if "--worker-windows" in sys.argv:
    try:
        from screens.installation_tools import flasher_worker_windows
        flasher_worker_windows.main()
    except Exception as e:
        pass
    sys.exit(0)

if "--worker-linux" in sys.argv:
    try:
        from screens.installation_tools import flasher_worker_linux
        flasher_worker_linux.main()
    except Exception as e:
        pass
    sys.exit(0)

try:
    import customtkinter as ctk
except ImportError:
    msg_show_error("Error", "Faltan librerías. Ejecuta 'pip install customtkinter pillow'.")
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
                self.iconbitmap(icon_path)
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

        self.withdraw() # Ocultar ventana durante la carga inicial para evitar flickering
        
        self.frames = {}
        for F in (StartScreen, OptionSelectionScreen, InfoScreen, ExplanationScreen, DistroSelectionScreen, DistroInfoScreen, BuildProgressScreen, UsbFlashScreen, BasicConceptsScreen, BitlockerScreen, WslInstallScreen, InstructionsScreen, VirtualMachineScreen, CleanInstallationScreen, DocumentationScreen, AboutScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")
        self.update_idletasks() # Forzar render
        self.deiconify() # Mostrar ventana ya lista

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
    app = App()
    register_app_window(app)  # Registrar ventana para centrar diálogos correctamente
    app.mainloop()
