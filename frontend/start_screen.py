import customtkinter as ctk
from utils import apply_glow_effect

class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Textos de bienvenida estilo terminal
        self.title_lbl = ctk.CTkLabel(self, text=">_ ROOKIE LINUX DEVELOP", 
                                      font=ctk.CTkFont(family="Consolas", size=50, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.place(relx=0.5, rely=0.35, anchor="center")
        
        self.subtitle_lbl = ctk.CTkLabel(self, text="[ Sistema automatizado ]", 
                                         font=ctk.CTkFont(family="Consolas", size=16),
                                         text_color="#008800")
        self.subtitle_lbl.place(relx=0.5, rely=0.45, anchor="center")
            
        self.btn = ctk.CTkButton(self, text="INICIAR SISTEMA    →", font=ctk.CTkFont(family="Consolas", size=18, weight="bold"), 
                            height=60, width=280, corner_radius=5,
                            command=lambda: controller.show_frame("InfoScreen"),
                            cursor="hand2", 
                            fg_color="transparent", border_width=2, border_color="#008800",
                            hover_color="#001100", text_color="#008800")
        
        apply_glow_effect(self.btn, default_text="INICIAR SISTEMA    →", hover_text="INICIAR SISTEMA       →")
        self.btn.place(relx=0.5, rely=0.65, anchor="center")
