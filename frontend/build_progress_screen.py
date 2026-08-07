import customtkinter as ctk
import os
import sys
import subprocess
import threading
import glob
import time
import re
from custom_messagebox import msg_show_info, msg_show_error, msg_show_warning, msg_ask_yes_no
from utils import apply_glow_effect, get_project_root

class BuildProgressScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Construyendo Sistema_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))

        self.info_lbl = ctk.CTkLabel(self, text="", text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=16))
        self.info_lbl.grid(row=1, column=0, pady=(0, 20))
        
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, pady=(0, 20))
        
        self.status_lbl = ctk.CTkLabel(self.progress_frame, text="Estado: Iniciando...", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=14))
        self.status_lbl.pack(pady=(0, 10))
        
        self.lbl_download = ctk.CTkLabel(self.progress_frame, text="Descarga: 0%", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=12))
        self.lbl_download.pack(anchor="w")
        self.progress_bar_download = ctk.CTkProgressBar(self.progress_frame, mode="determinate", width=500, progress_color="#00FF00", fg_color="#002200")
        self.progress_bar_download.pack(pady=(0, 10))
        self.progress_bar_download.set(0)
        
        self.lbl_generation = ctk.CTkLabel(self.progress_frame, text="Generación: 0%", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=12))
        self.lbl_generation.pack(anchor="w")
        self.progress_bar_generation = ctk.CTkProgressBar(self.progress_frame, mode="determinate", width=500, progress_color="#00FF00", fg_color="#002200")
        self.progress_bar_generation.pack()
        self.progress_bar_generation.set(0)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(10, 20))
        
        self.btn_flash_usb = ctk.CTkButton(btn_frame, text="Montar en USB", command=lambda: self.controller.show_frame("UsbFlashScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="#004400", border_width=2, border_color="#00FF00",
                                   hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_flash_usb, default_text="Montar en USB", hover_text="Montar en USB")
        
        self.btn_action = ctk.CTkButton(btn_frame, text="Cancelar", command=self.cancel_process,
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#FF0000",
                                   hover_color="#330000", text_color="#FF0000")
        apply_glow_effect(self.btn_action, default_text="Cancelar", hover_text="Cancelar", color_base="#AA0000", color_glow="#FF0000")
        
        # Ocultar botones inicialmente, se empaquetan en on_show
        self.btn_action.pack(side="left", padx=10)
        
        self.current_process = None
        self.current_iso_target_dir = None
        self.is_cancelled = False
        
        self.target_download = 0.0
        self.current_download = 0.0
        self.is_animating_dl = False
        
        self.target_gen = 0.0
        self.current_gen = 0.0
        self.is_animating_gen = False

    def on_show(self):
        distro_seleccionada = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        self.info_lbl.configure(text=f"Preparando la construcción de: {distro_seleccionada}")
        self.status_lbl.configure(text="Estado: Iniciando motor de Docker...", text_color="#00FF00")
        
        self.is_cancelled = False
        self.btn_flash_usb.pack_forget()
        self.btn_action.configure(text="Cancelar", command=self.cancel_process, text_color="#FF0000", border_color="#FF0000", hover_color="#330000", state="normal")
        apply_glow_effect(self.btn_action, default_text="Cancelar", hover_text="Cancelar", color_base="#AA0000", color_glow="#FF0000")
        
        self.target_download = 0.0
        self.current_download = 0.0
        self.is_animating_dl = False
        self.target_gen = 0.0
        self.current_gen = 0.0
        self.is_animating_gen = False
        
        self.update_progress_download(0.0, "0,00")
        self.update_progress_generation(0.0, "0,00")
        self.ejecutar_script()

    def update_progress_download(self, val, text_val):
        if self.progress_bar_download.cget("mode") == "indeterminate":
            self.progress_bar_download.stop()
            self.progress_bar_download.configure(mode="determinate")
        self.target_download = val
        if not self.is_animating_dl:
            self.is_animating_dl = True
            self.animate_download()

    def update_progress_generation(self, val, text_val):
        if self.progress_bar_generation.cget("mode") == "indeterminate":
            self.progress_bar_generation.stop()
            self.progress_bar_generation.configure(mode="determinate")
        self.target_gen = val
        if not self.is_animating_gen:
            self.is_animating_gen = True
            self.animate_generation()

    def animate_download(self):
        if self.is_cancelled:
            self.is_animating_dl = False
            return
            
        step = 0.005 # 0.5% por frame
        if self.current_download < self.target_download:
            self.current_download += step
            if self.current_download > self.target_download:
                self.current_download = self.target_download
        elif self.current_download > self.target_download:
            self.current_download = self.target_download
            
        self.progress_bar_download.set(self.current_download)
        val = self.current_download * 100.0
        text_val = f"{val:.2f}".replace('.', ',')
        self.lbl_download.configure(text=f"Descarga: {text_val}%")
        
        if self.current_download < self.target_download:
            self.after(20, self.animate_download)
        else:
            self.is_animating_dl = False
            
    def animate_generation(self):
        if self.is_cancelled:
            self.is_animating_gen = False
            return
            
        step = 0.005
        if self.current_gen < self.target_gen:
            self.current_gen += step
            if self.current_gen > self.target_gen:
                self.current_gen = self.target_gen
        elif self.current_gen > self.target_gen:
            self.current_gen = self.target_gen
            
        self.progress_bar_generation.set(self.current_gen)
        val = self.current_gen * 100.0
        text_val = f"{val:.2f}".replace('.', ',')
        self.lbl_generation.configure(text=f"Generación: {text_val}%")
        
        if self.current_gen < self.target_gen:
            self.after(20, self.animate_generation)
        else:
            self.is_animating_gen = False

    def start_indeterminate_download(self):
        self.progress_bar_download.configure(mode="indeterminate")
        self.progress_bar_download.start()
        self.lbl_download.configure(text="Descarga: Conectando...")

    def start_indeterminate_generation(self):
        self.progress_bar_generation.configure(mode="indeterminate")
        self.progress_bar_generation.start()
        self.lbl_generation.configure(text="Generación: Procesando...")

    def set_btn_volver(self):
        self.btn_action.configure(text="← Volver", command=lambda: self.controller.show_frame("DistroInfoScreen"), 
                                  text_color="#008800", border_color="#008800", hover_color="#001100", state="normal")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")

    def cancel_process(self):
        self.is_cancelled = True
        self.btn_action.configure(state="disabled")
        self.status_lbl.configure(text="Estado: Cancelando proceso y limpiando...", text_color="#FF0000")
        
        if self.current_process:
            try:
                self.current_process.kill()
            except Exception:
                pass
            
            try:
                cflags = 0x08000000 if sys.platform == "win32" else 0
                subprocess.run('wsl --cd ~ -u root -e pkill -f "build_iso.sh|download_iso.sh"', shell=True, creationflags=cflags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
                
        if self.current_iso_target_dir:
            try:
                time.sleep(0.5)
                isos = glob.glob(os.path.join(self.current_iso_target_dir, "*.iso"))
                for iso in isos:
                    os.remove(iso)
            except Exception:
                pass
                
        self.status_lbl.configure(text="Estado: Proceso cancelado.")
        self.set_btn_volver()

    def check_and_delete_iso(self, directory, name_desc, distro_env, ask_confirmation=True):
        isos = glob.glob(os.path.join(directory, "*.iso"))
        if isos:
            iso_file = isos[0]
            iso_name = os.path.basename(iso_file)
            
            if ask_confirmation:
                msg = f"Se encontró una ISO {name_desc} existente: '{iso_name}'.\n\n¿Desea eliminarla y generarla de nuevo?\n\n• 'Sí' para reconstruir.\n• 'No' para reusar la existente."
                should_delete = msg_ask_yes_no("ISO Detectada", msg)
            else:
                should_delete = True
                
            if should_delete:
                try:
                    os.remove(iso_file)
                    print(f"Eliminado: {iso_file}")
                    return True
                except Exception as e:
                    if ask_confirmation:
                        msg_show_warning("Advertencia", f"No se pudo eliminar el archivo:\n{e}")
                    return True
            else:
                return False
        return True

    def ejecutar_script(self):
        # 1. Verificar si WSL está disponible
        try:
            cflags = 0x08000000 if sys.platform == "win32" else 0
            res = subprocess.run(["wsl", "--status"], capture_output=True, text=True, creationflags=cflags)
            if res.returncode != 0:
                raise Exception("WSL no instalado")
        except Exception:
            msg_show_error(
                "WSL Requerido", 
                "El Subsistema de Windows para Linux (WSL) no está instalado o no se detecta correctamente.\n\n"
                "Por favor, vuelve al menú de Opciones y utiliza la herramienta 'Instalar WSL'."
            )
            self.status_lbl.configure(text="Estado: Error de dependencia (WSL).", text_color="#FF0000")
            self.set_btn_volver()
            return

        # Limpieza proactiva de procesos huérfanos de WSL
        try:
            subprocess.run('wsl --cd ~ -u root -e pkill -f "build_iso.sh|download_iso.sh"', shell=True, creationflags=cflags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

        distro_seleccionada = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        
        distro_map = {
            "Ubuntu": "ubuntu",
            "Linux Mint": "mint",
            "Fedora": "fedora",
            "Pop!_OS": "popos"
        }
        
        distro_env = distro_map.get(distro_seleccionada, "ubuntu")
        
        if distro_seleccionada == "Pop!_OS":
            respuesta = msg_ask_yes_no(
                "Versión de Pop!_OS", 
                "¿Tienes una tarjeta gráfica NVIDIA en tu equipo?\n\n"
                "• Selecciona 'Sí' para usar la ISO con drivers NVIDIA preinstalados.\n"
                "• Selecciona 'No' para usar la ISO estándar (Intel/AMD)."
            )
            if respuesta:
                distro_env = "popos_nvidia"
            else:
                distro_env = "popos_amd"
                
        project_root = get_project_root()
        
        # Check oficial ISO
        download_dir = os.path.join(project_root, "downloads", "iso", distro_env)
        os.makedirs(download_dir, exist_ok=True)
        self.check_and_delete_iso(download_dir, "oficial descargada", distro_env)
        
        # Iniciar hilo de Docker para descarga
        self.current_iso_target_dir = download_dir
        threading.Thread(target=self.run_download_thread, args=(project_root, distro_env, distro_seleccionada), daemon=True).start()

    def run_download_thread(self, project_root, distro_env, distro_seleccionada):
        self.after(0, self.start_indeterminate_download)
        
        try:
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            
            # Instalar dependencias en WSL (reemplaza a docker build)
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Instalando dependencias de Linux en WSL..."))
            wsl_deps_cmd = 'wsl --cd ~ -u root -e bash -c "apt-get update && apt-get install -y xorriso squashfs-tools e2fsprogs mtools dosfstools p7zip-full wget curl aria2 syslinux-utils isolinux coreutils"'
            subprocess.run(wsl_deps_cmd, shell=True, creationflags=creationflags, check=False)
            
            def to_wsl_path(win_path):
                drive, rest = os.path.splitdrive(win_path)
                return f"/mnt/{drive[0].lower()}{rest.replace(os.sep, '/')}"
                
            wsl_project_root = to_wsl_path(project_root)
            drive_letter = os.path.splitdrive(project_root)[0][0].lower()
            
            mount_logic = f'if [ ! -d /mnt/{drive_letter} ]; then mkdir -p /mnt/{drive_letter}; fi; if ! mountpoint -q /mnt/{drive_letter}; then mount -t drvfs {drive_letter.upper()}: /mnt/{drive_letter}; fi; '
            
            # Ejecutar run de la descarga usando WSL en vez de docker
            cmd = f'wsl --cd ~ -u root -e bash -c "{mount_logic}export ISO_DISTRO=\\"{distro_env}\\"; sed -i \\"s/\\\\r\\$//\\" {wsl_project_root}/builder/download_iso.sh 2>/dev/null; cd {wsl_project_root} && bash {wsl_project_root}/builder/download_iso.sh \\"{distro_env}\\""'
            
            self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=creationflags, bufsize=1, universal_newlines=True)
            
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Descargando imagen oficial de la ISO..."))
            
            last_lines = []
            for line in iter(self.current_process.stdout.readline, ''):
                if not line or self.is_cancelled:
                    break
                
                last_lines.append(line.strip())
                if len(last_lines) > 5:
                    last_lines.pop(0)
                    
                percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                if percent_match:
                    percent_val = float(percent_match.group(1)) / 100.0
                    val = float(percent_match.group(1))
                    text_val = f"{val:.2f}".replace('.', ',')
                    self.after(0, self.update_progress_download, percent_val, text_val)
                    
            self.current_process.stdout.close()
            self.current_process.wait()
            
            if self.is_cancelled:
                return
            
            if self.current_process.returncode == 0:
                self.after(0, self.update_progress_download, 1.0, "100,00")
                self.after(0, self.check_output_iso_and_build, project_root, distro_env, distro_seleccionada)
            else:
                error_details = "\n".join(last_lines)
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error en la descarga.", text_color="#FF0000"))
                self.after(0, lambda err=error_details: msg_show_error("Error", f"Ocurrió un error durante la descarga de la ISO.\nDetalles:\n{err}"))
                self.after(0, self.set_btn_volver)
                
        except Exception as e:
            if not self.is_cancelled:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda: msg_show_error("Error", str(e)))
                self.after(0, self.set_btn_volver)

    def check_output_iso_and_build(self, project_root, distro_env, distro_seleccionada):
        if self.is_cancelled:
            return
        output_dir = os.path.join(project_root, "output", distro_env)
        os.makedirs(output_dir, exist_ok=True)
        should_build = self.check_and_delete_iso(output_dir, "modificada final", distro_env, ask_confirmation=True)
        
        self.current_iso_target_dir = output_dir
        if not self.is_cancelled:
            if should_build:
                threading.Thread(target=self.run_build_thread, args=(project_root, distro_env, distro_seleccionada), daemon=True).start()
            else:
                self.after(0, self.update_progress_generation, 1.0, "100,00")
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Usando ISO generada previamente.", text_color="#00FF00"))
                self.after(0, lambda: self.btn_flash_usb.pack(side="left", padx=10))
                self.after(0, self.set_btn_volver)

    def run_build_thread(self, project_root, distro_env, distro_seleccionada):
        self.after(0, self.start_indeterminate_generation)
        current_phase = "processing"
        
        try:
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            
            def to_wsl_path(win_path):
                drive, rest = os.path.splitdrive(win_path)
                return f"/mnt/{drive[0].lower()}{rest.replace(os.sep, '/')}"
                
            wsl_project_root = to_wsl_path(project_root)
            drive_letter = os.path.splitdrive(project_root)[0][0].lower()
            
            mount_logic = f'if [ ! -d /mnt/{drive_letter} ]; then mkdir -p /mnt/{drive_letter}; fi; if ! mountpoint -q /mnt/{drive_letter}; then mount -t drvfs {drive_letter.upper()}: /mnt/{drive_letter}; fi; '
            
            custom_iso_name = f"{distro_seleccionada} custom by Stack"
            cmd = f'wsl --cd ~ -u root -e bash -c "{mount_logic}export ISO_DISTRO=\\"{distro_env}\\"; export CUSTOM_ISO_NAME=\\"{custom_iso_name}\\"; sed -i \\"s/\\\\r\\$//\\" {wsl_project_root}/builder/build_iso.sh 2>/dev/null; cd {wsl_project_root} && bash {wsl_project_root}/builder/build_iso.sh"'
            
            self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=creationflags, bufsize=1, universal_newlines=True)
            
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Modificando e inyectando código en la ISO..."))
            self.after(0, self.update_progress_download, 1.0, "100,00")
            
            current_subphase = "generating"
            base_percent = 0.0
            scale_percent = 1.0
            
            last_lines = []
            char_buffer = []
            
            while True:
                if self.is_cancelled:
                    break
                
                char = self.current_process.stdout.read(1)
                if not char:
                    break
                
                if char == '\r' or char == '\n':
                    line = ''.join(char_buffer).strip()
                    char_buffer = []
                    
                    if not line:
                        continue
                    
                    last_lines.append(line)
                    if len(last_lines) > 5:
                        last_lines.pop(0)
                        
                    line_lower = line.lower()
                    
                    if "desempaquetando squashfs" in line_lower:
                        current_phase = "generating"
                        current_subphase = "unpacking"
                        base_percent = 0.0
                        scale_percent = 0.25
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Desempaquetando sistema de archivos base (1/3)..."))
                    elif "reempaquetando squashfs" in line_lower:
                        current_phase = "generating"
                        current_subphase = "repacking"
                        base_percent = 0.25
                        scale_percent = 0.50
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Comprimiendo nuevo sistema de archivos (2/3)..."))
                    elif "generando nueva iso" in line_lower:
                        current_phase = "generating"
                        current_subphase = "generating"
                        if "pop" in distro_env.lower():
                            base_percent = 0.75
                            scale_percent = 0.25
                            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Empaquetando y exportando ISO final (3/3)..."))
                        else:
                            base_percent = 0.0
                            scale_percent = 1.0
                            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Empaquetando y exportando ISO final..."))
                            
                    percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                    if percent_match:
                        raw_percent = float(percent_match.group(1)) / 100.0
                        actual_percent = base_percent + (raw_percent * scale_percent)
                        val = actual_percent * 100.0
                        text_val = f"{val:.2f}".replace('.', ',')
                        if current_phase == "generating":
                            self.after(0, self.update_progress_generation, actual_percent, text_val)
                            
                    if "fatal_error" in line_lower or line_lower.startswith("[fatal_error]"):
                        # El script de WSL reportó un error crítico — mostrarlo de inmediato
                        error_details = line
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error crítico en el proceso.", text_color="#FF0000"))
                        self.after(0, lambda err=error_details: msg_show_error(
                            "Error crítico",
                            f"El proceso de construcción falló en un paso crítico:\n\n{err}\n\n"
                            "Revisa que la ISO descargada no esté corrupta e inténtalo de nuevo."
                        ))
                        self.after(0, self.set_btn_volver)
                        return
                    elif "exitosa" in line_lower:
                        current_phase = "done"
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: ¡ISO finalizada con éxito!"))
                        self.after(0, self.update_progress_generation, 1.0, "100,00")
                else:
                    char_buffer.append(char)
                    
            self.current_process.stdout.close()
            self.current_process.wait()
            
            if self.is_cancelled:
                return
            
            if self.current_process.returncode == 0:
                self.after(0, self.update_progress_generation, 1.0, "100,00")
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Sistema Construido Exitosamente.", text_color="#00FF00"))
                
                def on_success_actions():
                    msg_show_info("Éxito", f"¡La imagen de {distro_seleccionada} se ha construido correctamente!\nYa puedes usarla para flashear una USB o instalarla en una máquina virtual. \nTu imagen se encuentra en la carpeta output")
                    self.btn_flash_usb.pack(side="left", padx=10)
                    
                    if msg_ask_yes_no("Ahorrar Espacio", "¿Deseas eliminar la ISO oficial descargada para ahorrar espacio en tu disco duro?\n\nTu imagen personalizada recién creada NO se borrará y se mantendrá segura en la carpeta 'output'."):
                        try:
                            import glob
                            import os
                            isos = glob.glob(os.path.join(self.current_iso_target_dir, "*.iso"))
                            for iso in isos:
                                os.remove(iso)
                        except Exception:
                            pass
                            
                self.after(0, on_success_actions)
            else:
                self.after(0, self.update_progress_generation, 0.0, "0,00")
                error_details = "\n".join(last_lines)
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error en la construcción.", text_color="#FF0000"))
                self.after(0, lambda err=error_details: msg_show_error("Error", f"Ocurrió un error durante la construcción de la ISO.\nDetalles:\n{err}"))

                
        except Exception as e:
            if not self.is_cancelled:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda: msg_show_error("Error", str(e)))
            
        finally:
            if not self.is_cancelled:
                self.after(0, self.set_btn_volver)
