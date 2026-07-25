import tkinter as tk
from tkinter import messagebox
import sys

try:
    import customtkinter as ctk
except ImportError:
    messagebox.showerror("Error", "Faltan librerías. Ejecuta 'pip install customtkinter pillow'.")
    sys.exit(1)

from start_screen import StartScreen
from info_screen import InfoScreen
from explanation_screen import ExplanationScreen
from distro_selection_screen import DistroSelectionScreen
from distro_info_screen import DistroInfoScreen
from build_progress_screen import BuildProgressScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rookie Linux Developer - Terminal Mode")
        self.geometry("900x600")
        self.resizable(True, True)
        self.minsize(800, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Fondo negro sólido estilo terminal para toda la app
        self.container = ctk.CTkFrame(self, fg_color="#0a0a0a")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartScreen, InfoScreen, ExplanationScreen, DistroSelectionScreen, DistroInfoScreen, BuildProgressScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    app = App()
    app.mainloop()
