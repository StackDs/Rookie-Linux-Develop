import customtkinter as ctk
from utils import apply_glow_effect

class WslInstallScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = ctk.CTkLabel(self, text="> Instalación de WSL_", 
                                      font=ctk.CTkFont(family="Consolas", size=40, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.grid(row=0, column=0, pady=(20, 10))
        
        self.desc_lbl = ctk.CTkLabel(self, text="Selecciona el modo de instalación de WSL que deseas realizar:", 
                                     font=ctk.CTkFont(family="Consolas", size=18), text_color="#00E676", justify="center")
        self.desc_lbl.grid(row=1, column=0, pady=(0, 20))
        
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=2, column=0, pady=(10, 20))
        
        # Option 1: App Mode
        self.btn_app_mode = ctk.CTkButton(options_frame, text="1. Instalar WSL para usar la app", 
                                          command=lambda: self.controller.show_frame("WslAppInstallScreen"),
                                          height=50, width=400, corner_radius=5,
                                          font=ctk.CTkFont(family="Consolas", size=16, weight="bold"), cursor="hand2",
                                          fg_color="#004400", border_width=2, border_color="#00FF00",
                                          hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_app_mode, default_text="1. Instalar WSL para usar la app", hover_text="1. Instalar WSL para usar la app")
        self.btn_app_mode.pack(pady=(0, 10))
        
        self.desc_app = ctk.CTkLabel(options_frame, text="Instala el subsistema y una distro auxiliar\npara poder compilar imágenes de Rookie Linux.",
                                     font=ctk.CTkFont(family="Consolas", size=14), text_color="#008800")
        self.desc_app.pack(pady=(0, 25))
        
        # Option 2: Main Mode
        self.btn_main_mode = ctk.CTkButton(options_frame, text="2. Instalar WSL como main en Windows", 
                                          command=lambda: self.controller.show_frame("WslMainInstallScreen"),
                                          height=50, width=400, corner_radius=5,
                                          font=ctk.CTkFont(family="Consolas", size=16, weight="bold"), cursor="hand2",
                                          fg_color="#004400", border_width=2, border_color="#00FF00",
                                          hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_main_mode, default_text="2. Instalar WSL como main en Windows", hover_text="2. Instalar WSL como main en Windows")
        self.btn_main_mode.pack(pady=(0, 10))
        
        self.desc_main = ctk.CTkLabel(options_frame, text="Instala una distro completa para usarla\ncomo tu sistema principal en Windows.",
                                     font=ctk.CTkFont(family="Consolas", size=14), text_color="#008800")
        self.desc_main.pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(10, 20), sticky="s")
        
        self.btn_home = ctk.CTkButton(btn_frame, text="← Menú Principal", command=lambda: self.controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=180, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_home, default_text="← Menú Principal", hover_text="← Menú Principal")
        self.btn_home.grid(row=0, column=0, padx=10)
