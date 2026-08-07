import customtkinter as ctk
import os
from PIL import Image
from utils import get_project_root
from utils import apply_glow_effect

class BitlockerScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> BitLocker_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))
        
        # main content
        content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=10)
        
        bl_title = ctk.CTkLabel(content_frame, text=">_ ¿Qué es BitLocker?", text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=20, weight="bold"))
        bl_title.pack(anchor="w", pady=(10, 5))
        
        bl_text = (
            "BitLocker es una tecnología de Microsoft que cifra el disco duro para proteger tus archivos. "
            "Si BitLocker está activado, el instalador de Linux no podrá 'ver' ni modificar el espacio libre de tu disco.\n\n"
            "Para poder instalar Linux (especialmente en Dual Boot), es indispensable entrar a Windows, "
            "buscar 'Administrar BitLocker' y desactivarlo antes de iniciar la instalación de Linux. "
            "En muchos casos esto no basta para desactivarlo por completo; en ese caso te recomendamos formatear tu "
            "computador por completo para instalar una versión de Windows sin BitLocker y así no tener problemas más tarde."
        )
        bl_lbl = ctk.CTkLabel(content_frame, text=bl_text, text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=15), wraplength=700, justify="left")
        bl_lbl.pack(anchor="w", pady=(0, 15))
        
        self.load_image(content_frame, "bitlocker.jpg")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20))
        
        self.btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: self.controller.show_frame("CleanInstallationScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_volver, default_text="←    Volver", hover_text="←       Volver")
        self.btn_volver.pack(side="left", padx=15)
        
    def load_image(self, parent, filename):
        base_path = os.path.join(get_project_root(), "assets", "Utils")
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
