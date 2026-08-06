import customtkinter as ctk
from utils import apply_glow_effect

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
            "    - Navegadores: Brave, Firefox\n"
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
        
        btn_home = ctk.CTkButton(btn_frame, text="⌂ Volver a Opciones", command=lambda: controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(btn_home, default_text="⌂ Volver a Opciones", hover_text="⌂ Volver a Opciones")
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
