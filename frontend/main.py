import tkinter as tk
from custom_messagebox import msg_show_error
import sys

# Worker hook para flasheo como Admin
if "--worker" in sys.argv:
    try:
        import flasher_worker
        flasher_worker.main()
    except Exception as e:
        open('C:/Users/Stack/Desktop/error_main.txt', 'w').write(str(e))

    flasher_worker.main()
    import sys as _sys
    _sys.exit(0)

try:
    import customtkinter as ctk
except ImportError:
    msg_show_error("Error", "Faltan librerías. Ejecuta 'pip install customtkinter pillow'.")
    sys.exit(1)

from start_screen import StartScreen
from option_selection_screen import OptionSelectionScreen
from info_screen import InfoScreen
from explanation_screen import ExplanationScreen
from distro_selection_screen import DistroSelectionScreen
from distro_info_screen import DistroInfoScreen
from build_progress_screen import BuildProgressScreen
from usb_flash_screen import UsbFlashScreen
from basic_concepts_screen import BasicConceptsScreen
from bitlocker_screen import BitlockerScreen
from wsl_install_screen import WslInstallScreen
from instructions_screen import InstructionsScreen
from virtual_machine_screen import VirtualMachineScreen
from clean_installation_screen import CleanInstallationScreen
from documentation_screen import DocumentationScreen
from about_screen import AboutScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rookie Linux Develop")
        self.geometry("900x600")
        self.resizable(False, False)
        self.minsize(900, 600)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Banner superior
        self.banner = ctk.CTkFrame(self, height=40, fg_color="#0a0a0a", corner_radius=0)
        self.banner.grid(row=0, column=0, sticky="ew")
        
        from utils import apply_glow_effect
        self.btn_global_home = ctk.CTkButton(self.banner, text="⌂ Menú Principal", command=lambda: self.show_frame("OptionSelectionScreen"),
                                      width=120, height=30, fg_color="transparent", text_color="#00FF00", 
                                      hover_color="#003300", font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        self.btn_global_home.pack(side="left", padx=15, pady=5)
        apply_glow_effect(self.btn_global_home, default_text="⌂ Menú Principal", hover_text="⌂ Menú Principal")

        self.btn_start_screen = ctk.CTkButton(self.banner, text="Pantalla de Inicio ⏻", command=lambda: self.show_frame("StartScreen"),
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

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    app = App()
    app.mainloop()
