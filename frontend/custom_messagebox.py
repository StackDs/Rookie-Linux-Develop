import customtkinter as ctk

# Referencia global a la ventana principal de la app.
# Se registra desde main.py una vez que App() está construida.
_app_root = None

def register_app_window(app_instance):
    """Registra la ventana principal para que los diálogos puedan centrarse sobre ella."""
    global _app_root
    _app_root = app_instance

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, title, message, msg_type="info", width=550, height=350):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        # Make it modal
        self.transient(self.master)
        self.grab_set()

        # Centrar sobre la ventana principal usando la referencia global
        self.update_idletasks()
        try:
            root = _app_root
            if root is not None:
                root.update_idletasks()
                rx = root.winfo_x()
                ry = root.winfo_y()
                rw = root.winfo_width()
                rh = root.winfo_height()
                x = rx + (rw // 2) - (width // 2)
                y = ry + (rh // 2) - (height // 2)
            else:
                x = (self.winfo_screenwidth() // 2) - (width // 2)
                y = (self.winfo_screenheight() // 2) - (height // 2)

            # Asegurar que no se salga de los bordes de la pantalla
            x = max(0, x)
            y = max(0, y)
            self.geometry(f"+{int(x)}+{int(y)}")
        except Exception:
            pass  # Fallback silencioso

        self.configure(fg_color="#0a0a0a")

        self.result = None

        # Setup colors based on type
        title_color = "#00FF00"
        if msg_type == "error":
            title_color = "#FF0000"
        elif msg_type == "warning":
            title_color = "#FFAA00"

        lbl_title = ctk.CTkLabel(self, text=f">_ {title}", text_color=title_color, font=ctk.CTkFont(family="Consolas", size=20, weight="bold"))
        lbl_title.pack(pady=(20, 10))

        lbl_msg = ctk.CTkLabel(self, text=message, text_color="#00E676", font=ctk.CTkFont(family="Consolas", size=14), wraplength=width - 50, justify="center")
        lbl_msg.pack(pady=(10, 20), padx=20, expand=True)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        if msg_type == "askyesno":
            btn_yes = ctk.CTkButton(btn_frame, text="Sí", command=self.on_yes,
                                    width=100, height=35, fg_color="transparent", border_width=2,
                                    border_color="#008800", text_color="#00FF00", hover_color="#002200",
                                    font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
            btn_yes.pack(side="left", padx=10)

            btn_no = ctk.CTkButton(btn_frame, text="No", command=self.on_no,
                                    width=100, height=35, fg_color="transparent", border_width=2,
                                    border_color="#880000", text_color="#FF0000", hover_color="#220000",
                                    font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
            btn_no.pack(side="left", padx=10)
        else:
            btn_ok = ctk.CTkButton(btn_frame, text="Aceptar", command=self.on_ok,
                                    width=120, height=35, fg_color="transparent", border_width=2,
                                    border_color=title_color, text_color=title_color, hover_color="#111111",
                                    font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
            btn_ok.pack()

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()

    def on_ok(self):
        self.result = True
        self.destroy()


def msg_show_info(title, message, width=500, height=300):
    dialog = CustomMessageBox(title, message, "info", width, height)
    dialog.wait_window()
    return dialog.result

def msg_show_error(title, message, width=500, height=300):
    dialog = CustomMessageBox(title, message, "error", width, height)
    dialog.wait_window()
    return dialog.result

def msg_show_warning(title, message, width=500, height=300):
    dialog = CustomMessageBox(title, message, "warning", width, height)
    dialog.wait_window()
    return dialog.result

def msg_ask_yes_no(title, message, width=550, height=350):
    dialog = CustomMessageBox(title, message, "askyesno", width, height)
    dialog.wait_window()
    return dialog.result
