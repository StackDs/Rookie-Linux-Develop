import customtkinter as ctk
import os
import sys
import subprocess
import threading
import glob
import json
import time
import tempfile
from tkinter import filedialog
from custom_messagebox import msg_show_info, msg_show_error, msg_show_warning, msg_ask_yes_no
from utils import apply_glow_effect, get_project_root, ProgressManager

class UsbFlashScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.drives_info = []
        
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="> Flasheador USB_", 
                                  text_color="#00FF00",
                                  font=ctk.CTkFont(family="Consolas", size=38, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))

        self.info_lbl = ctk.CTkLabel(self, text="Selecciona una unidad USB para grabar la ISO", text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=16))
        self.info_lbl.grid(row=1, column=0, pady=(0, 15))
        
        # Admin Warning
        self.admin_lbl = ctk.CTkLabel(self, text="Se te pedirá permisos de Administrador.", 
                                      text_color="#FFAA00", font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        self.admin_lbl.grid(row=2, column=0, pady=(0, 15))
        
        # ISO Selection Frame
        iso_frame = ctk.CTkFrame(self, fg_color="transparent")
        iso_frame.grid(row=3, column=0, pady=(0, 15))
        
        self.iso_var = ctk.StringVar(value="")
        self.iso_entry = ctk.CTkEntry(iso_frame, textvariable=self.iso_var, width=350, font=ctk.CTkFont(family="Consolas", size=13), state="disabled", fg_color="#001100", border_color="#008800", text_color="#00FF00")
        self.iso_entry.pack(side="left", padx=10)
        
        self.btn_browse = ctk.CTkButton(iso_frame, text="Buscar ISO", command=self.browse_iso, height=30, width=100, font=ctk.CTkFont(family="Consolas", size=13, weight="bold"), cursor="hand2", fg_color="transparent", border_width=1, border_color="#008800", hover_color="#002200", text_color="#00FF00")
        self.btn_browse.pack(side="left")

        # Selection Frame
        sel_frame = ctk.CTkFrame(self, fg_color="transparent")
        sel_frame.grid(row=4, column=0, pady=(0, 20))
        
        self.combo_var = ctk.StringVar(value="Buscando unidades...")
        self.usb_combo = ctk.CTkComboBox(sel_frame, variable=self.combo_var, values=["Buscando unidades..."], width=350,
                                         font=ctk.CTkFont(family="Consolas", size=14),
                                         fg_color="#001100", border_color="#008800", text_color="#00FF00",
                                         button_color="#005500", button_hover_color="#00AA00", dropdown_fg_color="#001100", dropdown_text_color="#00FF00")
        self.usb_combo.pack(side="left", padx=10)
        
        self.btn_refresh = ctk.CTkButton(sel_frame, text="↻ Refrescar", command=self.load_drives,
                                   height=30, width=100, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=13, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=1, border_color="#008800",
                                   hover_color="#002200", text_color="#00FF00")
        self.btn_refresh.pack(side="left")
        
        # Progress Frame
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=5, column=0, pady=(0, 20))
        
        self.status_lbl = ctk.CTkLabel(self.progress_frame, text="Estado: Esperando confirmación...", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=14))
        self.status_lbl.pack(pady=(0, 10))
        
        self.lbl_progress = ctk.CTkLabel(self.progress_frame, text="Progreso: 0%", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=12))
        self.lbl_progress.pack(anchor="w")
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, mode="determinate", width=500, progress_color="#00FF00", fg_color="#002200")
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=6, column=0, pady=(10, 20))
        
        self.btn_action = ctk.CTkButton(btn_frame, text="← Volver", command=lambda: self.controller.show_frame("OptionSelectionScreen"),
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")
        self.btn_action.pack(side="left", padx=10)
        
        self.btn_flash = ctk.CTkButton(btn_frame, text="Flashear USB", command=self.start_flash,
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="#004400", border_width=2, border_color="#00FF00",
                                   hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_flash, default_text="Flashear USB", hover_text="Flashear USB")
        self.btn_flash.pack(side="left", padx=10)
        
        self.is_flashing = False
        self.cancel_flag = os.path.join(tempfile.gettempdir(), "rookie_flash_cancel.flag")
        
        self.prog_manager = ProgressManager(self, self.progress_bar, self.lbl_progress, "Progreso: ")

    def on_show(self):
        self.prog_manager.reset()
        self.status_lbl.configure(text="Estado: Esperando confirmación...", text_color="#008800")
        self.btn_flash.configure(state="normal")
        self.set_btn_volver()
        threading.Thread(target=self.load_drives, daemon=True).start()

    def set_btn_volver(self):
        self.btn_action.configure(text="← Volver", command=lambda: self.controller.show_frame("OptionSelectionScreen"),
                                  text_color="#008800", border_color="#008800", hover_color="#001100", state="normal")
        apply_glow_effect(self.btn_action, default_text="← Volver", hover_text="← Volver")

    def cancel_flash(self):
        msg = "¿Estás seguro que deseas cancelar el flasheo?\n\nADVERTENCIA: Si cancelas ahora, tu USB quedará corrupto e inutilizable hasta que lo vuelvas a formatear."
        if msg_ask_yes_no("Confirmar Cancelación", msg):
            self.btn_action.configure(state="disabled")
            self.status_lbl.configure(text="Estado: Cancelando proceso de escritura...", text_color="#FFAA00")
            try:
                with open(self.cancel_flag, "w") as f:
                    f.write("cancel")
            except: pass

    def load_drives(self):
        self.combo_var.set("Buscando unidades...")
        self.usb_combo.configure(values=["Buscando unidades..."])
        self.drives_info = []
        
        try:
            cmd = 'powershell -NoProfile -Command "Get-Disk | Where-Object {$_.BusType -eq \'USB\'} | Select-Object Number, FriendlyName, Size | ConvertTo-Json -Compress"'
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=creationflags)
            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, dict):
                        data = [data]
                    
                    values = []
                    for disk in data:
                        size_gb = disk.get("Size", 0) / (1024**3)
                        name = disk.get("FriendlyName", "USB Drive")
                        num = disk.get("Number", -1)
                        if num != -1:
                            display_str = f"Disco {num}: {name} ({size_gb:.1f} GB)"
                            values.append(display_str)
                            self.drives_info.append({"num": num, "display": display_str})
                    
                    if values:
                        self.usb_combo.configure(values=values)
                        self.combo_var.set(values[0])
                    else:
                        self.combo_var.set("No se encontraron USBs")
                        self.usb_combo.configure(values=["No se encontraron USBs"])
                except Exception as e:
                    self.combo_var.set("Error procesando USBs")
            else:
                self.combo_var.set("No se encontraron USBs")
                self.usb_combo.configure(values=["No se encontraron USBs"])
        except Exception as e:
            self.combo_var.set("Error al buscar unidades")

    def browse_iso(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen ISO",
            filetypes=(("Archivos ISO", "*.iso"), ("Todos los archivos", "*.*"))
        )
        if filename:
            self.iso_var.set(filename)

    def start_flash(self):
        iso_path = self.iso_var.get()
        if not iso_path or not os.path.exists(iso_path) or not iso_path.lower().endswith(".iso"):
            msg_show_warning("Aviso", "Por favor selecciona un archivo ISO válido.")
            return

        selected = self.combo_var.get()
        if "Disco" not in selected:
            msg_show_warning("Aviso", "Por favor selecciona un disco USB válido.")
            return
            
        target_num = None
        for d in self.drives_info:
            if d["display"] == selected:
                target_num = d["num"]
                break
                
        if target_num is None:
            msg_show_warning("Error", "No se pudo identificar el número de disco.")
            return
            
        iso_name = os.path.basename(iso_path)
        
        msg = f"ATENCIÓN: Vas a formatear y sobrescribir el siguiente disco:\n\n{selected}\n\nCon la imagen:\n{iso_name}\n\nTODOS LOS DATOS EN EL USB SE PERDERÁN.\n¿Estás absolutamente seguro de continuar?"
        if not msg_ask_yes_no("Peligro de pérdida de datos", msg, width=600, height=450):
            return
            
        try:
            if os.path.exists(self.cancel_flag):
                os.remove(self.cancel_flag)
        except: pass
            
        self.btn_flash.configure(state="disabled")
        
        self.btn_action.configure(text="Cancelar", command=self.cancel_flash, 
                                  text_color="#FF0000", border_color="#FF0000", hover_color="#330000")
        apply_glow_effect(self.btn_action, default_text="Cancelar", hover_text="Cancelar", color_base="#AA0000", color_glow="#FF0000")
        
        self.status_lbl.configure(text="Estado: Preparando disco (diskpart)...", text_color="#FFAA00")
        
        threading.Thread(target=self.flash_worker, args=(iso_path, target_num), daemon=True).start()

    def update_progress(self, percent, text):
        self.prog_manager.update_progress(percent)

    def flash_worker(self, iso_path, drive_num):
        prog_file = os.path.join(tempfile.gettempdir(), "rookie_flash_progress.json")
        try:
            if os.path.exists(prog_file):
                os.remove(prog_file)
        except:
            pass
            
        try:
            python_exe = sys.executable
            
            # Lanzamos el proceso trabajador elevado usando --worker
            if getattr(sys, 'frozen', False):
                # Exe empaquetado: relanzarse a sí mismo con --worker como proceso Admin
                args_list = f'--worker --iso "{iso_path}" --drive {drive_num} --progress "{prog_file}"'
                ps_cmd = f'Start-Process -FilePath "{python_exe}" -ArgumentList \'{args_list}\' -Verb RunAs -WindowStyle Hidden'
            else:
                # Modo código fuente: lanzar flasher_worker.py directamente
                worker_script = os.path.join(os.path.dirname(__file__), "flasher_worker.py")
                args_list = f'"{worker_script}" --iso "{iso_path}" --drive {drive_num} --progress "{prog_file}"'
                ps_cmd = f'Start-Process -FilePath "{python_exe}" -ArgumentList \'{args_list}\' -Verb RunAs -WindowStyle Hidden'
            
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            res = subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd], capture_output=True, text=True, creationflags=creationflags)
            
            if res.returncode != 0:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Flasheo cancelado o fallido.", text_color="#FF0000"))
                self.after(0, lambda: self.btn_flash.configure(state="normal"))
                self.after(0, self.set_btn_volver)
                return
                
            # Polling loop
            done = False
            error_msg = ""
            
            while not done:
                time.sleep(0.1)
                if not os.path.exists(prog_file):
                    continue
                    
                try:
                    with open(prog_file, "r") as f:
                        data = json.load(f)
                        
                    st = data.get("status", "")
                    pct = data.get("percent", 0.0)
                    txt = data.get("text", "0")
                    err = data.get("error", "")
                    
                    if st == "cleaning":
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Preparando y limpiando disco...", text_color="#FFAA00"))
                    elif st == "writing":
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Escribiendo ISO a bajo nivel (Modo DD)...", text_color="#00FF00"))
                        self.after(0, self.update_progress, pct, txt)
                    elif st == "done":
                        self.after(0, self.update_progress, 1.0, "100,00")
                        self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: ¡Flasheo completado con éxito!", text_color="#00FF00"))
                        self.after(0, lambda: msg_show_info("Éxito", "El USB booteable ha sido creado correctamente. Ya puedes usarlo para instalar el sistema."))
                        done = True
                    elif st == "error":
                        error_msg = err
                        done = True
                        
                except json.JSONDecodeError:
                    # File might be partially written, just ignore this cycle
                    pass
                except Exception as e:
                    pass
                    
            if error_msg:
                self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Operación interrumpida o fallida.", text_color="#FF0000"))
                self.after(0, lambda e=error_msg: msg_show_error("Error", f"Detalles:\n{e}"))
                
        except Exception as e:
            self.status_lbl.after(0, lambda: self.status_lbl.configure(text="Estado: Error inesperado.", text_color="#FF0000"))
            self.after(0, lambda e=e: msg_show_error("Error", str(e)))
        finally:
            self.after(0, self.set_btn_volver)
            self.after(0, lambda: self.btn_flash.configure(state="normal"))
            try:
                if os.path.exists(prog_file):
                    os.remove(prog_file)
                if os.path.exists(self.cancel_flag):
                    os.remove(self.cancel_flag)
            except:
                pass
