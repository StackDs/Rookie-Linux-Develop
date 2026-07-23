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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Efecto Glow Estilo Terminal
def apply_glow_effect(btn, default_text, hover_text=None):
    color_base = "#008800" # Verde terminal atenuado
    color_glow = "#00FF00" # Verde terminal brillante
    
    def on_enter(e):
        btn.configure(
            border_color=color_glow,
            text_color=color_glow,
            text=hover_text if hover_text else default_text
        )
        
    def on_leave(e):
        btn.configure(
            border_color=color_base,
            text_color=color_base,
            text=default_text
        )
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rookie Linux Developer - Terminal Mode")
        self.geometry("900x600")
        self.resizable(True, True)
        self.minsize(800, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Fondo negro sólido estilo terminal para toda la app
        self.container = ctk.CTkFrame(self, fg_color="#0a0a0a")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartScreen, InfoScreen, ExplanationScreen, DistroSelectionScreen, DistroInfoScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()


class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Textos de bienvenida estilo terminal
        self.title_lbl = ctk.CTkLabel(self, text=">_ ROOKIE LINUX DEVELOPER", 
                                      font=ctk.CTkFont(family="Consolas", size=50, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.place(relx=0.5, rely=0.35, anchor="center")
        
        self.subtitle_lbl = ctk.CTkLabel(self, text="[ Sistema de despliegue automatizado en espera ]", 
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


class InfoScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
            
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="> ¿Qué hace este programa?_", 
                             text_color="#00FF00",
                             font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        title.grid(row=1, column=0, pady=(0, 20))
        
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.grid(row=2, column=0, padx=40, pady=(0, 40), sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        
        self.info_textbox = ctk.CTkTextbox(text_frame, font=ctk.CTkFont(family="Consolas", size=15), 
                                           fg_color="transparent", text_color="#00E676", 
                                           corner_radius=0, wrap="word", border_width=0)
        self.info_textbox.pack(fill="both", expand=True)
        self.info_textbox.configure(state="disabled")
        
        self.info_text = (
            "> Inicializando Rookie-Linux-Develop v1.0...\n"
            "> Cargando dependencias...\n"
            "> Listo.\n\n"
            "Rookie-Linux-Develop es una herramienta diseñada para generar una imagen "
            "de Linux completamente equipada para el desarrollo. Su objetivo es evitar las "
            "configuraciones tediosas y darte un entorno profesional desde el primer minuto.\n\n"
            "A continuación, un resumen de la configuración del entorno:\n\n"
            "[+] DISTRIBUCIONES SOPORTADAS\n"
            "    - Ubuntu, Mint, Fedora, Pop!_OS, entre otras.\n\n"
            "[+] ENTORNOS DE DESARROLLO (IDE's)\n"
            "    - Visual Studio Code\n"
            "    - IntelliJ IDEA\n"
            "    - Emacs\n"
            "    - Antigravity\n\n"
            "[+] LENGUAJES Y COMPILADORES\n"
            "    - C/C++ (gcc, clang, make, cmake, gdb, valgrind)\n"
            "    - Java (OpenJDK 17/21, Maven)\n"
            "    - Python (Python 3, pip, venv, flake8, ipython)\n"
            "    - C# (.NET SDK)\n"
            "    - JavaScript/TypeScript (Node.js LTS, npm)\n\n"
            "[+] BASES DE DATOS\n"
            "    - PostgreSQL, SQLite\n"
            "    - Clientes: DBeaver, pgAdmin4\n\n"
            "[+] LIBRERÍAS Y FRAMEWORKS\n"
            "    - Data Science: Pandas, NumPy, JupyterLab\n"
            "    - Desarrollo Web: Flask, Django, FastAPI\n"
            "    - Gráficos (C++): SDL2, OpenGL, SFML\n"
            "    - Móvil: Flutter, Dart SDK\n\n"
            "[+] SISTEMA Y CONTENEDORES\n"
            "    - Git, GitHub CLI\n"
            "    - Docker Engine, Docker Compose\n"
            "    - Utilidades: Zsh, tmux, htop, btop, ripgrep, fzf, jq\n\n"
            "[+] USO DIARIO\n"
            "    - Navegadores: Brave, Firefox, Chromium\n"
            "    - Multimedia/Ofimática: OBS Studio, VLC, LibreOffice\n"
            "    - Otros: JFLAP\n\n"
            "> Fin de la lectura de paquetes.\n"
            "> Esperando acción del usuario..."
        )
        
        self.typing_job = None
        self.char_index = 0
        self.has_animated = False
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: controller.show_frame("StartScreen"),
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_volver, default_text="←    Volver", hover_text="←       Volver")
        btn_volver.pack(side="left", padx=15)
        
        btn_siguiente = ctk.CTkButton(btn_frame, text="Siguiente    →", command=lambda: controller.show_frame("ExplanationScreen"),
                                      height=45, width=170, corner_radius=5,
                                      font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                      fg_color="transparent", border_width=2, border_color="#008800",
                                      hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_siguiente, default_text="Siguiente    →", hover_text="Siguiente       →")
        btn_siguiente.pack(side="left", padx=15)

    def on_show(self):
        if not getattr(self, "has_animated", False):
            self.has_animated = True
            if self.typing_job:
                self.after_cancel(self.typing_job)
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("0.0", "end")
            self.char_index = 0
            self.type_character()
        else:
            if self.typing_job:
                self.after_cancel(self.typing_job)
                self.typing_job = None
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("0.0", "end")
            self.info_textbox.insert("end", self.info_text)
            self.info_textbox.configure(state="disabled")
            self.info_textbox.see("end")
        
    def type_character(self):
        if self.char_index < len(self.info_text):
            chunk_size = 2 
            chunk = self.info_text[self.char_index : self.char_index + chunk_size]
            self.info_textbox.insert("end", chunk)
            self.info_textbox.see("end")
            self.char_index += chunk_size
            self.typing_job = self.after(10, self.type_character)
        else:
            self.info_textbox.configure(state="disabled")


class ExplanationScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="> Conceptos Básicos_", 
                             text_color="#00FF00",
                             font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        title.grid(row=1, column=0, pady=(0, 20))
        
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.grid(row=2, column=0, padx=40, pady=(0, 40), sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        
        self.info_textbox = ctk.CTkTextbox(text_frame, font=ctk.CTkFont(family="Consolas", size=16), 
                                           fg_color="transparent", text_color="#00E676", 
                                           corner_radius=0, wrap="word", border_width=0)
        self.info_textbox.pack(fill="both", expand=True)
        self.info_textbox.configure(state="disabled")
        
        self.info_text = (
            "> ¿Qué es Linux y qué es una Distribución?\n\n"
            "Mucha gente dice 'Uso Linux', pero técnicamente esto es inexacto. "
            "Linux NO es un sistema operativo completo por sí solo. Linux es únicamente el KERNEL.\n\n"
            "[+] EL KERNEL DE LINUX\n"
            "El kernel (o núcleo) es el motor del sistema. Es la pieza de software más profunda "
            "que se comunica directamente con el hardware (tu CPU, memoria, teclado, pantalla). "
            "Sin embargo, un motor por sí solo no te sirve para conducir; necesitas un volante, "
            "ruedas y un chasis para interactuar con él.\n\n"
            "[+] EL SISTEMA OPERATIVO GNU/LINUX\n"
            "Para que el kernel sea útil para una persona, se le agregan herramientas y programas "
            "de usuario (muchos de ellos provenientes del proyecto GNU), interfaces gráficas, "
            "terminales, manejadores de archivos y navegadores. La combinación del Kernel Linux "
            "más todo este software de usuario forma un sistema operativo completo.\n\n"
            "[+] ¿QUÉ ES UNA DISTRIBUCIÓN (DISTRO)?\n"
            "Como el Kernel de Linux y las herramientas de usuario son de código abierto (libres), "
            "cualquier grupo u organización puede tomar ese Kernel, empaquetarlo con su propia "
            "selección de software, su propio entorno gráfico y sus propias herramientas, "
            "creando un 'sabor' único. A estos sabores se les llama 'Distribuciones'.\n\n"
            "> Ubuntu, Fedora, Mint y Pop!_OS son ejemplos de distribuciones.\n"
            "> Comparten el mismo 'motor', pero ofrecen diseños y herramientas diferentes."
        )
        
        self.typing_job = None
        self.char_index = 0
        self.has_animated = False
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: controller.show_frame("InfoScreen"),
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_volver, default_text="←    Volver", hover_text="←       Volver")
        btn_volver.pack(side="left", padx=15)
        
        btn_siguiente = ctk.CTkButton(btn_frame, text="Entendido    →", command=lambda: controller.show_frame("DistroSelectionScreen"),
                                      height=45, width=180, corner_radius=5,
                                      font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                      fg_color="transparent", border_width=2, border_color="#008800",
                                      hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_siguiente, default_text="Entendido    →", hover_text="Entendido       →")
        btn_siguiente.pack(side="left", padx=15)

    def on_show(self):
        if not getattr(self, "has_animated", False):
            self.has_animated = True
            if self.typing_job:
                self.after_cancel(self.typing_job)
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("0.0", "end")
            self.char_index = 0
            self.type_character()
        else:
            if self.typing_job:
                self.after_cancel(self.typing_job)
                self.typing_job = None
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("0.0", "end")
            self.info_textbox.insert("end", self.info_text)
            self.info_textbox.configure(state="disabled")
            self.info_textbox.see("end")
        
    def type_character(self):
        if self.char_index < len(self.info_text):
            chunk_size = 2 
            chunk = self.info_text[self.char_index : self.char_index + chunk_size]
            self.info_textbox.insert("end", chunk)
            self.info_textbox.see("end")
            self.char_index += chunk_size
            self.typing_job = self.after(10, self.type_character)
        else:
            self.info_textbox.configure(state="disabled")


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
            img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", img_file)
            
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
        
        btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: controller.show_frame("ExplanationScreen"),
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_volver, default_text="←    Volver", hover_text="←       Volver")
        btn_volver.pack(side="left", padx=15)
        
        btn_siguiente = ctk.CTkButton(btn_frame, text="Siguiente    →", command=lambda: controller.show_frame("DistroInfoScreen"),
                                      height=45, width=170, corner_radius=5,
                                      font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                      fg_color="transparent", border_width=2, border_color="#008800",
                                      hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_siguiente, default_text="Siguiente    →", hover_text="Siguiente       →")
        btn_siguiente.pack(side="left", padx=15)

class DistroInfoScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Información_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=1, column=0, pady=(0, 20))
        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=2, column=0, padx=40, pady=(0, 40), sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        
        content_frame.grid_columnconfigure(0, weight=3) # Lado texto
        content_frame.grid_columnconfigure(1, weight=2) # Lado imágenes
        content_frame.grid_rowconfigure(0, weight=1)
        
        self.info_textbox = ctk.CTkTextbox(content_frame, font=ctk.CTkFont(family="Consolas", size=15), 
                                           fg_color="transparent", text_color="#00E676", 
                                           corner_radius=0, wrap="word", border_width=0)
        self.info_textbox.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.info_textbox.configure(state="disabled")
        
        self.images_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.images_frame.grid(row=0, column=1, sticky="nsew")
        self.images_frame.grid_rowconfigure(0, weight=2)
        self.images_frame.grid_rowconfigure(1, weight=1)
        self.images_frame.grid_columnconfigure(0, weight=1)
        self.images_frame.grid_columnconfigure(1, weight=1)
        
        self.img_btn_escritorio = ctk.CTkButton(self.images_frame, text="", fg_color="transparent", hover_color="#002200", cursor="hand2")
        self.img_btn_escritorio.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 5))
        
        self.img_btn_gestor = ctk.CTkButton(self.images_frame, text="", fg_color="transparent", hover_color="#002200", cursor="hand2")
        self.img_btn_gestor.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        
        self.img_btn_terminal = ctk.CTkButton(self.images_frame, text="", fg_color="transparent", hover_color="#002200", cursor="hand2")
        self.img_btn_terminal.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        
        self.folder_map = {
            "Ubuntu": "Ubuntu",
            "Linux Mint": "Mint",
            "Fedora": "Fedora",
            "Pop!_OS": "Pop"
        }
        self.current_images = []
        
        self.distro_texts = {
            "Ubuntu": (
                "> Analizando: Ubuntu Linux\n\n"
                "Ubuntu es el punto de partida perfecto para entrar al mundo Linux y una de las distribuciones "
                "más populares. Basada en Debian, combina simplicidad, estabilidad y rendimiento.\n\n"
                "Destaca por su facilidad de uso, su enorme catálogo de software y su gran comunidad que facilita "
                "encontrar ayuda. Es ideal tanto para principiantes como para usuarios avanzados, ofreciendo "
                "soporte a largo plazo (LTS) y una amplia compatibilidad de hardware."
            ),
            "Linux Mint": (
                "> Analizando: Linux Mint\n\n"
                "Linux Mint está diseñada para que cambiar a Linux sea lo más sencillo posible, especialmente "
                "si provienes de Windows. Basada en Ubuntu, ofrece una experiencia cómoda, rápida y estable "
                "con una interfaz familiar.\n\n"
                "Incluye numerosas herramientas listas para usar, excelente rendimiento y acceso a los mismos "
                "repositorios de Ubuntu, siendo ideal para dar nueva vida a equipos antiguos o para el uso diario "
                "sin complicaciones."
            ),
            "Fedora": (
                "> Analizando: Fedora Linux\n\n"
                "Fedora combina innovación y confiabilidad en una distribución diseñada para quienes quieren estar "
                "a la vanguardia. Impulsada por la comunidad y patrocinada por Red Hat, incorpora siempre las "
                "tecnologías más recientes del ecosistema Linux.\n\n"
                "Con su enfoque en la seguridad, software actualizado y excelente integración con contenedores, "
                "es una opción perfecta para desarrolladores, estudiantes y usuarios que buscan un sistema moderno "
                "y de alto rendimiento."
            ),
            "Pop!_OS": (
                "> Analizando: Pop!_OS\n\n"
                "Pop!_OS está pensado para quienes quieren hacer más con menos esfuerzo. Desarrollada por System76 "
                "y basada en Ubuntu, ofrece una experiencia moderna enfocada en la productividad y el flujo de trabajo.\n\n"
                "Destaca por sus potentes funciones de gestión de ventanas, excelente soporte para gamers "
                "y creadores de contenido, y por ofrecer versiones optimizadas para tarjetas "
                "gráficas NVIDIA y AMD."
            )
        }
        
        self.typing_job = None
        self.char_index = 0
        self.current_text = ""
        self.last_distro = None
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: controller.show_frame("DistroSelectionScreen"),
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_volver, default_text="←    Volver", hover_text="←       Volver")
        btn_volver.pack(side="left", padx=15)
        
        btn_ejecutar = ctk.CTkButton(btn_frame, text="Confirmar y Ejecutar", command=self.ejecutar_script,
                                     height=45, width=220, corner_radius=5,
                                     font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                     fg_color="transparent", border_width=2, border_color="#008800",
                                     hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_ejecutar, default_text="Confirmar y Ejecutar", hover_text="Confirmar y Ejecutar")
        btn_ejecutar.pack(side="left", padx=15)

    def load_images(self, distro):
        folder = self.folder_map.get(distro, "Ubuntu")
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "DistrosScreenShots", folder)
        self.current_images = []
        
        def set_img(btn, filename, size):
            try:
                img_path = os.path.join(base_path, filename)
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    if img.mode != 'RGBA' and img.mode != 'RGB':
                        img = img.convert('RGBA')
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                    self.current_images.append(ctk_img)
                    btn.configure(image=ctk_img, text="", command=lambda p=img_path: self.zoom_image(p))
                else:
                    btn.configure(image="", text=f"[{filename} null]", command=None)
            except Exception as e:
                btn.configure(image="", text="[Error]", command=None)

        set_img(self.img_btn_escritorio, "escritorio.png", (360, 220))
        set_img(self.img_btn_gestor, "gestor.png", (175, 110))
        set_img(self.img_btn_terminal, "terminal.png", (175, 110))

    def zoom_image(self, img_path):
        top = ctk.CTkToplevel(self)
        top.title("Visor de Imagen")
        top.geometry("1000x700")
        top.configure(fg_color="#0a0a0a")
        top.transient(self.winfo_toplevel())
        top.grab_set()
        
        try:
            img = Image.open(img_path)
            width, height = img.size
            ratio = min(950/width, 650/height)
            new_w, new_h = int(width * ratio), int(height * ratio)
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            lbl = ctk.CTkLabel(top, image=ctk_img, text="")
            lbl.pack(expand=True, fill="both", padx=20, pady=20)
            
            lbl.bind("<Button-1>", lambda e: top.destroy())
        except Exception:
            err = ctk.CTkLabel(top, text="Error cargando zoom.", text_color="#FF0000")
            err.pack(expand=True)
            
        top.bind("<Escape>", lambda e: top.destroy())

    def on_show(self):
        distro = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        self.title.configure(text=f"> Información de {distro}_")
        self.current_text = self.distro_texts.get(distro, "> Analizando...\n\nInformación no disponible.")
        
        if distro != self.last_distro:
            self.last_distro = distro
            self.load_images(distro)
            if self.typing_job:
                self.after_cancel(self.typing_job)
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("0.0", "end")
            self.char_index = 0
            self.type_character()
        else:
            if self.typing_job:
                self.after_cancel(self.typing_job)
                self.typing_job = None
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("0.0", "end")
            self.info_textbox.insert("end", self.current_text)
            self.info_textbox.configure(state="disabled")
            self.info_textbox.see("end")
            
    def type_character(self):
        if self.char_index < len(self.current_text):
            chunk_size = 2 
            chunk = self.current_text[self.char_index : self.char_index + chunk_size]
            self.info_textbox.insert("end", chunk)
            self.info_textbox.see("end")
            self.char_index += chunk_size
            self.typing_job = self.after(10, self.type_character)
        else:
            self.info_textbox.configure(state="disabled")

    def ejecutar_script(self):
        distro_seleccionada = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        
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
