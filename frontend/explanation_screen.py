import customtkinter as ctk
from utils import apply_glow_effect

class ExplanationScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="> Sobre Linux_", 
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
            "> Comparten el mismo 'motor', pero ofrecen diseños y herramientas diferentes.\n\n"
            "[+] ¿Cómo instalamos una distro?\n"
            "  Existen 3 métodos principales:\n"
            "  1. Instalación nativa (Dual Boot): Consiste en instalar Linux en\n"
            "     una partición del disco duro, junto con Windows.\n"
            "  2. Máquina Virtual: Consiste en instalar Linux en una máquina\n"
            "     virtual, que es un emulador de hardware que permite ejecutar\n"
            "     otro sistema operativo dentro de Windows.\n"
            "  3. Instalación limpia: Consiste en reemplazar Windows por Linux.\n\n"
            "> Todos estos conceptos serán explicados detalladamente más adelante." 
        )
        
        self.typing_job = None
        self.char_index = 0
        self.has_animated = False
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(0, 40))
        
        btn_volver = ctk.CTkButton(btn_frame, text="←    Volver", command=lambda: controller.show_frame("InfoScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_volver, default_text="←    Volver", hover_text="←       Volver")
        btn_volver.pack(side="left", padx=15)
        
        btn_siguiente = ctk.CTkButton(btn_frame, text="Siguiente    →", command=lambda: controller.show_frame("BasicConceptsScreen"),
                                      height=45, width=220, corner_radius=5,
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
