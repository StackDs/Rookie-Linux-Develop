from customtkinter.windows.widgets import core_rendering
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
        self.tabview.add("Librerías y Frameworks")
        self.tabview.add("Ofimática")
        self.tabview.add("Tutoriales")
        
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
        create_link(tab_so, "Documentación de WSL", "https://learn.microsoft.com/es-es/windows/wsl/", 0, 0)
        create_link(tab_so, "Documentación de Ubuntu", "https://help.ubuntu.com/", 1, 0)
        create_link(tab_so, "Documentación de Fedora", "https://docs.fedoraproject.org/", 2, 0)
        create_link(tab_so, "Documentación de Linux Mint", "https://linuxmint.com/documentation.php", 0, 1)
        create_link(tab_so, "Documentación de Pop!_OS", "https://support.system76.com/", 1, 1)
        create_link(tab_so, "Documentación del Kernel de Linux", "https://docs.kernel.org/", 2, 1)
        create_link(tab_so, "La Biblia de Linux", "https://wiki.archlinux.org/", 3, 0)

        # --- Lenguajes ---
        tab_lang = self.tabview.tab("Lenguajes")
        tab_lang.grid_columnconfigure((0,1), weight=1)
        create_link(tab_lang, "Documentación de Python", "https://docs.python.org/3/", 0, 0)
        create_link(tab_lang, "Documentación de C++", "https://en.cppreference.com/", 1, 0)
        create_link(tab_lang, "Documentación de CMake", "https://cmake.org/cmake/help/latest/", 2, 0)
        create_link(tab_lang, "Documentación de Java", "https://docs.oracle.com/en/java/", 3, 0)
        create_link(tab_lang, "Documentación de GCC", "https://gcc.gnu.org/onlinedocs/", 4, 0)
        create_link(tab_lang, "Documentación de Clang", "https://clang.llvm.org/docs/", 5, 0)
        create_link(tab_lang, "Documentación de Make", "https://www.gnu.org/software/make/manual/", 6, 0)
        create_link(tab_lang, "Documentación de GDB", "https://sourceware.org/gdb/documentation/", 7, 0)
        create_link(tab_lang, "Documentación de Valgrind", "https://valgrind.org/docs/manual/manual.html", 8, 0)
        create_link(tab_lang, "Documentación de Node.js", "https://nodejs.org/en/docs/", 0, 1)
        create_link(tab_lang, "Documentación de TypeScript", "https://www.typescriptlang.org/docs/", 1, 1)
        create_link(tab_lang, "Documentación de .NET Microsoft", "https://learn.microsoft.com/es-es/dotnet/", 2, 1)
        create_link(tab_lang, "Documentación de Maven", "https://maven.apache.org/guides/", 3, 1)
        create_link(tab_lang, "Documentación de Flake8", "https://flake8.pycqa.org/en/latest/", 4, 1)
        create_link(tab_lang, "Documentación de IPython", "https://ipython.readthedocs.io/", 5, 1)
        create_link(tab_lang, "Documentación de Dart", "https://dart.dev/guides", 6, 1)
        create_link(tab_lang, "Documentación de Bash", "https://www.gnu.org/software/bash/manual/", 7, 1)
        # --- IDEs y Terminal ---
        tab_ide = self.tabview.tab("IDEs y Terminal")
        tab_ide.grid_columnconfigure((0,1), weight=1)
        create_link(tab_ide, "Documentación de Visual Studio Code", "https://code.visualstudio.com/docs", 0, 0)
        create_link(tab_ide, "Documentación de IntelliJ IDEA", "https://www.jetbrains.com/help/idea/", 1, 0)
        create_link(tab_ide, "Documentación de Git (Pro Git Book)", "https://git-scm.com/book/es/v2", 2, 0)
        create_link(tab_ide, "Documentación de Oh My Zsh", "https://ohmyz.sh/", 3, 0)
        create_link(tab_ide, "Documentación de Emacs", "https://www.gnu.org/software/emacs/manual/", 4, 0)
        create_link(tab_ide, "Documentación de GitHub CLI", "https://cli.github.com/manual/", 5, 0)
        create_link(tab_ide, "Documentación de htop", "https://htop.dev/", 6, 0)
        create_link(tab_ide, "Documentación de Tmux", "https://tmuxcheatsheet.com/", 0, 1)
        create_link(tab_ide, "Documentación de Ripgrep (rg)", "https://github.com/BurntSushi/ripgrep", 1, 1)
        create_link(tab_ide, "Documentación de FZF (Fuzzy Finder)", "https://github.com/junegunn/fzf", 2, 1)
        create_link(tab_ide, "Documentación de btop", "https://github.com/aristocratos/btop", 3, 1)
        create_link(tab_ide, "Documentación de jq Manual", "https://jqlang.github.io/jq/manual/", 4, 1)
        create_link(tab_ide, "Documentación de Antigravity", "https://antigravity.google/docs/getting-started", 5, 1)
        
        # --- Base de Datos ---
        tab_db = self.tabview.tab("Bases de Datos")
        tab_db.grid_columnconfigure((0,1), weight=1)
        create_link(tab_db, "Documentación de Docker & Docker Compose", "https://docs.docker.com/", 0, 0)
        create_link(tab_db, "Documentación de PostgreSQL", "https://www.postgresql.org/docs/", 1, 0)
        create_link(tab_db, "Documentación de DBeaver", "https://dbeaver.com/docs/wiki/", 2, 0)
        create_link(tab_db, "Documentación de SQLite", "https://www.sqlite.org/docs.html", 0, 1)
        create_link(tab_db, "Documentación de pgAdmin 4", "https://www.pgadmin.org/docs/", 1, 1)

        # --- Librerías y Frameworks ---
        tab_libs = self.tabview.tab("Librerías y Frameworks")
        tab_libs.grid_columnconfigure((0,1), weight=1)
        
        # Columna 0: Python y Web
        create_link(tab_libs, "Documentación de Pandas", "https://pandas.pydata.org/docs/", 0, 0)
        create_link(tab_libs, "Documentación de NumPy", "https://numpy.org/doc/stable/", 1, 0)
        create_link(tab_libs, "Documentación de JupyterLab", "https://jupyterlab.readthedocs.io/", 2, 0)
        create_link(tab_libs, "Documentación de Flask", "https://flask.palletsprojects.com/", 3, 0)
        create_link(tab_libs, "Documentación de Django", "https://docs.djangoproject.com/", 4, 0)
        create_link(tab_libs, "Documentación de FastAPI", "https://fastapi.tiangolo.com/", 5, 0)
        
        # Columna 1: Gráficos y Móvil
        create_link(tab_libs, "Documentación de SDL2 Wiki", "https://wiki.libsdl.org/", 0, 1)
        create_link(tab_libs, "Documentación de OpenGL", "https://www.opengl.org/documentation/", 1, 1)
        create_link(tab_libs, "Documentación de SFML", "https://github.com/sfml/sfml", 2, 1)
        create_link(tab_libs, "Documentación de Flutter", "https://docs.flutter.dev/", 3, 1)

        # --- Ofimática ---
        tab_daily = self.tabview.tab("Ofimática")
        tab_daily.grid_columnconfigure((0,1), weight=1)
        
        # Columna 0
        create_link(tab_daily, "Documentación de Brave Browser", "https://brave.com/linux/", 0, 0)
        create_link(tab_daily, "Documentación de Firefox", "https://support.mozilla.org/es/products/firefox", 1, 0)
        create_link(tab_daily, "Documentación de LibreOffice", "https://documentation.libreoffice.org/es/", 2, 0)
        
        # Columna 1
        create_link(tab_daily, "Documentación de OBS Studio", "https://docs.obsproject.com/", 0, 1)
        create_link(tab_daily, "Documentación de VLC Media Player", "https://wiki.videolan.org/Documentation:Documentation/", 1, 1)
        create_link(tab_daily, "Documentación de JFLAP", "https://www.jflap.org/tutorial/", 2, 1)
        
        # --- Tutoriales ---
        tab_tutorials = self.tabview.tab("Tutoriales")
        tab_tutorials.grid_columnconfigure((0,1), weight=1)
        
        create_link(tab_tutorials, "Dual Boot Pop!_OS con Windows", "https://www.vojtechstruhar.com/blog/037-how-to-dualboot-popos-and-windows/", 0, 0)
        create_link(tab_tutorials, "Dual Boot Ubuntu con Windows", "https://help.ubuntu.com/community/WindowsDualBoot", 1, 0)
        create_link(tab_tutorials, "Dual Boot Linux Mint con Windows", "https://itsfoss.com/guide-install-linux-mint-16-dual-boot-windows/", 2, 0)
        create_link(tab_tutorials, "Dual Boot Fedora con Windows", "https://itsfoss.com/dual-boot-fedora-windows/", 3, 0)
        
        # Columna 1
        create_link(tab_tutorials, "Tutorial: Primeros Pasos en Git", "https://www.atlassian.com/es/git/tutorials", 0, 1)
        create_link(tab_tutorials, "Tutorial: Comandos de Terminal Linux", "https://ubuntu.com/tutorials/command-line-for-beginners", 1, 1)
        create_link(tab_tutorials, "Tutorial: Sintaxis de C", "https://www.w3schools.com/c/c_syntax.php", 2, 1)
        create_link(tab_tutorials, "Tutorial: GRUB THEMES", "https://github.com/jacksaur/Gorgeous-GRUB", 3, 1)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10, 20))
        
        self.btn_action = ctk.CTkButton(btn_frame, text="← Volver", command=lambda: self.controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#00FF00")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")
        self.btn_action.pack(side="left", padx=10)
