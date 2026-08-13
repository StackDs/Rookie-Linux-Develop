import customtkinter as ctk
import os
import sys
import subprocess
import threading
import glob
import time
import re
from custom_messagebox import msg_show_info, msg_show_error, msg_show_warning, msg_ask_yes_no
from utils import apply_glow_effect, get_project_root, ProgressManager

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
        
        lbl_frame_dl = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        lbl_frame_dl.pack(fill="x")
        
        self.lbl_download = ctk.CTkLabel(lbl_frame_dl, text="Descarga: 0%", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=12))
        self.lbl_download.pack(side="left")
        self.eta_lbl_download = ctk.CTkLabel(lbl_frame_dl, text="", text_color="#006600", font=ctk.CTkFont(family="Consolas", size=12))
        self.eta_lbl_download.pack(side="right")
        
        self.progress_bar_download = ctk.CTkProgressBar(self.progress_frame, mode="determinate", width=500, progress_color="#00FF00", fg_color="#002200")
        self.progress_bar_download.pack(pady=(0, 10))
        self.progress_bar_download.set(0)
        
        lbl_frame_gen = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        lbl_frame_gen.pack(fill="x")
        
        self.lbl_generation = ctk.CTkLabel(lbl_frame_gen, text="Generación: 0%", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=12))
        self.lbl_generation.pack(side="left")
        self.eta_lbl_generation = ctk.CTkLabel(lbl_frame_gen, text="", text_color="#006600", font=ctk.CTkFont(family="Consolas", size=12))
        self.eta_lbl_generation.pack(side="right")
        
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
        self.is_building = False
        
        self.prog_mgr_dl = ProgressManager(self, self.progress_bar_download, self.lbl_download, "Descarga: ", eta_label=self.eta_lbl_download)
        self.prog_mgr_gen = ProgressManager(self, self.progress_bar_generation, self.lbl_generation, "Generación: ", eta_label=self.eta_lbl_generation)

    def on_show(self):
        distro_seleccionada = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        self.info_lbl.configure(text=f"Preparando la construcción de: {distro_seleccionada}")
        self.status_lbl.configure(text="Estado: Iniciando motor de Docker...", text_color="#00FF00")
        
        self.is_cancelled = False
        self.is_building = True
        self.btn_flash_usb.pack_forget()
        self.btn_action.configure(text="Cancelar", command=self.cancel_process, text_color="#FF0000", border_color="#FF0000", hover_color="#330000", state="normal")
        apply_glow_effect(self.btn_action, default_text="Cancelar", hover_text="Cancelar", color_base="#AA0000", color_glow="#FF0000")
        
        self.prog_mgr_dl.reset()
        self.prog_mgr_gen.reset()
        self.ejecutar_script()

    def update_progress_download(self, val, text_val):
        self.prog_mgr_dl.set_determinate()
        self.prog_mgr_dl.update_progress(val)

    def update_progress_generation(self, val, text_val):
        self.prog_mgr_gen.set_determinate()
        self.prog_mgr_gen.update_progress(val)

    def start_indeterminate_download(self):
        self.prog_mgr_dl.set_indeterminate("Descarga: Conectando...")

    def start_indeterminate_generation(self):
        self.prog_mgr_gen.set_determinate()
        self.prog_mgr_gen.enable_simulation(cap=0.99, rate=0.00015) # Sube ~7.5% por minuto si no hay datos

    def set_btn_volver(self):
        self.btn_action.configure(text="← Volver", command=lambda: self.controller.show_frame("DistroInfoScreen"), 
                                  text_color="#008800", border_color="#008800", hover_color="#001100", state="normal")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")

    def cancel_process(self, ask_confirm=True):
        if ask_confirm and not self.is_cancelled:
            if not msg_ask_yes_no("Confirmar", "¿Estás seguro de que deseas cancelar la construcción actual?"):
                return
                
        self.is_cancelled = True
        self.is_building = False
        self.btn_action.configure(state="disabled")
        self.prog_mgr_gen.disable_simulation()
        self.prog_mgr_dl.disable_simulation()
        self.status_lbl.configure(text="Estado: Cancelando proceso y limpiando...", text_color="#FF0000")
        
        if self.current_process:
            try:
                self.current_process.kill()
            except Exception:
                pass
            
            try:
                if sys.platform == "win32":
                    subprocess.run('wsl --cd ~ -u root -e pkill -f "build_iso.sh|download_iso.sh"', shell=True, creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run('pkill -f "build_iso.sh|download_iso.sh"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        # 1. Verificar si WSL está disponible y funcional (Solo Windows)
        if sys.platform == "win32":
            try:
                # Ejecutar un comando bash simple para asegurar que WSL y una distro están instalados
                res = subprocess.run(["wsl", "-e", "bash", "-c", "echo wsl_ok"], capture_output=True, text=True, creationflags=0x08000000)
                if res.returncode != 0 or "wsl_ok" not in res.stdout:
                    raise Exception("WSL no instalado o sin distribución válida")
            except Exception:
                msg_show_error(
                    "WSL Requerido", 
                    "El Subsistema de Windows para Linux (WSL) no está habilitado o no hay una distribución instalada correctamente.\n\n"
                    "Por favor, vuelve al menú de Opciones y utiliza la herramienta 'Instalar WSL'."
                )
                self.status_lbl.configure(text="Estado: Error de dependencia (WSL).", text_color="#FF0000")
                self.set_btn_volver()
                return

            # Limpieza proactiva de procesos huérfanos de WSL
            try:
                subprocess.run('wsl --cd ~ -u root -e pkill -f "build_iso.sh|download_iso.sh"', shell=True, creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
        else:
            # En Linux nativo limpiamos los procesos huérfanos locales
            try:
                subprocess.run('pkill -f "build_iso.sh|download_iso.sh"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            if sys.platform == "win32":
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Detectando dependencias de Linux en WSL..."))
                wsl_deps_cmd = 'wsl --cd ~ -u root -e bash -c "apt-get update && apt-get install -y xorriso squashfs-tools e2fsprogs mtools dosfstools p7zip-full wget curl aria2 syslinux-utils isolinux coreutils"'
                subprocess.run(wsl_deps_cmd, shell=True, creationflags=0x08000000, check=False)
                
                def to_wsl_path(win_path):
                    drive, rest = os.path.splitdrive(win_path)
                    return f"/mnt/{drive[0].lower()}{rest.replace(os.sep, '/')}"
                    
                wsl_project_root = to_wsl_path(project_root)
                drive_letter = os.path.splitdrive(project_root)[0][0].lower()
                
                mount_logic = f'if [ ! -d /mnt/{drive_letter} ]; then mkdir -p /mnt/{drive_letter}; fi; if ! mountpoint -q /mnt/{drive_letter}; then mount -t drvfs {drive_letter.upper()}: /mnt/{drive_letter}; fi; '
                
                cmd = f'wsl --cd ~ -u root -e bash -c "{mount_logic}export ISO_DISTRO=\\"{distro_env}\\"; sed -i \\"s/\\\\r\\$//\\" \\"{wsl_project_root}/builder/download_iso.sh\\" 2>/dev/null; cd \\"{wsl_project_root}\\" && bash \\"{wsl_project_root}/builder/download_iso.sh\\" \\"{distro_env}\\""'
                
                self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=0x08000000, bufsize=1, universal_newlines=True)
            else:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Instalando dependencias nativas de Linux..."))
                linux_deps_cmd = 'pkexec bash -c "apt-get update && apt-get install -y xorriso squashfs-tools e2fsprogs mtools dosfstools p7zip-full wget curl aria2 syslinux-utils isolinux coreutils"'
                subprocess.run(linux_deps_cmd, shell=True, check=False)
                
                cmd = f'export ISO_DISTRO="{distro_env}"; cd "{project_root}" && bash "{project_root}/builder/download_iso.sh" "{distro_env}"'
                self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
            
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Descargando imagen oficial de la ISO..."))
            
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
                    percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                    if percent_match:
                        percent_val = float(percent_match.group(1)) / 100.0
                        val = float(percent_match.group(1))
                        text_val = f"{val:.2f}".replace('.', ',')
                        self.after(0, self.update_progress_download, percent_val, text_val)
                else:
                    char_buffer.append(char)
                    
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
                self.is_building = False
                
        except Exception as e:
            if not self.is_cancelled:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda: msg_show_error("Error", str(e)))
                self.after(0, self.set_btn_volver)
                self.is_building = False

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
                self.is_building = False

    def run_build_thread(self, project_root, distro_env, distro_seleccionada):
        self.after(0, self.start_indeterminate_generation)
        current_phase = "processing"
        
        try:
            custom_iso_name = f"{distro_seleccionada} custom by Stack"
            
            if sys.platform == "win32":
                def to_wsl_path(win_path):
                    drive, rest = os.path.splitdrive(win_path)
                    return f"/mnt/{drive[0].lower()}{rest.replace(os.sep, '/')}"
                    
                wsl_project_root = to_wsl_path(project_root)
                drive_letter = os.path.splitdrive(project_root)[0][0].lower()
                
                mount_logic = f'if [ ! -d /mnt/{drive_letter} ]; then mkdir -p /mnt/{drive_letter}; fi; if ! mountpoint -q /mnt/{drive_letter}; then mount -t drvfs {drive_letter.upper()}: /mnt/{drive_letter}; fi; '
                
                cmd = f'wsl --cd ~ -u root -e bash -c "{mount_logic}export ISO_DISTRO=\\"{distro_env}\\"; export CUSTOM_ISO_NAME=\\"{custom_iso_name}\\"; sed -i \\"s/\\\\r\\$//\\" \\"{wsl_project_root}/builder/build_iso.sh\\" 2>/dev/null; cd \\"{wsl_project_root}\\" && bash \\"{wsl_project_root}/builder/build_iso.sh\\""'
                
                self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=0x08000000, bufsize=1, universal_newlines=True)
            else:
                cmd = f'pkexec bash -c "export ISO_DISTRO=\\"{distro_env}\\"; export CUSTOM_ISO_NAME=\\"{custom_iso_name}\\"; cd \\"{project_root}\\" && bash \\"{project_root}/builder/build_iso.sh\\""'
                self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
            
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Modificando e inyectando código en la ISO..."))
            self.after(0, self.update_progress_download, 1.0, "100,00")
            
            current_phase = "processing"
            current_subphase = "init"
            
            if distro_env == "ubuntu":
                phases = {
                    "generating": {"start": 0.0, "weight": 1.0, "label": "Empaquetando ISO final"}
                }
                current_subphase = "generating"
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Empaquetando ISO final..."))
            elif distro_env == "fedora":
                phases = {
                    "extracting_squashfs": {"start": 0.0, "weight": 0.15, "label": "Extrayendo imagen base"},
                    "unpacking": {"start": 0.15, "weight": 0.20, "label": "Desempaquetando sistema"},
                    "repacking": {"start": 0.35, "weight": 0.50, "label": "Comprimiendo nuevo sistema"},
                    "generating": {"start": 0.85, "weight": 0.15, "label": "Exportando ISO"}
                }
            else:
                phases = {
                    "extracting_squashfs": {"start": 0.0, "weight": 0.15, "label": "Extrayendo squashfs"},
                    "unpacking": {"start": 0.15, "weight": 0.20, "label": "Desempaquetando squashfs"},
                    "repacking": {"start": 0.35, "weight": 0.50, "label": "Reempaquetando squashfs"},
                    "generating": {"start": 0.85, "weight": 0.15, "label": "Exportando ISO"}
                }
                
            total_phases_count = len(phases)
            phase_keys = list(phases.keys())
            
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
                    
                    phase_changed = False
                    if "extrayendo" in line_lower and ("squashfs" in line_lower or "imagen" in line_lower):
                        current_subphase = "extracting_squashfs"
                        phase_changed = True
                    elif "desempaquetando squashfs" in line_lower:
                        current_subphase = "unpacking"
                        phase_changed = True
                    elif "reempaquetando squashfs" in line_lower:
                        current_subphase = "repacking"
                        phase_changed = True
                    elif "generando nueva iso" in line_lower:
                        current_subphase = "generating"
                        phase_changed = True
                        
                    if phase_changed and current_subphase in phases:
                        phase_info = phases[current_subphase]
                        current_pass_idx = phase_keys.index(current_subphase) + 1
                        
                        if total_phases_count > 1:
                            status_text = f"Estado: {phase_info['label']} ({current_pass_idx}/{total_phases_count})..."
                        else:
                            status_text = f"Estado: {phase_info['label']}..."
                            
                        self.status_lbl.after(0, lambda t=status_text: self.status_lbl.configure(text=t))
                        
                        if current_subphase in ["extracting_squashfs", "unpacking", "repacking"]:
                            phase_end = phase_info["start"] + phase_info["weight"]
                            rate = 0.00003 if current_subphase == "repacking" else 0.00015
                            self.after(0, lambda c=phase_end, r=rate: self.prog_mgr_gen.enable_simulation(cap=c, rate=r))
                        else:
                            self.after(0, self.prog_mgr_gen.disable_simulation)
                            
                    percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                    if not percent_match and re.match(r'^\d+$', line.strip()):
                        percent_match = re.match(r'^(\d+)$', line.strip())
                        
                    if percent_match and current_subphase in phases:
                        raw_percent = float(percent_match.group(1)) / 100.0
                        
                        phase_start = phases[current_subphase]["start"]
                        phase_weight = phases[current_subphase]["weight"]
                        
                        actual_percent = phase_start + (raw_percent * phase_weight)
                        
                        val = actual_percent * 100.0
                        text_val = f"{val:.2f}".replace('.', ',')
                        
                        self.after(0, self.update_progress_generation, actual_percent, text_val)
                            
                    if "fatal_error" in line_lower or line_lower.startswith("[fatal_error]"):
                        # El script de WSL reportó un error crítico — mostrarlo de inmediato
                        error_details = line
                        self.after(0, self.prog_mgr_gen.disable_simulation)
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
                self.is_building = False
                self.after(0, self.prog_mgr_gen.disable_simulation)
                self.after(0, self.update_progress_generation, 1.0, "100,00")
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Sistema Construido Exitosamente.", text_color="#00FF00"))
                
                def on_success_actions():
                    msg_show_info("Éxito", f"¡La imagen de {distro_seleccionada} se ha construido correctamente!\nYa puedes usarla para flashear una USB o instalarla en una máquina virtual. \nTu imagen se encuentra en la carpeta output")
                    self.btn_flash_usb.pack(side="left", padx=10)
                    
                    if msg_ask_yes_no("Ahorrar Espacio", "¿Deseas eliminar la ISO oficial descargada para ahorrar espacio en tu disco duro?\n\nTu imagen personalizada recién creada NO se borrará y se mantendrá segura en la carpeta 'output'."):
                            import glob
                            import os
                            from utils import get_project_root
                            download_dir = os.path.join(get_project_root(), "downloads", "iso", distro_env)
                            isos = glob.glob(os.path.join(download_dir, "*.iso"))
                            deleted = False
                            for iso in isos:
                                try:
                                    os.remove(iso)
                                    deleted = True
                                except Exception:
                                    pass
                            if deleted:
                                msg_show_info("Ahorrar Espacio", "La imagen original (oficial) ha sido eliminada correctamente para liberar espacio.")
                    
                    self.controller.show_frame("OptionSelectionScreen")

                # Esperar a que la animación llegue visualmente al 100% antes de mostrar el popup
                self.prog_mgr_gen.set_on_complete(on_success_actions)
            else:
                self.is_building = False
                self.after(0, self.prog_mgr_gen.disable_simulation)
                self.after(0, self.update_progress_generation, 0.0, "0,00")
                error_details = "\n".join(last_lines)
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error en la construcción.", text_color="#FF0000"))
                self.after(0, lambda err=error_details: msg_show_error("Error", f"Ocurrió un error durante la construcción de la ISO.\nDetalles:\n{err}"))

                
        except Exception as e:
            if not self.is_cancelled:
                self.is_building = False
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda: msg_show_error("Error", str(e)))
            
        finally:
            if not self.is_cancelled:
                self.is_building = False
                self.after(0, self.set_btn_volver)
