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
        self.resizable(False, False)
        
        # Configurar el grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (StartScreen, InfoScreen, DistroSelectionScreen):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def show_frame(self, page_name):
        '''Muestra la pantalla solicitada'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Cargar wallpaper
        wallpaper_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "genericWallpaper.png")
        self.bg_image = None
        if os.path.exists(wallpaper_path):
            try:
                img = Image.open(wallpaper_path)
                # Escalar la imagen al tamaño de la ventana (900x600)
                self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(900, 600))
                
                # Etiqueta que actúa como fondo
                bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
                bg_label.place(relx=0.5, rely=0.5, anchor="center")
            except Exception as e:
                print(f"Error al cargar el wallpaper: {e}")
                
        # Botón solitario flotante interactivo (Glow y flecha animada)
        self.btn = ctk.CTkButton(self, text="Entrar        →", font=ctk.CTkFont(size=20, weight="bold"), 
                            height=60, width=240, corner_radius=15,
                            command=lambda: controller.show_frame("InfoScreen"),
                            cursor="hand2", 
                            fg_color="#1a1a1a", # fondo oscuro (semitransparente visualmente contra el fondo)
                            border_width=2, border_color="#00ACC1", # cian tenue
                            hover_color="#1a1a1a", text_color="#FFFFFF")
        
        # Eventos para el efecto Hover
        self.btn.bind("<Enter>", self.on_hover_enter)
        self.btn.bind("<Leave>", self.on_hover_leave)
        
        # Posicionado en el costado derecho abajo
        self.btn.place(relx=0.95, rely=0.92, anchor="se")

    def on_hover_enter(self, event):
        # Borde brillante cian (Glow) y flecha desplazada a la derecha
        self.btn.configure(
            border_color="#00FFFF", 
            text_color="#00FFFF",
            text="Entrar           →" # Simula un desplazamiento de unos ~5px
        )

    def on_hover_leave(self, event):
        # Vuelve al estado normal
        self.btn.configure(
            border_color="#00ACC1", 
            text_color="#FFFFFF",
            text="Entrar        →"
        )

class InfoScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Centrar contenido
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(self, text="¿Qué hace este programa?", 
                             font=ctk.CTkFont(family="Roboto", size=38, weight="bold"))
        title.grid(row=1, column=0, pady=(0, 40))
        
        # Contenedor principal de la caja de texto
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.grid(row=2, column=0, padx=40, pady=(0, 40), sticky="nsew")
        
        self.grid_rowconfigure(2, weight=1)
        
        # TextBox con scroll automático
        info_textbox = ctk.CTkTextbox(text_frame, font=ctk.CTkFont(family="Roboto", size=16), 
                                      fg_color="gray15", text_color="gray85",
                                      corner_radius=15, wrap="word")
        info_textbox.pack(fill="both", expand=True)
        
        # Texto detallado (resumido y amigable)
        info_text = (
            "Rookie-Linux-Develop es una aplicación desarrollada con el fin de generar una "
            "imagen de Linux equipada con todo lo necesario para comenzar a desarrollar. "
            "Su objetivo principal es introducir de forma fácil y amigable a nuevos usuarios "
            "al entorno de Linux, evitando configuraciones tediosas.\n\n"
            "Esta herramienta automatiza la preparación de tu entorno. A continuación, un resumen "
            "de lo que incluye la imagen generada:\n\n"
            "=== DISTRIBUCIONES ===\n"
            "• Opciones populares como Ubuntu, Mint, Fedora, Pop!_OS, entre otras.\n\n"
            "=== ENTORNOS DE DESARROLLO (IDE's) ===\n"
            "• Editores modernos y potentes como Visual Studio Code, IntelliJ IDEA, Emacs y Antigravity.\n\n"
            "=== LENGUAJES Y COMPILADORES ===\n"
            "• Entornos listos para programar en C/C++, Java, Python, C# (.NET) y JavaScript/TypeScript.\n\n"
            "=== BASES DE DATOS ===\n"
            "• Motores como PostgreSQL y SQLite, con clientes gráficos como DBeaver y pgAdmin4.\n\n"
            "=== LIBRERÍAS Y FRAMEWORKS ===\n"
            "• Ciencia de Datos en Python: Herramientas para análisis y manejo de datos (Pandas, NumPy, JupyterLab, etc.).\n"
            "• Desarrollo Web: Flask, Django, FastAPI y utilidades para Node.js.\n"
            "• Gráficos interactivos: Librerías esenciales para C/C++ (SDL2, OpenGL, SFML).\n"
            "• Desarrollo Móvil: Flutter y Dart SDK.\n\n"
            "=== HERRAMIENTAS DE SISTEMA Y CONTENEDORES ===\n"
            "• Git y GitHub CLI preconfigurados para gestionar tu código.\n"
            "• Docker Engine y Docker Compose para trabajar fácilmente con contenedores.\n"
            "• Terminales vitaminadas (Zsh, tmux) y utilidades modernas de consola para búsquedas y monitoreo.\n\n"
            "=== APLICACIONES DE USO DIARIO ===\n"
            "• Navegadores web seguros (Brave, Firefox).\n"
            "• Ofimática y multimedia completa (LibreOffice, VLC, OBS Studio).\n"
            "• Herramientas educativas y páginas web útiles preconfiguradas (como JFLAP)."
        )
        
        info_textbox.insert("0.0", info_text)
        info_textbox.configure(state="disabled") # Hacerlo de solo lectura
        
        # Frame de botones
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="Volver", command=lambda: controller.show_frame("StartScreen"),
                                   height=50, width=150, corner_radius=15,
                                   font=ctk.CTkFont(size=16, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#757575",
                                   hover_color="#757575", text_color="#FFFFFF")
        btn_volver.pack(side="left", padx=15)
        
        btn_siguiente = ctk.CTkButton(btn_frame, text="Siguiente", command=lambda: controller.show_frame("DistroSelectionScreen"),
                                      height=50, width=200, corner_radius=15,
                                      font=ctk.CTkFont(size=16, weight="bold"), cursor="hand2",
                                      fg_color="transparent", border_width=2, border_color="#1E88E5",
                                      hover_color="#1E88E5", text_color="#FFFFFF")
        btn_siguiente.pack(side="left", padx=15)

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
            ("Fedora", "fedora-logo.png"),
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
        
        # Cambiado para que el botón "Volver" regrese a la pantalla InfoScreen en vez de WelcomeScreen
        btn_volver = ctk.CTkButton(btn_frame, text="Volver", command=lambda: controller.show_frame("InfoScreen"),
                                   height=50, width=150, corner_radius=15,
                                   font=ctk.CTkFont(size=16, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#757575",
                                   hover_color="#757575", text_color="#FFFFFF")
        btn_volver.pack(side="left", padx=15)
        
        btn_ejecutar = ctk.CTkButton(btn_frame, text="Confirmar y Ejecutar", command=self.ejecutar_script,
                                     height=50, width=220, corner_radius=15,
                                     font=ctk.CTkFont(size=16, weight="bold"), cursor="hand2",
                                     fg_color="transparent", border_width=2, border_color="#1E88E5",
                                     hover_color="#1E88E5", text_color="#FFFFFF")
        btn_ejecutar.pack(side="left", padx=15)
        
    def ejecutar_script(self):
        distro_seleccionada = self.distro_var.get()
        
        if distro_seleccionada == "Pop!_OS":
            respuesta = messagebox.askyesno(
                "Versión de Pop!_OS", 
                "¿Tienes una tarjeta gráfica NVIDIA en tu equipo?\n\n"
                "• Selecciona 'Sí' para usar la ISO con drivers NVIDIA preinstalados.\n"
                "• Selecciona 'No' para usar la ISO estándar (Intel/AMD)."
            )
            if respuesta:
                distro_seleccionada = "Pop!_OS (NVIDIA)"
            else:
                distro_seleccionada = "Pop!_OS (Intel/AMD)"
                
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
