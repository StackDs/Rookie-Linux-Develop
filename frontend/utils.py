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
