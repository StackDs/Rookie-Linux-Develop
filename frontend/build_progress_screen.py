import customtkinter as ctk
import os
import sys
import subprocess
import threading
import glob
import re
from tkinter import messagebox
from utils import apply_glow_effect

class BuildProgressScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Construyendo Sistema_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=1, column=0, pady=(0, 20))

        self.info_lbl = ctk.CTkLabel(self, text="", text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=16))
        self.info_lbl.grid(row=2, column=0, pady=(0, 30))
        
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=3, column=0, pady=(0, 20))
        
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
        btn_frame.grid(row=4, column=0, pady=(40, 0))
        
        self.btn_flash_usb = ctk.CTkButton(btn_frame, text="Montar en USB", command=lambda: self.controller.show_frame("UsbFlashScreen"),
                                   height=45, width=200, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="#004400", border_width=2, border_color="#00FF00",
                                   hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_flash_usb, default_text="Montar en USB", hover_text="Montar en USB")
        
        self.btn_action = ctk.CTkButton(btn_frame, text="Cancelar", command=self.cancel_process,
                                   height=45, width=200, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#FF0000",
                                   hover_color="#330000", text_color="#FF0000")
        apply_glow_effect(self.btn_action, default_text="Cancelar", hover_text="Cancelar")
        
        # Ocultar botones inicialmente, se empaquetan en on_show
        self.btn_action.pack(side="left", padx=10)
        
        self.current_process = None
        self.current_iso_target_dir = None
        self.is_cancelled = False

    def on_show(self):
        distro_seleccionada = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        self.info_lbl.configure(text=f"Preparando la construcción de: {distro_seleccionada}")
        self.status_lbl.configure(text="Estado: Iniciando motor de Docker...", text_color="#00FF00")
        
        self.is_cancelled = False
        self.btn_flash_usb.pack_forget()
        self.btn_action.configure(text="Cancelar", command=self.cancel_process, text_color="#FF0000", border_color="#FF0000", hover_color="#330000", state="normal")
        apply_glow_effect(self.btn_action, default_text="Cancelar", hover_text="Cancelar")
        
        self.update_progress_download(0.0, "0")
        self.update_progress_generation(0.0, "0")
        self.ejecutar_script()

    def update_progress_download(self, val, text_val):
        self.progress_bar_download.set(val)
        self.lbl_download.configure(text=f"Descarga: {text_val}%")

    def update_progress_generation(self, val, text_val):
        self.progress_bar_generation.set(val)
        self.lbl_generation.configure(text=f"Generación: {text_val}%")

    def set_btn_volver(self):
        self.btn_action.configure(text="← Volver al Inicio", command=lambda: self.controller.show_frame("StartScreen"), 
                                  text_color="#008800", border_color="#008800", hover_color="#001100", state="normal")
        apply_glow_effect(self.btn_action, default_text="← Volver al Inicio", hover_text="← Volver al Inicio")

    def cancel_process(self):
        self.is_cancelled = True
        self.btn_action.configure(state="disabled")
        self.status_lbl.configure(text="Estado: Cancelando proceso y limpiando...", text_color="#FF0000")
        
        if self.current_process:
            try:
                self.current_process.kill()
            except Exception:
                pass
                
        if self.current_iso_target_dir:
            try:
                isos = glob.glob(os.path.join(self.current_iso_target_dir, "*.iso"))
                for iso in isos:
                    os.remove(iso)
            except Exception:
                pass
                
        self.status_lbl.configure(text="Estado: Proceso cancelado.")
        self.set_btn_volver()

    def check_and_delete_iso(self, directory, name_desc, distro_env):
        isos = glob.glob(os.path.join(directory, "*.iso"))
        if not isos and "popos" in distro_env:
            isos = glob.glob(os.path.join(os.path.dirname(directory), "pop", "*.iso"))
        if isos:
            iso_file = isos[0]
            iso_name = os.path.basename(iso_file)
            msg = f"Se encontró una ISO {name_desc} existente: '{iso_name}'.\n\n¿Desea eliminarla y generarla de nuevo?\n\n• 'Sí' para reconstruir.\n• 'No' para reusar la existente."
            if messagebox.askyesno("ISO Detectada", msg):
                try:
                    os.remove(iso_file)
                    print(f"Eliminado: {iso_file}")
                    return True
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"No se pudo eliminar el archivo:\n{e}")
                    return True
            else:
                return False
        return True

    def ejecutar_script(self):
        distro_seleccionada = self.controller.frames["DistroSelectionScreen"].distro_var.get()
        
        distro_map = {
            "Ubuntu": "ubuntu",
            "Linux Mint": "mint",
            "Fedora": "fedora",
            "Pop!_OS": "popos"
        }
        
        distro_env = distro_map.get(distro_seleccionada, "ubuntu")
        
        if distro_seleccionada == "Pop!_OS":
            respuesta = messagebox.askyesno(
                "Versión de Pop!_OS", 
                "¿Tienes una tarjeta gráfica NVIDIA en tu equipo?\n\n"
                "• Selecciona 'Sí' para usar la ISO con drivers NVIDIA preinstalados.\n"
                "• Selecciona 'No' para usar la ISO estándar (Intel/AMD)."
            )
            if respuesta:
                distro_env = "popos_nvidia"
            else:
                distro_env = "popos_amd"
                
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        
        # Check oficial ISO
        download_dir = os.path.join(project_root, "downloads", "iso", distro_env)
        os.makedirs(download_dir, exist_ok=True)
        self.check_and_delete_iso(download_dir, "oficial descargada", distro_env)
        
        # Iniciar hilo de Docker para descarga
        self.current_iso_target_dir = download_dir
        threading.Thread(target=self.run_download_thread, args=(project_root, distro_env, distro_seleccionada), daemon=True).start()

    def run_download_thread(self, project_root, distro_env, distro_seleccionada):
        self.after(0, self.update_progress_download, 0.0, "0")
        
        try:
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            
            # Ejecutar build primero
            build_cmd = 'docker compose build builder'
            subprocess.run(build_cmd, shell=True, cwd=project_root, creationflags=creationflags, check=False)
            
            # Ejecutar run de la descarga
            cmd = f'docker compose run -e ISO_DISTRO="{distro_env}" --rm builder /workspace/builder/download_iso.sh "{distro_env}"'
            
            self.current_process = subprocess.Popen(cmd, shell=True, cwd=project_root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=creationflags, bufsize=1, universal_newlines=True)
            
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
                    text_val = str(int(float(percent_match.group(1))))
                    self.after(0, self.update_progress_download, percent_val, text_val)
                    
            self.current_process.stdout.close()
            self.current_process.wait()
            
            if self.is_cancelled:
                return
            
            if self.current_process.returncode == 0:
                self.after(0, self.update_progress_download, 1.0, "100")
                self.after(0, self.check_output_iso_and_build, project_root, distro_env, distro_seleccionada)
            else:
                error_details = "\n".join(last_lines)
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error en la descarga.", text_color="#FF0000"))
                self.after(0, lambda err=error_details: messagebox.showerror("Error", f"Ocurrió un error durante la descarga de la ISO.\nDetalles:\n{err}"))
                self.after(0, self.set_btn_volver)
                
        except Exception as e:
            if not self.is_cancelled:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
                self.after(0, self.set_btn_volver)

    def check_output_iso_and_build(self, project_root, distro_env, distro_seleccionada):
        if self.is_cancelled:
            return
        output_dir = os.path.join(project_root, "output", distro_env)
        os.makedirs(output_dir, exist_ok=True)
        should_build = self.check_and_delete_iso(output_dir, "modificada final", distro_env)
        
        self.current_iso_target_dir = output_dir
        if not self.is_cancelled:
            if should_build:
                threading.Thread(target=self.run_build_thread, args=(project_root, distro_env, distro_seleccionada), daemon=True).start()
            else:
                self.after(0, self.update_progress_generation, 1.0, "100")
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Usando ISO generada previamente.", text_color="#00FF00"))
                self.after(0, lambda: self.btn_flash_usb.pack(side="left", padx=10))
                self.after(0, self.set_btn_volver)

    def run_build_thread(self, project_root, distro_env, distro_seleccionada):
        self.after(0, self.update_progress_generation, 0.0, "0")
        current_phase = "processing"
        
        try:
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            
            cmd = f'docker compose run -e ISO_DISTRO="{distro_env}" --rm builder /workspace/builder/build_iso.sh'
            
            self.current_process = subprocess.Popen(cmd, shell=True, cwd=project_root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=creationflags, bufsize=1, universal_newlines=True)
            
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Modificando e inyectando código en la ISO..."))
            self.after(0, self.update_progress_download, 1.0, "100")
            
            last_lines = []
            for line in iter(self.current_process.stdout.readline, ''):
                if not line or self.is_cancelled:
                    break
                
                last_lines.append(line.strip())
                if len(last_lines) > 5:
                    last_lines.pop(0)
                    
                line_lower = line.lower()
                percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                if percent_match:
                    percent_val = float(percent_match.group(1)) / 100.0
                    text_val = str(int(float(percent_match.group(1))))
                    if current_phase == "generating":
                        self.after(0, self.update_progress_generation, percent_val, text_val)
                        
                if "generando nueva iso" in line_lower:
                    current_phase = "generating"
                    self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Empaquetando y exportando ISO final..."))
                elif "exitosa" in line_lower:
                    current_phase = "done"
                    self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: ¡ISO finalizada con éxito!"))
                    self.after(0, self.update_progress_generation, 1.0, "100")
                    
            self.current_process.stdout.close()
            self.current_process.wait()
            
            if self.is_cancelled:
                return
            
            if self.current_process.returncode == 0:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Sistema Construido Exitosamente.", text_color="#00FF00"))
                self.after(0, lambda: messagebox.showinfo("Éxito", f"¡La imagen de {distro_seleccionada} se ha construido correctamente!\n\nRevisa la carpeta 'output'."))
                self.after(0, lambda: self.btn_flash_usb.pack(side="left", padx=10))
            else:
                error_details = "\n".join(last_lines)
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error en la construcción.", text_color="#FF0000"))
                self.after(0, lambda err=error_details: messagebox.showerror("Error", f"Ocurrió un error durante la construcción de la ISO.\nDetalles:\n{err}"))

                
        except Exception as e:
            if not self.is_cancelled:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
            
        finally:
            if not self.is_cancelled:
                self.after(0, self.set_btn_volver)
