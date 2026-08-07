import customtkinter as ctk
import os
from PIL import Image
from utils import apply_glow_effect, get_project_root

class AboutScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Acerca de Rookie Linux_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))
        
        text_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        text_frame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        
        initial_text = (
            "> Rookie Linux Develop v1.0\n"
            "Desarrollado por: Stack\n\n"
            "¡Gracias por descargar y utilizar Rookie Linux Develop!\n\n"
            "Este proyecto nació con la intención de facilitar el acceso al mundo del\n"
            "desarrollo en Linux, ahorrando horas de configuración tediosa. Esperamos\n"
            "que esta herramienta te sea de gran utilidad y mejore tu productividad."
        )
        
        lbl_initial = ctk.CTkLabel(text_frame, text=initial_text, 
                                   font=ctk.CTkFont(family="Consolas", size=16), 
                                   text_color="#00E676", justify="left")
        lbl_initial.pack(anchor="w", pady=(0, 20))
        
        # Cargar imagen de bienvenida en medio
        self.load_image(text_frame, "welcome.jpg")
        
        license_text = (
            "[+] LICENCIA Y CÓDIGO ABIERTO (MIT License - Simplificada)\n"
            "Rookie Linux Develop es un proyecto de código abierto (Open Source).\n"
            "Eres completamente libre de utilizar, estudiar, copiar, modificar y\n"
            "distribuir este software y su código fuente a voluntad.\n\n"
            "La única condición (y muestra de compañerismo) es que se debe mantener\n"
            "el reconocimiento y otorgar el crédito correspondiente a los creadores\n"
            "originales de este proyecto\n\n"
            "El software se proporciona 'tal cual', sin garantías de ningún tipo."
        )
        
        lbl_license = ctk.CTkLabel(text_frame, text=license_text, 
                                   font=ctk.CTkFont(family="Consolas", size=16), 
                                   text_color="#00E676", justify="left")
        lbl_license.pack(anchor="w", pady=(20, 10))
        
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

    def load_image(self, parent, filename):
        base_path = os.path.join(get_project_root(), "assets")
        img_path = os.path.join(base_path, filename)
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                width, height = img.size
                new_w = 400
                new_h = int(height * (new_w / width))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
                lbl = ctk.CTkLabel(parent, image=ctk_img, text="", cursor="hand2")
                lbl.pack(pady=(0, 15))
                lbl.bind("<Button-1>", lambda e, p=img_path: self.zoom_image(p))
        except Exception as e:
            print(f"Error loading image {filename}: {e}")

    def zoom_image(self, img_path):
        top = ctk.CTkToplevel(self)
        top.title("Visor de Imagen")
        w, h = 1000, 700
        ws, hs = top.winfo_screenwidth(), top.winfo_screenheight()
        x, y = (ws // 2) - (w // 2), (hs // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.configure(fg_color="#0a0a0a")
        top.transient(self.winfo_toplevel())
        top.grab_set()
        
        try:
            img = Image.open(img_path)
            width, height = img.size
            ratio = min(950/width, 650/height)
            new_w, new_h = int(width * ratio), int(height * ratio)
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            lbl = ctk.CTkLabel(top, image=ctk_img, text="", cursor="hand2")
            lbl.pack(expand=True, fill="both", padx=20, pady=20)
            
            lbl.bind("<Button-1>", lambda e: top.destroy())
        except Exception:
            err = ctk.CTkLabel(top, text="Error cargando zoom.", text_color="#FF0000")
            err.pack(expand=True)
            
        top.bind("<Escape>", lambda e: top.destroy())
