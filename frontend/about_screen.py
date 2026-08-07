import customtkinter as ctk
from utils import apply_glow_effect

class AboutScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Acerca de Rookie Linux_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))
        
        # Placeholder para el contenido futuro
        self.info_lbl = ctk.CTkLabel(self, text="[Espacio reservado para licencia y créditos]", text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=16))
        self.info_lbl.grid(row=1, column=0, pady=10)
        
        self.grid_rowconfigure(1, weight=1)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20))
        
        self.btn_action = ctk.CTkButton(btn_frame, text="← Volver", command=lambda: self.controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")
        self.btn_action.pack(side="left", padx=10)
