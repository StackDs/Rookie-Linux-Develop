import customtkinter as ctk
from utils import apply_glow_effect

class OptionSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = ctk.CTkLabel(self, text="> Selecciona una opción_", 
                                      font=ctk.CTkFont(family="Consolas", size=40, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.grid(row=1, column=0, pady=(0, 40))
        
        # Option A: Informacion del programa
        self.btn_info = ctk.CTkButton(self, text="Información e instrucciones de uso", 
                                      command=lambda: controller.show_frame("InfoScreen"),
                                      height=50, width=350, corner_radius=5,
                                      font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                                      cursor="hand2", fg_color="transparent", 
                                      border_width=2, border_color="#008800",
                                      hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_info, default_text="Información e instrucciones de uso", hover_text="Información e instrucciones de uso")
        self.btn_info.grid(row=2, column=0, pady=(0, 15))

        # Option B: Sobre Linux
        self.btn_concepts = ctk.CTkButton(self, text="Sobre Linux", 
                                          command=lambda: controller.show_frame("ExplanationScreen"),
                                          height=50, width=350, corner_radius=5,
                                          font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                                          cursor="hand2", fg_color="transparent", 
                                          border_width=2, border_color="#008800",
                                          hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_concepts, default_text="Sobre Linux", hover_text="Sobre Linux")
        self.btn_concepts.grid(row=3, column=0, pady=(0, 15))

        # Option C: Crear imagen
        self.btn_create = ctk.CTkButton(self, text="Crear imagen personalizada", 
                                        command=lambda: controller.show_frame("DistroSelectionScreen"),
                                        height=50, width=350, corner_radius=5,
                                        font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                                        cursor="hand2", fg_color="transparent", 
                                        border_width=2, border_color="#008800",
                                        hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_create, default_text="Crear imagen personalizada", hover_text="Crear imagen personalizada")
        self.btn_create.grid(row=4, column=0, pady=(0, 15))

        # Option D: Montar imagen
        self.btn_mount = ctk.CTkButton(self, text="Montar imagen (Requiere un USB)", 
                                       command=lambda: controller.show_frame("UsbFlashScreen"),
                                       height=50, width=350, corner_radius=5,
                                       font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                                       cursor="hand2", fg_color="transparent", 
                                       border_width=2, border_color="#008800",
                                       hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_mount, default_text="Montar imagen (Requiere un USB)", hover_text="Montar imagen (Requiere un USB)")
        self.btn_mount.grid(row=5, column=0, pady=(0, 15))

        # Option E: Instalar WSL
        self.btn_wsl = ctk.CTkButton(self, text="Instalar WSL (Necesario para el desarrollo)", 
                                       command=lambda: controller.show_frame("WslInstallScreen"),
                                       height=50, width=350, corner_radius=5,
                                       font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                                       cursor="hand2", fg_color="transparent", 
                                       border_width=2, border_color="#008800",
                                       hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_wsl, default_text="Instalar WSL (Necesario para el desarrollo)", hover_text="Instalar WSL (Necesario para el desarrollo)")
        self.btn_wsl.grid(row=6, column=0, pady=(0, 15))
