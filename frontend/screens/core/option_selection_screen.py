import customtkinter as ctk
from utils import apply_glow_effect

class OptionSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        for i in range(1, 9):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = ctk.CTkLabel(self, text="> Selecciona una opción_", 
                                      font=ctk.CTkFont(family="Consolas", size=40, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.grid(row=0, column=0, pady=(20, 10))
        
        import sys
        
        self.create_option(1, "Manual de uso", lambda: controller.show_frame("InfoScreen"))
        self.create_option(2, "Sobre Linux", lambda: controller.show_frame("ExplanationScreen"))
        self.create_option(3, "Crear imagen personalizada", lambda: controller.show_frame("DistroSelectionScreen"))
        self.create_option(4, "Montar imagen (Requiere USB)", lambda: controller.show_frame("UsbFlashScreen"))
        
        if sys.platform == "win32":
            self.create_option(5, "Instalar WSL (Necesario)", lambda: controller.show_frame("WslInstallScreen"))
        else:
            self.create_option(5, "Instalar WSL (Necesario)", self.show_wsl_not_needed, dimmed=True)
            
        self.create_option(6, "Documentación oficial", lambda: controller.show_frame("DocumentationScreen"))
        self.create_option(7, "Acerca de Rookie Linux", lambda: controller.show_frame("AboutScreen"))

    def show_wsl_not_needed(self):
        from custom_messagebox import msg_show_info
        msg_show_info(
            "Información del Sistema", 
            "WSL (Windows Subsystem for Linux) es una herramienta exclusiva de Microsoft para ejecutar Linux dentro de Windows.\n\nComo ya te encuentras ejecutando este programa de forma nativa en Linux, no necesitas instalar nada adicional. ¡Puedes continuar directamente con las demás opciones!",
            width=650, height=350
        )

    def create_option(self, row, text, command, dimmed=False):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=row, column=0, pady=(0, 8))
        
        arrow = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Consolas", size=24, weight="bold"), text_color="#00FF00", width=30)
        arrow.pack(side="left")
        
        btn = ctk.CTkButton(frame, text=text, command=command,
                            height=40, width=350, corner_radius=5,
                            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                            cursor="hand2", fg_color="transparent", 
                            border_width=2, border_color="#008800",
                            hover_color="#001100", text_color="#008800")
        btn.pack(side="left")
        
        dummy = ctk.CTkLabel(frame, text="", width=30)
        dummy.pack(side="left")
        
        if command is None:
            btn.configure(state="disabled", fg_color="transparent", text_color="#003300", border_color="#003300")
            return btn
            
        if dimmed:
            btn.configure(text_color="#003300", border_color="#003300")
        else:
            apply_glow_effect(btn, default_text=text, hover_text=text)
            
        def on_enter(e):
            if not dimmed:
                arrow.configure(text=">")
        def on_leave(e):
            if not dimmed:
                arrow.configure(text="")
            
        btn.bind("<Enter>", on_enter, add="+")
        btn.bind("<Leave>", on_leave, add="+")
        
        return btn
