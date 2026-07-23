import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

try:
    import customtkinter as ctk
    from PIL import Image
except ImportError:
    messagebox.showerror("Error", "Faltan librerías. Ejecuta 'pip install customtkinter pillow'.")
    sys.exit(1)

# Configurar el tema oscuro y colores de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rookie Linux Developer")
        self.geometry("900x600")
        
        # Configurar el grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (WelcomeScreen, DistroSelectionScreen):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name):
        '''Muestra la pantalla solicitada'''
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Centrar contenido
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(self, text="¡Bienvenido a Rookie Linux!", 
                             font=ctk.CTkFont(family="Roboto", size=42, weight="bold"))
        title.grid(row=1, column=0, pady=(0, 30))
        
        # Descripción
        desc = ctk.CTkLabel(self, text="Esta herramienta te ayudará a configurar y desarrollar\ntu entorno Linux de manera rápida y elegante.",
                            font=ctk.CTkFont(family="Roboto", size=20), text_color="gray70")
        desc.grid(row=2, column=0, pady=(0, 60))
        
        # Botón
        btn = ctk.CTkButton(self, text="Comenzar", font=ctk.CTkFont(size=18, weight="bold"), 
                            height=55, width=220, corner_radius=10,
                            command=lambda: controller.show_frame("DistroSelectionScreen"),
                            cursor="hand2")
        btn.grid(row=3, column=0)

class DistroSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(self, text="Selecciona una Distribución", font=ctk.CTkFont(family="Roboto", size=32, weight="bold"))
        title.grid(row=0, column=0, pady=(40, 20))
        
        # Variable para la selección
        self.distro_var = ctk.StringVar(value="Ubuntu")
        
        distros = [
            ("Ubuntu", "ubuntu-logo.png"),
            ("Fedora", "fedora-logo.jpg"),
            ("Pop!_OS", "PopOS-logo.png"),
            ("Linux Mint", "Linux-Mint-Logo.png")
        ]
        
        # Frame para las tarjetas de las distribuciones
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, padx=20, pady=20)
        
        self.images = [] # mantener referencia
        
        for idx, (name, img_file) in enumerate(distros):
            img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", img_file)
            
            # Crear una tarjeta (frame con bordes redondeados) para cada distro
            card = ctk.CTkFrame(cards_frame, corner_radius=15, fg_color="gray15")
            card.grid(row=0, column=idx, padx=15, pady=10)
            
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    if img.mode != 'RGBA' and img.mode != 'RGB':
                        img = img.convert('RGBA')
                    
                    # ctk.CTkImage maneja automáticamente el escalado HDPI y formato
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                    self.images.append(ctk_img)
                    
                    # Etiqueta con la imagen
                    img_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    img_lbl.pack(pady=(20, 10), padx=20)
                except Exception as e:
                    print(f"Error al cargar imagen {img_file}: {e}")
                    # Fallback
                    lbl = ctk.CTkLabel(card, text="[Imagen]", width=120, height=120)
                    lbl.pack(pady=(20, 10), padx=20)
            else:
                lbl = ctk.CTkLabel(card, text="[Imagen no encontrada]", width=120, height=120)
                lbl.pack(pady=(20, 10), padx=20)
                
            # Botón de radio para seleccionar
            rb = ctk.CTkRadioButton(card, text=name, variable=self.distro_var, value=name,
                                    font=ctk.CTkFont(size=18, weight="bold"), cursor="hand2")
            rb.pack(pady=(0, 20))
        
        # Botones de Acción
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="Volver", command=lambda: controller.show_frame("WelcomeScreen"),
                                   fg_color="gray30", hover_color="gray40", height=50, width=150,
                                   font=ctk.CTkFont(size=16, weight="bold"), cursor="hand2")
        btn_volver.pack(side="left", padx=15)
        
        btn_ejecutar = ctk.CTkButton(btn_frame, text="Confirmar y Ejecutar", command=self.ejecutar_script,
                                     height=50, width=220, font=ctk.CTkFont(size=16, weight="bold"), cursor="hand2")
        btn_ejecutar.pack(side="left", padx=15)
        
    def ejecutar_script(self):
        distro_seleccionada = self.distro_var.get()
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_dir, "script_herramienta.py")
            
            # Ejecutar script
            resultado = subprocess.run([sys.executable, script_path, distro_seleccionada], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                messagebox.showinfo("Éxito", f"Has seleccionado {distro_seleccionada}.\n\nScript ejecutado correctamente:\n{resultado.stdout}")
            else:
                messagebox.showerror("Error", f"Hubo un error al ejecutar el script:\n\n{resultado.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()
