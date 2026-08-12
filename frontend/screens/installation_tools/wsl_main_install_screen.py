import customtkinter as ctk
import subprocess
import threading
import sys
import time
from custom_messagebox import msg_show_info, msg_show_error, msg_ask_yes_no
from utils import apply_glow_effect

class WslMainInstallScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=20)
        
        self.title_lbl = ctk.CTkLabel(header_frame, text="> Gestor Principal de WSL_", 
                                      font=ctk.CTkFont(family="Consolas", size=32, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.pack(side="left")
        
        self.btn_home = ctk.CTkButton(header_frame, text="← Volver", command=self.go_home,
                                   height=35, width=120, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=14, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_home, default_text="← Volver", hover_text="← Volver")
        self.btn_home.pack(side="right")
        
        # Tabview
        self.tabview = ctk.CTkTabview(self, fg_color="#051505", segmented_button_fg_color="#002200",
                                      segmented_button_selected_color="#004400",
                                      segmented_button_selected_hover_color="#005500",
                                      segmented_button_unselected_color="#001100",
                                      segmented_button_unselected_hover_color="#003300",
                                      text_color="#00FF00")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        self.tab_status = self.tabview.add("Estado del Sistema")
        self.tab_distros = self.tabview.add("Gestión de Distribuciones")
        
        self.setup_status_tab()
        self.setup_distros_tab()
        
    def setup_status_tab(self):
        self.tab_status.grid_columnconfigure(0, weight=1)
        
        self.status_container = ctk.CTkFrame(self.tab_status, fg_color="#001100", corner_radius=10)
        self.status_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(self.status_container, text="Análisis del Entorno WSL", font=ctk.CTkFont(family="Consolas", size=20, weight="bold"), text_color="#00FF00")
        title.pack(pady=(20, 10))
        
        self.status_labels = {}
        fields = [
            ("wsl_installed", "WSL"),
            ("wsl2_available", "WSL 2"),
            ("vm_platform", "Virtual Machine"),
            ("virt_enabled", "Virtualización"),
            ("default_version", "Versión predeterminada"),
            ("default_distro", "Distribución predeterminada")
        ]
        
        for key, text in fields:
            row_frame = ctk.CTkFrame(self.status_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=60, pady=5)
            
            lbl_name = ctk.CTkLabel(row_frame, text=text, font=ctk.CTkFont(family="Consolas", size=16), text_color="#00E676", width=280, anchor="w")
            lbl_name.pack(side="left")
            
            lbl_val = ctk.CTkLabel(row_frame, text="Buscando...", font=ctk.CTkFont(family="Consolas", size=16, weight="bold"), text_color="#AAAAAA")
            lbl_val.pack(side="left")
            
            self.status_labels[key] = lbl_val
            
        self.btn_fix_wsl = ctk.CTkButton(self.status_container, text="Habilitar / Instalar WSL", command=self.install_wsl,
                                         height=45, width=280, fg_color="#004400", hover_color="#007700", border_color="#00FF00", border_width=2, text_color="#FFFFFF", font=ctk.CTkFont(family="Consolas", size=16, weight="bold"), state="disabled")
        self.btn_fix_wsl.pack(pady=(30, 10))
        apply_glow_effect(self.btn_fix_wsl, default_text="Habilitar / Instalar WSL", hover_text="Habilitar / Instalar WSL")
        
        self.install_wsl_status_lbl = ctk.CTkLabel(self.status_container, text="", font=ctk.CTkFont(family="Consolas", size=14, weight="bold"), text_color="#FFAA00")
        self.install_wsl_status_lbl.pack(pady=(0, 5))
        
        self.install_wsl_progress = ctk.CTkProgressBar(self.status_container, mode="indeterminate", width=280, progress_color="#00FF00", fg_color="#002200")
        # Not packed initially

    def setup_distros_tab(self):
        # Dos paneles: Izquierda (lista), Derecha (Progreso/Config)
        self.split_frame = ctk.CTkFrame(self.tab_distros, fg_color="transparent")
        self.split_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.split_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.split_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.split_frame.grid_rowconfigure(0, weight=1)
        
        # Panel Izquierdo: Lista de Distros
        self.list_panel = ctk.CTkFrame(self.split_frame, fg_color="#001100", corner_radius=10)
        self.list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        title_list = ctk.CTkLabel(self.list_panel, text="Distribuciones Disponibles", font=ctk.CTkFont(family="Consolas", size=18, weight="bold"), text_color="#00FF00")
        title_list.pack(pady=(15, 10))
        
        self.scroll_distros = ctk.CTkScrollableFrame(self.list_panel, fg_color="transparent")
        self.scroll_distros.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.btn_install_selected = ctk.CTkButton(self.list_panel, text="Instalar Seleccionadas", command=self.start_install,
                                                  height=45, fg_color="#004400", hover_color="#007700", border_color="#00FF00", border_width=2, text_color="#FFFFFF", font=ctk.CTkFont(family="Consolas", size=15, weight="bold"))
        self.btn_install_selected.pack(pady=15, padx=20, fill="x")
        
        # Panel Derecho: Instalación / Configuración
        self.config_panel = ctk.CTkFrame(self.split_frame, fg_color="#001100", corner_radius=10)
        self.config_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        title_cfg = ctk.CTkLabel(self.config_panel, text="Progreso y Configuración", font=ctk.CTkFont(family="Consolas", size=18, weight="bold"), text_color="#00FF00")
        title_cfg.pack(pady=(15, 10))
        
        self.scroll_progress = ctk.CTkScrollableFrame(self.config_panel, fg_color="transparent")
        self.scroll_progress.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Dictionaries to keep track
        self.distro_vars = {} 
        self.installed_distros = {}
        
    def on_show(self):
        self.load_wsl_status()
        self.load_distros()

    def go_home(self):
        self.controller.show_frame("WslInstallScreen")
        
    def load_wsl_status(self):
        threading.Thread(target=self._worker_load_status, daemon=True).start()

    def _worker_load_status(self):
        is_win = sys.platform == "win32"
        
        wsl_installed = False
        wsl2_avail = False
        default_version = "Desconocida"
        default_distro = "Ninguna"
        
        if is_win:
            try:
                res = subprocess.run(["wsl", "--status"], capture_output=True, text=True, creationflags=0x08000000)
                if res.returncode == 0:
                    wsl_installed = True
                    out = res.stdout.replace('\x00', '')
                    if "WSL 2" in out or "Versión predeterminada: 2" in out or "Default Version: 2" in out:
                        wsl2_avail = True
                        default_version = "WSL 2"
                    elif "Versión predeterminada: 1" in out or "Default Version: 1" in out:
                        default_version = "WSL 1"
                    
                res_l = subprocess.run(["wsl", "-l", "-v"], capture_output=True, text=True, creationflags=0x08000000)
                if res_l.returncode == 0:
                    lines = res_l.stdout.split('\n')
                    for line in lines:
                        if "*" in line:
                            parts = line.replace("*", "").replace('\x00', '').strip().split()
                            if parts:
                                default_distro = parts[0]
            except:
                pass
        else:
            wsl_installed = True
            wsl2_avail = True
            default_version = "WSL 2"
            default_distro = "Ubuntu"
            
        def update_ui():
            self.update_status_label("wsl_installed", "✓ Instalado" if wsl_installed else "✗ No instalado", "#00FF00" if wsl_installed else "#FF0000")
            self.update_status_label("wsl2_available", "✓ Disponible" if wsl2_avail else "✗ No disponible", "#00FF00" if wsl2_avail else "#FFAA00")
            self.update_status_label("vm_platform", "✓ Habilitado" if wsl_installed else "? Desconocido", "#00FF00" if wsl_installed else "#AAAAAA")
            self.update_status_label("virt_enabled", "✓ Habilitada" if wsl_installed else "? Desconocida", "#00FF00" if wsl_installed else "#AAAAAA")
            self.update_status_label("default_version", default_version, "#00E676")
            self.update_status_label("default_distro", default_distro, "#00E676")
            
            if not wsl_installed:
                self.btn_fix_wsl.configure(state="normal")
            else:
                self.btn_fix_wsl.configure(state="disabled", fg_color="#002200", text="WSL ya está habilitado", text_color="#008800")
                self.install_wsl_status_lbl.configure(text="")
                self.install_wsl_progress.pack_forget()
            
        self.after(0, update_ui)
        
    def update_status_label(self, key, text, color):
        if key in self.status_labels:
            self.status_labels[key].configure(text=text, text_color=color)
            
    def load_distros(self):
        for widget in self.scroll_distros.winfo_children():
            widget.destroy()
        
        lbl_loading = ctk.CTkLabel(self.scroll_distros, text="Cargando distribuciones...", text_color="#00FF00", font=ctk.CTkFont(family="Consolas", size=14))
        lbl_loading.pack(pady=20)
        
        threading.Thread(target=self._worker_load_distros, daemon=True).start()
        
    def _worker_load_distros(self):
        is_win = sys.platform == "win32"
        
        fallback_distros = [
            "Ubuntu", "Debian", "Kali Linux", "Arch Linux", "openSUSE",
            "Oracle Linux", "Fedora", "AlmaLinux", "Rocky Linux", "SLES"
        ]
        
        available_distros = []
        installed_distros = {}
        
        if is_win:
            try:
                # 1. Obtener distribuciones instaladas (wsl -l -v)
                res = subprocess.run(["wsl", "-l", "-v"], capture_output=True, text=True, creationflags=0x08000000)
                if res.returncode == 0:
                    lines = res.stdout.split('\n')[1:] # Saltar cabecera
                    for line in lines:
                        line = line.replace('\x00', '').strip()
                        if line:
                            parts = line.replace('*', '').strip().split()
                            if len(parts) >= 2:
                                name = parts[0]
                                state = parts[1]
                                installed_distros[name] = state
                                
                # 2. Obtener distribuciones online (wsl -l -o)
                res_o = subprocess.run(["wsl", "-l", "-o"], capture_output=True, text=True, creationflags=0x08000000)
                if res_o.returncode == 0:
                    lines = res_o.stdout.split('\n')
                    start_parsing = False
                    for line in lines:
                        line = line.replace('\x00', '').strip()
                        if not line:
                            continue
                        if line.startswith("NAME"):
                            start_parsing = True
                            continue
                        if start_parsing:
                            parts = line.split()
                            if parts:
                                available_distros.append(parts[0])
            except Exception as e:
                pass
                
            if not available_distros:
                available_distros = fallback_distros
        else:
            installed_distros = {"Ubuntu": "Running", "Debian": "Stopped"}
            available_distros = fallback_distros
            
        def update_ui():
            for widget in self.scroll_distros.winfo_children():
                widget.destroy()
                
            self.distro_vars.clear()
            self.installed_distros = installed_distros
            
            # Combinar listas para mostrar todo correctamente
            all_distros = sorted(list(set(available_distros + list(installed_distros.keys()))))
            
            for distro in all_distros:
                frame = ctk.CTkFrame(self.scroll_distros, fg_color="#002200", corner_radius=5)
                frame.pack(fill="x", pady=5)
                
                if distro in installed_distros:
                    state = installed_distros[distro]
                    lbl = ctk.CTkLabel(frame, text=f"{distro}", font=ctk.CTkFont(family="Consolas", size=14, weight="bold"), text_color="#00FF00")
                    lbl.pack(side="left", padx=10, pady=10)
                    
                    status_color = "#00FF00" if state.lower() == "running" else "#AAAAAA"
                    lbl_status = ctk.CTkLabel(frame, text=f"✓ Instalada ({state})", font=ctk.CTkFont(family="Consolas", size=12), text_color=status_color)
                    lbl_status.pack(side="right", padx=10, pady=10)
                else:
                    var = ctk.BooleanVar(value=False)
                    self.distro_vars[distro] = var
                    chk = ctk.CTkCheckBox(frame, text=distro, variable=var, font=ctk.CTkFont(family="Consolas", size=14), 
                                          text_color="#FFFFFF", fg_color="#00AA00", hover_color="#00FF00", border_color="#00FF00")
                    chk.pack(side="left", padx=10, pady=10)
                    
        self.after(0, update_ui)

    def install_wsl(self):
        msg_show_info(
            "Habilitar WSL", 
            "El sistema intentará habilitar WSL e instalará los componentes básicos.\n\n"
            "Se requerirán permisos de Administrador y podría ser necesario un reinicio del equipo al finalizar."
        )
        self.btn_fix_wsl.configure(state="disabled", text="Instalando...")
        self.install_wsl_status_lbl.configure(text="Habilitando WSL, por favor espera... (Puede tardar varios minutos)", text_color="#FFAA00")
        self.install_wsl_progress.pack(pady=(0, 20))
        self.install_wsl_progress.start()
        
        def worker():
            try:
                cflags = 0x08000000 if sys.platform == "win32" else 0
                ps_cmd = 'Start-Process powershell -ArgumentList "-WindowStyle", "Hidden", "-Command", "wsl --install --no-distribution; exit" -Verb RunAs -Wait'
                res = subprocess.run(['powershell', '-Command', ps_cmd], creationflags=cflags)
                
                if res.returncode == 0:
                    self.after(0, lambda: self.install_wsl_status_lbl.configure(text="¡Instalación exitosa! Requiere reinicio.", text_color="#00FF00"))
                    self.after(0, lambda: msg_show_info("WSL Habilitado", "La instalación de WSL base fue exitosa. DEBES REINICIAR el sistema para aplicar los cambios antes de instalar distribuciones."))
                else:
                    self.after(0, lambda: self.install_wsl_status_lbl.configure(text="Error al habilitar WSL.", text_color="#FF0000"))
                    self.after(0, lambda: msg_show_error("Error", "No se pudo habilitar WSL. Revisa los permisos."))
            except Exception as e:
                self.after(0, lambda: self.install_wsl_status_lbl.configure(text="Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda e=e: msg_show_error("Error", str(e)))
            finally:
                self.after(0, self.install_wsl_progress.stop)
                self.after(0, self.load_wsl_status)
                
        threading.Thread(target=worker, daemon=True).start()

    def start_install(self):
        selected = [d for d, var in self.distro_vars.items() if var.get()]
        if not selected:
            msg_show_error("Selección vacía", "Por favor, selecciona al menos una distribución disponible para instalar.")
            return
            
        distros_str = "\n".join([f"- {d}" for d in selected])
        confirm = msg_ask_yes_no(
            "Confirmar Instalación",
            f"¿Estás seguro de que deseas instalar las siguientes distribuciones?\n\n{distros_str}\n\nEsto puede tardar varios minutos y requerirá descargar datos de internet."
        )
        if not confirm:
            return
            
        for widget in self.scroll_progress.winfo_children():
            widget.destroy()
            
        for distro in selected:
            self.create_progress_card(distro)
            
        # Deshabilitar botones mientras se instala
        self.btn_install_selected.configure(state="disabled")
        for var in self.distro_vars.values():
            var.set(False)
            
        threading.Thread(target=self._worker_install_distros, args=(selected,), daemon=True).start()
        
    def _worker_install_distros(self, distros):
        is_win = sys.platform == "win32"
        
        for distro in distros:
            self.after(0, lambda d=distro: self.update_progress(d, status="⟳ Instalando...", percentage=0.2, color="#FFAA00"))
            
            success = False
            try:
                if is_win:
                    # wsl --install -d <Distro> abre una consola interactiva si no se pre-configura.
                    # Al correrlo con Start-Process, abrirá la ventana de PS para que el usuario escriba su credencial.
                    # Como alternativa "no-launch" evita la consola, pero luego hay que configurarlo.
                    # El usuario pidió configurar desde la GUI, así que usaremos --no-launch.
                    cflags = 0x08000000
                    ps_cmd = f'Start-Process powershell -ArgumentList "-WindowStyle", "Hidden", "-Command", "wsl --install -d {distro} --no-launch; exit" -Verb RunAs -Wait'
                    res = subprocess.run(['powershell', '-Command', ps_cmd], creationflags=cflags)
                    if res.returncode == 0:
                        success = True
                else:
                    time.sleep(2) # Simulación
                    success = True
                    
            except Exception as e:
                pass
                
            if success:
                self.after(0, lambda d=distro: self.update_progress(d, status="✓ Instalada", percentage=1.0, color="#00FF00", show_form=False))
                self.after(0, lambda d=distro: msg_show_info("Instalación Completa", f"La distribución {d} ha sido instalada.\n\nSi no se abrió automáticamente, ábrela desde el Menú de Inicio o con el comando: wsl en el CMD, ahí podrás configurar tu usuario y contraseña."))
            else:
                self.after(0, lambda d=distro: self.update_progress(d, status="✗ Error de instalación", percentage=0.0, color="#FF0000"))
                
        self.after(0, lambda: self.btn_install_selected.configure(state="normal"))
        self.after(0, self.load_distros)
            
    def create_progress_card(self, distro):
        from utils import ProgressManager
        card = ctk.CTkFrame(self.scroll_progress, fg_color="#002200", corner_radius=8)
        card.pack(fill="x", pady=5)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        lbl_name = ctk.CTkLabel(header, text=distro, font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), text_color="#00FF00")
        lbl_name.pack(side="left")
        
        lbl_status = ctk.CTkLabel(header, text="○ En espera", font=ctk.CTkFont(family="Consolas", size=12), text_color="#AAAAAA")
        lbl_status.pack(side="right")
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent", height=15)
        info_frame.pack(fill="x", padx=10, pady=(0, 2))
        
        lbl_perc = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(family="Consolas", size=11), text_color="#00FF00")
        lbl_perc.pack(side="left")
        
        lbl_eta = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(family="Consolas", size=11), text_color="#AAAAAA")
        lbl_eta.pack(side="right")
        
        prog = ctk.CTkProgressBar(card, progress_color="#00FF00", fg_color="#001100")
        prog.pack(fill="x", padx=10, pady=(0, 10))
        prog.set(0)
        
        mgr = ProgressManager(self, prog, lbl_perc, "Progreso: ", eta_label=lbl_eta)
        mgr.reset()
        
        card.pack_info = {"lbl_status": lbl_status, "prog": prog, "mgr": mgr}
        setattr(self, f"card_{distro.replace(' ', '_')}", card)
        
    def update_progress(self, distro, status, percentage, color, show_form=False):
        card = getattr(self, f"card_{distro.replace(' ', '_')}", None)
        if card:
            card.pack_info["lbl_status"].configure(text=status, text_color=color)
            mgr = card.pack_info["mgr"]
            if percentage >= 1.0:
                mgr.disable_simulation()
                mgr.update_progress(1.0)
            elif percentage == 0.0:
                mgr.reset()
            else:
                mgr.enable_simulation(cap=0.95, rate=0.0001)
            card.pack_info["prog"].configure(progress_color=color)


