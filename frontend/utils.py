import time
import customtkinter as ctk
import os
import sys
import subprocess
from tkinter import filedialog

def native_file_dialog(title="Seleccionar archivo", filetypes=(("Todos los archivos", "*.*"),)):
    """Abre un diálogo de selección de archivos. En Linux intenta usar Zenity o Kdialog para una apariencia nativa."""
    if sys.platform.startswith("linux"):
        try:
            # Intentar usar zenity (GNOME/GTK)
            cmd = ["zenity", "--file-selection", f"--title={title}"]
            for name, ext in filetypes:
                cmd.append(f"--file-filter={name} | {ext}")
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            elif result.returncode == 1:
                return "" # Cancelado
        except FileNotFoundError:
            try:
                # Intentar usar kdialog (KDE)
                filter_str = " ".join([ext for name, ext in filetypes])
                cmd = ["kdialog", "--title", title, "--getopenfilename", ".", filter_str]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
                elif result.returncode == 1:
                    return ""
            except FileNotFoundError:
                pass # Si no hay ni zenity ni kdialog, caemos en tkinter
                
    # Fallback a Tkinter (Windows, macOS o Linux sin herramientas nativas)
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

def get_project_root():
    """Retorna la raiz del proyecto de forma compatible con PyInstaller."""
    if getattr(sys, 'frozen', False):
        # Si esta empaquetado como exe, la raiz es la carpeta donde esta el exe
        return os.path.dirname(sys.executable)
    else:
        # Si se ejecuta desde el script, la raiz es un nivel arriba de 'frontend'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, ".."))
def apply_glow_effect(btn, default_text, hover_text=None, color_base="#008800", color_glow="#00FF00"):
    
    def on_enter(e):
        btn.configure(
            border_color=color_glow,
            text_color=color_glow,
            text=hover_text if hover_text else default_text
        )
        
    def on_leave(e):
        btn.configure(
            border_color=color_base,
            text_color=color_base,
            text=default_text
        )
        
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    # Force initial non-hovered state
    on_leave(None)

class ProgressManager:
    def __init__(self, root_widget, progress_bar, label_widget, label_prefix="Progreso: ", step=0.005, delay=20, eta_label=None):
        self.root_widget = root_widget
        self.progress_bar = progress_bar
        self.label_widget = label_widget
        self.eta_label = eta_label
        self.label_prefix = label_prefix
        self.step = step
        self.delay = delay
        
        # Desactivamos el output en consola para usar rich internamente
        try:
            from rich.console import Console
            from rich.progress import Progress
            self._devnull = open(os.devnull, "w")
            self.rich_console = Console(file=self._devnull)
            self.rich_progress = Progress(console=self.rich_console)
            self.task_id = self.rich_progress.add_task("progress", total=100.0)
            self.has_rich = True
        except ImportError:
            self.has_rich = False
        
        self.current_progress = 0.0
        self.target_progress = 0.0
        self.is_animating = False
        
        self.simulating = False
        self.sim_cap = 0.99
        self.sim_rate = 0.0001
        
        self._on_complete = None

    def __del__(self):
        if getattr(self, "has_rich", False):
            try:
                self._devnull.close()
            except:
                pass

    def update_progress(self, target_percent):
        self.target_progress = target_percent
        
        if not self.is_animating:
            self.is_animating = True
            self.animate()

    def set_on_complete(self, callback):
        """Registra un callback que se ejecutará cuando la animación llegue al target."""
        self._on_complete = callback
            
    def enable_simulation(self, cap=0.99, rate=0.00005):
        self.simulating = True
        self.sim_cap = cap
        self.sim_rate = rate
        if not self.is_animating:
            self.is_animating = True
            self.animate()

    def disable_simulation(self):
        self.simulating = False
            
    def set_indeterminate(self, text):
        self.is_animating = False
        if self.progress_bar.cget("mode") != "indeterminate":
            self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self.label_widget.configure(text=text)

    def set_determinate(self):
        self.progress_bar.stop()
        if self.progress_bar.cget("mode") != "determinate":
            self.progress_bar.configure(mode="determinate")
        
    def reset(self, text=None):
        self.is_animating = False
        self.simulating = False
        self._on_complete = None
        self.current_progress = 0.0
        self.target_progress = 0.0
        
        if self.has_rich:
            self.rich_progress.update(self.task_id, completed=0.0)
            self.rich_progress.reset(self.task_id, total=100.0)
            
        self.progress_bar.set(0.0)
        if text:
            self.label_widget.configure(text=text)
        else:
            self.label_widget.configure(text=f"{self.label_prefix}0,00%")
        if self.eta_label:
            self.eta_label.configure(text="")
            
    def animate(self):
        if self.simulating and self.target_progress < self.sim_cap:
            if abs(self.target_progress - self.current_progress) < 0.05:
                self.target_progress += self.sim_rate
                if self.target_progress > self.sim_cap:
                    self.target_progress = self.sim_cap

        diff = self.target_progress - self.current_progress
        
        # Exponential smoothing para un incremento fluido
        step = diff * 0.02
        min_step = 0.0001 
        
        if diff > 0:
            if step < min_step: step = min_step
            self.current_progress += step
            if self.current_progress > self.target_progress:
                self.current_progress = self.target_progress
        elif diff < 0:
            if step > -min_step: step = -min_step
            self.current_progress += step
            if self.current_progress < self.target_progress:
                self.current_progress = self.target_progress

        self.progress_bar.set(self.current_progress)
        
        if self.has_rich:
            # Backend rich para cálculos
            self.rich_progress.update(self.task_id, completed=self.current_progress * 100.0)
            task = self.rich_progress.tasks[self.task_id]
            
            val = task.percentage if task.percentage is not None else (self.current_progress * 100.0)
            text_val = f"{val:.2f}".replace('.', ',')
            self.label_widget.configure(text=f"{self.label_prefix}{text_val}%")
            
            if self.eta_label:
                # Solo mostrar ETA si se ha avanzado un mínimo razonable
                if task.time_remaining is not None and self.current_progress > 0.01 and self.current_progress < 0.99:
                    eta_seconds = int(task.time_remaining)
                    mins, secs = divmod(eta_seconds, 60)
                    hours, mins = divmod(mins, 60)
                    if hours > 0:
                        eta_str = f"Faltan ~{hours:02d}:{mins:02d}:{secs:02d}"
                    else:
                        eta_str = f"Faltan ~{mins:02d}:{secs:02d}"
                    self.eta_label.configure(text=eta_str)
                else:
                    if self.target_progress >= 0.99:
                        self.eta_label.configure(text="")
                    elif not self.eta_label.cget("text"):
                        self.eta_label.configure(text="Calculando ETA...")
        else:
            val = self.current_progress * 100.0
            text_val = f"{val:.2f}".replace('.', ',')
            self.label_widget.configure(text=f"{self.label_prefix}{text_val}%")
        
        if abs(self.current_progress - self.target_progress) < 0.00001 and not self.simulating:
            self.current_progress = self.target_progress
            self.is_animating = False
            if self._on_complete is not None:
                cb = self._on_complete
                self._on_complete = None
                self.root_widget.after(0, cb)
        else:
            self.root_widget.after(self.delay, self.animate)

