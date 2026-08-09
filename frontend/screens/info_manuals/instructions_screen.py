import customtkinter as ctk
from utils import apply_glow_effect

class InstructionsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
            
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="> Instrucciones de uso_", 
                             text_color="#00FF00",
                             font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        title.grid(row=0, column=0, pady=(20, 10))
        
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=10)
        
        self.info_textbox = ctk.CTkTextbox(text_frame, font=ctk.CTkFont(family="Consolas", size=15), 
                                           fg_color="transparent", text_color="#00E676", 
                                           corner_radius=0, wrap="word", border_width=0)
        self.info_textbox.pack(fill="both", expand=True)
        self.info_textbox.configure(state="disabled")
        
        self.info_text = (
            "> Cargando manual de usuario...\n"
            "> Listo.\n\n"
            "Aquí tienes una guía rápida de cómo utilizar cada sección de Rookie Linux Develop:\n\n"
            "[1] SOBRE LINUX\n"
            "    Aquí encontrarás información importante acerca de Linux y su\n"
            "    funcionamiento, distribuciones, etc. Además de encontrar\n"
            "    diferencias con Windows, formas de instalación y demás.\n\n"
            "[2] INSTALAR WSL (En caso de usar windows)\n"
            "    Visita esta opción antes que nada, el sistema hace uso de WSL\n"
            "    para funcionar, esto es exclusivo para windows, ya que en sistemas linux \n"
            "    usará comandos nativos.\n\n"
            "[3] CREAR IMAGEN PERSONALIZADA\n"
            "    El sistema permite seleccionar una distribución de tu interés\n"
            "    (ej. Ubuntu, Mint, Pop!). El sistema descargará la ISO oficial\n"
            "    y le inyectará todas las herramientas de desarrollo, librerías\n"
            "    y configuraciones predefinidas. Una vez terminada tendrás en\n"
            "    la carpeta output tu imagen custom, que podrás flashear en un\n"
            "    usb o usar en una máquina virtual.\n\n"
            "[4] MONTAR IMAGEN (REQUIERE USB)\n"
            "    Una vez que hayas creado tu imagen personalizada, usa esta\n"
            "    opción para 'flashearla' (grabarla) de forma segura en una\n"
            "    memoria USB. Luego podrás usar ese USB para instalar Linux\n"
            "    en tu computadora. Una vez que se instale el sistema, se\n"
            "    ejecutará automáticamente. El script de bienvenida te pedirá\n"
            "    iniciar sesión, y de ahí en adelante, se instalarán todas\n"
            "    las herramientas.\n\n"
            
            "> Si tienes dudas, consulta la documentación oficial en el repositorio.\n"
            "> Esperando acción del usuario..."
        )
        
        self.typing_job = None
        self.char_index = 0
        self.has_animated = False
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20))
        
        btn_home = ctk.CTkButton(btn_frame, text="⌂ Volver a Información", command=lambda: controller.show_frame("InfoScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_home, default_text="⌂ Volver a Información", hover_text="⌂ Volver a Información")
        btn_home.pack(side="left", padx=15)

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
