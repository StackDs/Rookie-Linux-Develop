import customtkinter as ctk
import webbrowser
from utils import apply_glow_effect

class DocumentationScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Documentación Oficial_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))
        
        self.tabview = ctk.CTkTabview(self, 
                                      fg_color="#001100", 
                                      segmented_button_fg_color="#002200",
                                      segmented_button_selected_color="#005500",
                                      segmented_button_selected_hover_color="#007700",
                                      segmented_button_unselected_color="#002200",
                                      segmented_button_unselected_hover_color="#003300",
                                      text_color="#00FF00")
        self.tabview.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=10)
        
        self.tabview.add("SO y Núcleo")
        self.tabview.add("Lenguajes")
        self.tabview.add("IDEs y Terminal")
        self.tabview.add("Bases de Datos")
        
        def create_link(parent, text, url, row, col=0):
            btn = ctk.CTkButton(parent, text=f"🔗 {text}", 
                                anchor="w",
                                fg_color="transparent", text_color="#00E676",
                                hover_color="#003300", font=ctk.CTkFont(family="Consolas", size=16),
                                command=lambda u=url: webbrowser.open(u))
            btn.grid(row=row, column=col, padx=20, pady=10, sticky="w")
            apply_glow_effect(btn, default_text=f"🔗 {text}", hover_text=f"🔗 {text}")

        # --- SO y Núcleo ---
        tab_so = self.tabview.tab("SO y Núcleo")
        tab_so.grid_columnconfigure((0,1), weight=1)
        create_link(tab_so, "WSL (Windows Subsystem for Linux)", "https://learn.microsoft.com/es-es/windows/wsl/", 0, 0)
        create_link(tab_so, "Documentación de Ubuntu", "https://help.ubuntu.com/", 1, 0)
        create_link(tab_so, "Documentación de Fedora", "https://docs.fedoraproject.org/", 2, 0)
        create_link(tab_so, "Guía de Linux Mint", "https://linuxmint.com/documentation.php", 0, 1)
        create_link(tab_so, "Soporte de Pop!_OS", "https://support.system76.com/", 1, 1)

        # --- Lenguajes ---
        tab_lang = self.tabview.tab("Lenguajes")
        tab_lang.grid_columnconfigure((0,1), weight=1)
        create_link(tab_lang, "Python 3 Oficial", "https://docs.python.org/3/", 0, 0)
        create_link(tab_lang, "C++ Reference", "https://en.cppreference.com/", 1, 0)
        create_link(tab_lang, "CMake Docs", "https://cmake.org/cmake/help/latest/", 2, 0)
        create_link(tab_lang, "Java SE Docs", "https://docs.oracle.com/en/java/", 3, 0)
        create_link(tab_lang, "Node.js Docs", "https://nodejs.org/en/docs/", 0, 1)
        create_link(tab_lang, "TypeScript Handbook", "https://www.typescriptlang.org/docs/", 1, 1)
        create_link(tab_lang, ".NET Microsoft Docs", "https://learn.microsoft.com/es-es/dotnet/", 2, 1)

        # --- IDEs y Terminal ---
        tab_ide = self.tabview.tab("IDEs y Terminal")
        tab_ide.grid_columnconfigure((0,1), weight=1)
        create_link(tab_ide, "Visual Studio Code", "https://code.visualstudio.com/docs", 0, 0)
        create_link(tab_ide, "IntelliJ IDEA", "https://www.jetbrains.com/help/idea/", 1, 0)
        create_link(tab_ide, "Git (Pro Git Book)", "https://git-scm.com/book/es/v2", 2, 0)
        create_link(tab_ide, "Oh My Zsh", "https://ohmyz.sh/", 3, 0)
        create_link(tab_ide, "Tmux Cheat Sheet", "https://tmuxcheatsheet.com/", 0, 1)
        create_link(tab_ide, "Ripgrep (rg)", "https://github.com/BurntSushi/ripgrep", 1, 1)
        create_link(tab_ide, "FZF (Fuzzy Finder)", "https://github.com/junegunn/fzf", 2, 1)
        
        # --- Base de Datos ---
        tab_db = self.tabview.tab("Bases de Datos")
        tab_db.grid_columnconfigure((0,1), weight=1)
        create_link(tab_db, "Docker & Docker Compose", "https://docs.docker.com/", 0, 0)
        create_link(tab_db, "PostgreSQL Oficial", "https://www.postgresql.org/docs/", 1, 0)
        create_link(tab_db, "DBeaver Docs", "https://dbeaver.com/docs/wiki/", 2, 0)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20))
        
        self.btn_action = ctk.CTkButton(btn_frame, text="← Volver", command=lambda: self.controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")
        self.btn_action.pack(side="left", padx=10)
