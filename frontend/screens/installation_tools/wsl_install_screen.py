import customtkinter as ctk
import subprocess
import threading
import sys
import time
from custom_messagebox import msg_show_info, msg_show_error
from utils import apply_glow_effect

class WslInstallScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = ctk.CTkLabel(self, text="> Instalador de WSL_", 
                                      font=ctk.CTkFont(family="Consolas", size=38, weight="bold"),
                                      text_color="#00FF00")
        self.title_lbl.grid(row=0, column=0, pady=(20, 10))
        
        self.desc_lbl = ctk.CTkLabel(self, text="Para compilar las imágenes, el sistema requiere el\nSubsistema de Windows para Linux (WSL).", 
                                     font=ctk.CTkFont(family="Consolas", size=16), text_color="#00E676", justify="center")
        self.desc_lbl.grid(row=1, column=0, pady=(0, 20))
        
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, pady=(0, 20))
        
        self.status_lbl = ctk.CTkLabel(self.progress_frame, text="Estado: Esperando confirmación...", text_color="#008800", font=ctk.CTkFont(family="Consolas", size=14))
        self.status_lbl.pack(pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, mode="indeterminate", width=500, progress_color="#00FF00", fg_color="#002200")
        self.progress_bar.pack()
        self.progress_bar.set(0)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(10, 20))
        
        self.btn_home = ctk.CTkButton(btn_frame, text="← Volver", command=self.go_home,
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_home, default_text="← Volver", hover_text="← Volver")
        self.btn_home.pack(side="left", padx=15)
        
        self.btn_install = ctk.CTkButton(btn_frame, text="Iniciar Instalación", command=self.start_install,
                                   height=45, width=220, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="#004400", border_width=2, border_color="#00FF00",
                                   hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_install, default_text="Iniciar Instalación", hover_text="Iniciar Instalación")
        self.btn_install.pack(side="left", padx=15)
        
        self.is_installing = False
        self.process = None

    def on_show(self):
        self.is_installing = False
        self.status_lbl.configure(text="Estado: Esperando confirmación...", text_color="#008800")
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.btn_install.configure(state="normal")
        self.btn_home.configure(state="normal")

    def go_home(self):
        if self.is_installing:
            return
        self.controller.show_frame("OptionSelectionScreen")

    def start_install(self):
        self.is_installing = True
        self.btn_install.configure(state="disabled")
        self.btn_home.configure(state="disabled")
        self.status_lbl.configure(text="Estado: Solicitando permisos e instalando WSL...", text_color="#FFAA00")
        self.progress_bar.start()
        
        threading.Thread(target=self.install_worker, daemon=True).start()

    def install_worker(self):
        try:
            cflags = 0x08000000 if sys.platform == "win32" else 0
            # Lanzar wsl --install elevado. PowerShell lo ejecutará en una ventana separada pero esperaremos a que termine si usamos -Wait, o haremos polling.
            # Start-Process con -Wait funciona para esperar que termine.
            ps_cmd = 'Start-Process powershell -ArgumentList "-NoExit", "-Command", "wsl --install; exit" -Verb RunAs -Wait'
            
            res = subprocess.run(['powershell', '-Command', ps_cmd], creationflags=cflags)
            
            if res.returncode == 0:
                self.after(0, self.install_success)
            else:
                self.after(0, lambda: self.install_failed("El proceso devolvió un error."))
                
        except Exception as e:
            self.after(0, lambda e=e: self.install_failed(str(e)))

    def install_success(self):
        self.is_installing = False
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.status_lbl.configure(text="Estado: Instalación finalizada con éxito.", text_color="#00FF00")
        self.btn_home.configure(state="normal")
        
        def show_popup():
            msg_show_info(
                "Instalación Exitosa",
                "WSL ha sido instalado o ya se encontraba habilitado.\n\n"
                "¡MUY IMPORTANTE! Si es la primera vez que instalas WSL, DEBES REINICIAR TU PC AHORA para que los cambios surtan efecto."
            )
        self.after(800, show_popup)

    def install_failed(self, err_msg):
        self.is_installing = False
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.status_lbl.configure(text="Estado: Error en la instalación.", text_color="#FF0000")
        self.btn_home.configure(state="normal")
        self.btn_install.configure(state="normal")
        msg_show_error(
            "Error",
            f"No se pudo instalar WSL.\nError: {err_msg}\n\n"
            "Puedes intentar abrir PowerShell como Administrador y ejecutar 'wsl --install' manualmente."
        )
