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
    def __init__(self, root_widget, progress_bar, label_widget, label_prefix="Progreso: ", step=0.005, delay=20):
        self.root_widget = root_widget
        self.progress_bar = progress_bar
        self.label_widget = label_widget
        self.label_prefix = label_prefix
        self.step = step
        self.delay = delay
        
        self.current_progress = 0.0
        self.target_progress = 0.0
        self.is_animating = False

    def update_progress(self, target_percent):
        self.target_progress = target_percent
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
        self.progress_bar.set(0.0)
        if text:
            self.label_widget.configure(text=text)
        else:
            self.label_widget.configure(text=f"{self.label_prefix}0,00%")
            
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
        
        if abs(self.current_progress - self.target_progress) < 0.00001:
            self.current_progress = self.target_progress
            self.is_animating = False
        else:
            self.root_widget.after(self.delay, self.animate)

