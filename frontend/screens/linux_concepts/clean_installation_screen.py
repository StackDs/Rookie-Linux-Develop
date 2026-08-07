import customtkinter as ctk
import os
from PIL import Image
from utils import get_project_root
from utils import apply_glow_effect

class CleanInstallationScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Instalación Limpia_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))
        
        # main content
        content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=10)
        
        ci_title = ctk.CTkLabel(content_frame, text=">_ ¿Qué es una Instalación Limpia?", text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=20, weight="bold"))
        ci_title.pack(anchor="w", pady=(10, 5))
        
        ci_text = (
            "Una 'Instalación Limpia' consiste en formatear completamente tu disco duro o unidad de almacenamiento "
            "y usar Linux como el único sistema operativo de tu computadora, eliminando Windows por completo.\n\n"
            "Esta opción ofrece el mejor rendimiento posible, ya que Linux tendrá acceso a todos los recursos del hardware "
            "de forma exclusiva. Es ideal si ya te sientes cómodo con Linux, si quieres revivir una PC antigua, o si estás "
            "completamente seguro de que no necesitas usar aplicaciones exclusivas de Windows."
        )
        ci_lbl = ctk.CTkLabel(content_frame, text=ci_text, text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=15), wraplength=700, justify="left")
        ci_lbl.pack(anchor="w", pady=(0, 15))
        
        self.load_image(content_frame, "onlyLinux.jpg")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20))
        
        self.btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: self.controller.show_frame("VirtualMachineScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_volver, default_text="←    Volver", hover_text="←       Volver")
        self.btn_volver.pack(side="left", padx=15)
        
        self.btn_siguiente = ctk.CTkButton(btn_frame, text="Siguiente    →", command=lambda: self.controller.show_frame("BitlockerScreen"),
                                       height=45, width=220, corner_radius=5,
                                       font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                       fg_color="transparent", border_width=2, border_color="#008800",
                                       hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_siguiente, default_text="Siguiente    →", hover_text="Siguiente       →")
        self.btn_siguiente.pack(side="left", padx=15)
        
    def load_image(self, parent, filename):
        base_path = os.path.join(get_project_root(), "assets")
        img_path = os.path.join(base_path, filename)
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                width, height = img.size
                new_w = 450
                new_h = int(height * (new_w / width))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
                lbl = ctk.CTkLabel(parent, image=ctk_img, text="")
                lbl.image_ref = ctk_img
                lbl.pack(pady=10)
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
