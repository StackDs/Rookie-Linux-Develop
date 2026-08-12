import customtkinter as ctk
from utils import apply_glow_effect

class WslMainInstallScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = ctk.CTkLabel(self, text="> Instalador WSL (Modo Main)_", 
                                      font=ctk.CTkFont(family="Consolas", size=38, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.grid(row=0, column=0, pady=(20, 10))
        
        self.desc_lbl = ctk.CTkLabel(self, text="Esta función te permitirá instalar WSL como tu sistema principal.\n\n(En desarrollo)", 
                                     font=ctk.CTkFont(family="Consolas", size=18), text_color="#00E676", justify="center")
        self.desc_lbl.grid(row=1, column=0, pady=(40, 20))
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20), sticky="s")
        
        self.btn_home = ctk.CTkButton(btn_frame, text="← Volver", command=self.go_home,
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_home, default_text="← Volver", hover_text="← Volver")
        self.btn_home.grid(row=0, column=0, padx=10)
        
    def go_home(self):
        self.controller.show_frame("WslInstallScreen")
