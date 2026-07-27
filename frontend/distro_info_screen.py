import customtkinter as ctk
import os
from PIL import Image
from utils import apply_glow_effect, get_project_root

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
                "soporte a largo plazo (LTS) y una amplia compatibilidad de hardware.\n\n"
                "⏱️ Tiempo est. de instalación: ~25-35 minutos (incluye scripts)\n"
                "💾 Espacio requerido en Disco: Mínimo 25 GB\n"
                "🔌 Espacio requerido en USB: Mínimo 8 GB"
            ),
            "Linux Mint": (
                "> Analizando: Linux Mint\n\n"
                "Linux Mint está diseñada para que cambiar a Linux sea lo más sencillo posible, especialmente "
                "si provienes de Windows. Basada en Ubuntu, ofrece una experiencia cómoda, rápida y estable "
                "con una interfaz familiar.\n\n"
                "Incluye numerosas herramientas listas para usar, excelente rendimiento y acceso a los mismos "
                "repositorios de Ubuntu, siendo ideal para dar nueva vida a equipos antiguos o para el uso diario "
                "sin complicaciones.\n\n"
                "⏱️ Tiempo est. de instalación: ~25-35 minutos (incluye scripts)\n"
                "💾 Espacio requerido en Disco: Mínimo 20 GB\n"
                "🔌 Espacio requerido en USB: Mínimo 4 GB (Se recomiendan 8 GB)"
            ),
            "Fedora": (
                "> Analizando: Fedora Linux\n\n"
                "Fedora combina innovación y confiabilidad en una distribución diseñada para quienes quieren estar "
                "a la vanguardia. Impulsada por la comunidad y patrocinada por Red Hat, incorpora siempre las "
                "tecnologías más recientes del ecosistema Linux.\n\n"
                "Con su enfoque en la seguridad, software actualizado y excelente integración con contenedores, "
                "es una opción perfecta para desarrolladores, estudiantes y usuarios que buscan un sistema moderno "
                "y de alto rendimiento.\n\n"
                "⏱️ Tiempo est. de instalación: ~30-40 minutos (incluye scripts)\n"
                "💾 Espacio requerido en Disco: Mínimo 20 GB\n"
                "🔌 Espacio requerido en USB: Mínimo 8 GB"
            ),
            "Pop!_OS": (
                "> Analizando: Pop!_OS\n\n"
                "Pop!_OS está pensado para quienes quieren hacer más con menos esfuerzo. Desarrollada por System76 "
                "y basada en Ubuntu, ofrece una experiencia moderna enfocada en la productividad y el flujo de trabajo.\n\n"
                "Destaca por sus potentes funciones de gestión de ventanas, excelente soporte para gamers "
                "y creadores de contenido, y por ofrecer versiones optimizadas para tarjetas "
                "gráficas NVIDIA y AMD.\n\n"
                "⏱️ Tiempo est. de instalación: ~25-35 minutos (incluye scripts)\n"
                "💾 Espacio requerido en Disco: Mínimo 20 GB\n"
                "🔌 Espacio requerido en USB: Mínimo 8 GB"
            )
        }
        
        self.typing_job = None
        self.char_index = 0
        self.current_text = ""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.last_distro = None
        btn_frame.grid(row=4, column=0, pady=(0, 40))
        
        self.btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: self.controller.show_frame("DistroSelectionScreen"),
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_volver, default_text="←    Volver", hover_text="←       Volver")
        self.btn_volver.pack(side="left", padx=15)
        
        self.btn_ejecutar = ctk.CTkButton(btn_frame, text="Confirmar y Ejecutar", command=lambda: self.controller.show_frame("BuildProgressScreen"),
                                     height=45, width=220, corner_radius=5,
                                     font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                     fg_color="transparent", border_width=2, border_color="#008800",
                                     hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_ejecutar, default_text="Confirmar y Ejecutar", hover_text="Confirmar y Ejecutar")
        self.btn_ejecutar.pack(side="left", padx=15)

    def load_images(self, distro):
        folder = self.folder_map.get(distro, "Ubuntu")
        base_path = os.path.join(get_project_root(), "assets", "DistrosScreenShots", folder)
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
