import time
import customtkinter as ctk
import os
import sys

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
        
        self.current_progress = 0.0
        self.target_progress = 0.0
        self.is_animating = False
        
        self.history = []
        self.last_eta_update = 0

    def update_progress(self, target_percent):
        self.target_progress = target_percent
        
        # Guardar historial para ETA
        current_time = time.time()
        self.history.append((current_time, target_percent))
        # Mantener solo los últimos 15 segundos
        self.history = [(t, p) for t, p in self.history if current_time - t <= 15]
        
        if not self.is_animating:
            self.is_animating = True
            self.animate()
            
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
        self.current_progress = 0.0
        self.target_progress = 0.0
        self.history = []
        self.last_eta_update = 0
        self.progress_bar.set(0.0)
        if text:
            self.label_widget.configure(text=text)
        else:
            self.label_widget.configure(text=f"{self.label_prefix}0,00%")
        if self.eta_label:
            self.eta_label.configure(text="")
            
    def animate(self):
        diff = self.target_progress - self.current_progress
        
        # Exponential smoothing para un incremento fluido y constante de los decimales
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
        val = self.current_progress * 100.0
        text_val = f"{val:.2f}".replace('.', ',')
        self.label_widget.configure(text=f"{self.label_prefix}{text_val}%")
        
        # Calcular y actualizar ETA
        if self.eta_label and self.history:
            current_time = time.time()
            if current_time - self.last_eta_update > 1.0: # Actualizar ETA cada 1 segundo visualmente
                old_t, old_p = self.history[0]
                dt = current_time - old_t
                dp = self.target_progress - old_p
                
                if dt > 3 and dp > 0: # Solo estimar si tenemos al menos 3 seg de historial y hemos avanzado
                    rate = dp / dt
                    if rate > 0:
                        remaining_p = 1.0 - self.target_progress
                        eta_seconds = int(remaining_p / rate)
                        
                        mins, secs = divmod(eta_seconds, 60)
                        hours, mins = divmod(mins, 60)
                        
                        if hours > 0:
                            eta_str = f"Faltan ~{hours:02d}:{mins:02d}:{secs:02d}"
                        else:
                            eta_str = f"Faltan ~{mins:02d}:{secs:02d}"
                            
                        self.eta_label.configure(text=eta_str)
                elif dt > 1 and dp == 0 and self.target_progress > 0 and self.target_progress < 1.0:
                    pass # Evitar que el ETA desaparezca si se congela un momento
                else:
                    if self.target_progress >= 0.999:
                        self.eta_label.configure(text="")
                    elif not self.eta_label.cget("text"):
                        self.eta_label.configure(text="Calculando...")
                        
                self.last_eta_update = current_time
        
        if abs(self.current_progress - self.target_progress) < 0.00001:
            self.current_progress = self.target_progress
            self.is_animating = False
        else:
            self.root_widget.after(self.delay, self.animate)

