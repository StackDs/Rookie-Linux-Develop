import customtkinter as ctk
import subprocess
import threading
import sys
import time
from custom_messagebox import msg_show_info, msg_show_error, msg_ask_yes_no
from utils import apply_glow_effect

class WslAppInstallScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_lbl = ctk.CTkLabel(self, text="> Instalador de WSL (Modo App)_", 
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
                                   height=45, width=150, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="transparent", border_width=2, border_color="#008800",
                                   hover_color="#001100", text_color="#008800")
        apply_glow_effect(self.btn_home, default_text="← Volver", hover_text="← Volver")
        self.btn_home.grid(row=0, column=0, padx=10)
        
        self.btn_install_wsl = ctk.CTkButton(btn_frame, text="1. Habilitar WSL", command=self.start_install_wsl,
                                   height=45, width=190, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="#004400", border_width=2, border_color="#00FF00",
                                   hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_install_wsl, default_text="1. Habilitar WSL", hover_text="1. Habilitar WSL")
        self.btn_install_wsl.grid(row=0, column=1, padx=10)

        self.btn_install_distro = ctk.CTkButton(btn_frame, text="2. Instalar Distro", command=self.start_install_distro,
                                   height=45, width=190, corner_radius=5,
                                   font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), cursor="hand2",
                                   fg_color="#004400", border_width=2, border_color="#00FF00",
                                   hover_color="#007700", text_color="#FFFFFF")
        apply_glow_effect(self.btn_install_distro, default_text="2. Instalar Distro", hover_text="2. Instalar Distro")
        self.btn_install_distro.grid(row=0, column=2, padx=10)
        
        self.is_installing = False

    def on_show(self):
        self.is_installing = False
        self.status_lbl.configure(text="Estado: Esperando selección...", text_color="#008800")
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.btn_install_wsl.configure(state="normal")
        self.btn_install_distro.configure(state="normal")
        self.btn_home.configure(state="normal")

    def go_home(self):
        if self.is_installing:
            return
        self.controller.show_frame("WslInstallScreen")

    def start_install_wsl(self):
        if not msg_ask_yes_no("Confirmación", "¿Deseas habilitar WSL y la Plataforma de Máquina Virtual?\n\nEsto requerirá permisos de Administrador y reiniciar tu equipo al finalizar."):
            return
            
        self.is_installing = True
        self.btn_install_wsl.configure(state="disabled")
        self.btn_install_distro.configure(state="disabled")
        self.btn_home.configure(state="disabled")
        self.status_lbl.configure(text="Estado: Habilitando características de Windows (Fase 1)...", text_color="#FFAA00")
        self.progress_bar.start()
        
        threading.Thread(target=self.install_worker, args=("wsl --install --no-distribution", 1), daemon=True).start()

    def start_install_distro(self):
        if sys.platform == "win32":
            try:
                res = subprocess.run(["wsl", "--status"], capture_output=True, text=True, creationflags=0x08000000)
                if res.returncode != 0:
                    raise Exception()
            except Exception:
                msg_show_error(
                    "WSL No Habilitado",
                    "Primero debes habilitar WSL y REINICIAR tu equipo antes de intentar instalar distro auxiliar."
                )
                return

        if not msg_ask_yes_no("Confirmación", "¿Deseas instalar una distribución base (Ubuntu) para que el entorno de WSL sea funcional?\n\nEsto tomará varios minutos."):
            return

        self.is_installing = True
        self.btn_install_wsl.configure(state="disabled")
        self.btn_install_distro.configure(state="disabled")
        self.btn_home.configure(state="disabled")
        self.status_lbl.configure(text="Estado: Instalando distribución base de Ubuntu (Fase 2)...", text_color="#FFAA00")
        self.progress_bar.start()
        
        threading.Thread(target=self.install_worker, args=("wsl --install -d Ubuntu --no-launch", 2), daemon=True).start()

    def install_worker(self, wsl_command, phase):
        try:
            cflags = 0x08000000 if sys.platform == "win32" else 0
            ps_cmd = f'Start-Process powershell -ArgumentList "-WindowStyle", "Hidden", "-Command", "{wsl_command}; exit" -Verb RunAs -Wait'
            
            res = subprocess.run(['powershell', '-Command', ps_cmd], creationflags=cflags)
            
            if res.returncode == 0:
                self.after(0, lambda: self.install_success(phase))
            else:
                self.after(0, lambda: self.install_failed("El proceso devolvió un error."))
                
        except Exception as e:
            self.after(0, lambda e=e: self.install_failed(str(e)))

    def install_success(self, phase):
        self.is_installing = False
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.status_lbl.configure(text="Estado: Proceso finalizado con éxito.", text_color="#00FF00")
        self.btn_home.configure(state="normal")
        self.btn_install_wsl.configure(state="normal")
        self.btn_install_distro.configure(state="normal")
        
        def show_popup():
            if phase == 1:
                msg_show_info(
                    "Fase 1 Completada",
                    "WSL y la Plataforma de Máquina Virtual han sido habilitadas.\n\n"
                    "¡DEBES REINICIAR TU PC AHORA!\n\n"
                    "Después de reiniciar, vuelve a abrir el programa y usa el botón '2. Instala una distro auxiliar' para finalizar."
                )
            else:
                msg_show_info(
                    "Instalación Exitosa",
                    "Una distribución auxiliar se ha instalado correctamente dentro de WSL.\n\n"
                    "El sistema ya está listo para construir las imágenes."
                )
            self.controller.show_frame("OptionSelectionScreen")
        self.after(800, show_popup)

    def install_failed(self, err_msg):
        self.is_installing = False
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.status_lbl.configure(text="Estado: Error en la instalación.", text_color="#FF0000")
        self.btn_home.configure(state="normal")
        self.btn_install_wsl.configure(state="normal")
        self.btn_install_distro.configure(state="normal")
        msg_show_error(
            "Error",
            f"El proceso ha fallado.\nError: {err_msg}\n\n"
            "Intenta ejecutar el comando manualmente en PowerShell como Administrador."
        )
