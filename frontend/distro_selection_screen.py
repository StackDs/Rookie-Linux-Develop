import customtkinter as ctk
import os
from PIL import Image
from utils import apply_glow_effect, get_project_root
from custom_messagebox import msg_show_error

class DistroSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
            
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="> Selecciona una Distribución_", text_color="#00FF00",
                             font=ctk.CTkFont(family="Consolas", size=32, weight="bold"))
        title.grid(row=0, column=0, pady=(40, 20))
        
        self.distro_var = ctk.StringVar(value="Ubuntu")
        
        distros = [
            ("Ubuntu", "ubuntu-logo.png"),
            ("Fedora", "fedora-logo.png"),
            ("Pop!_OS", "PopOS-logo.png"),
            ("Linux Mint", "Linux-Mint-Logo.png")
        ]
        
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, padx=20, pady=20)
        
        self.images = []
        
        for idx, (name, img_file) in enumerate(distros):
            img_path = os.path.join(get_project_root(), "assets", img_file)
            
            card = ctk.CTkFrame(cards_frame, fg_color="transparent", border_width=0)
            card.grid(row=0, column=idx, padx=15, pady=10)
            
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    if img.mode != 'RGBA' and img.mode != 'RGB':
                        img = img.convert('RGBA')
                    
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                    self.images.append(ctk_img)
                    
                    img_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    img_lbl.pack(pady=(20, 10), padx=20)
                except Exception as e:
                    lbl = ctk.CTkLabel(card, text="[Imagen]", text_color="#00FF00", font=ctk.CTkFont(family="Consolas"), width=120, height=120)
                    lbl.pack(pady=(20, 10), padx=20)
            else:
                lbl = ctk.CTkLabel(card, text="[IMG NULL]", text_color="#00FF00", font=ctk.CTkFont(family="Consolas"), width=120, height=120)
                lbl.pack(pady=(20, 10), padx=20)
                
            rb = ctk.CTkRadioButton(card, text=name, variable=self.distro_var, value=name,
                                    font=ctk.CTkFont(family="Consolas", size=18, weight="bold"), 
                                    text_color="#00FF00", fg_color="#00FF00", 
                                    cursor="hand2", bg_color="transparent")
            rb.pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="⌂ Volver a Opciones", command=lambda: controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_volver, default_text="⌂ Volver a Opciones", hover_text="⌂ Volver a Opciones")
        btn_volver.pack(side="left", padx=15)
        
        btn_siguiente = ctk.CTkButton(btn_frame, text="Siguiente    →", command=self.check_and_proceed,
                                      height=45, width=170, corner_radius=5,
                                      font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                      fg_color="transparent", border_width=2, border_color="#008800",
                                      hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_siguiente, default_text="Siguiente    →", hover_text="Siguiente       →")
        btn_siguiente.pack(side="left", padx=15)
        
    def check_and_proceed(self):
        if self.distro_var.get() == "Fedora":
            msg_show_error("En desarrollo", "Esta opción actualmente se encuentra en desarrollo.")
        else:
            self.controller.show_frame("DistroInfoScreen")
