import customtkinter as ctk

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
