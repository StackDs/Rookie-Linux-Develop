import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

def ejecutar_script():
    try:
        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "script_herramienta.py")
        
        # Ejecutar el script usando el mismo intérprete de Python
        resultado = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            messagebox.showinfo("Éxito", f"Script ejecutado correctamente:\n\n{resultado.stdout}")
        else:
            messagebox.showerror("Error", f"Hubo un error al ejecutar el script:\n\n{resultado.stderr}")
            
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Frontend de Herramientas")
ventana.geometry("400x250")
ventana.configure(padx=20, pady=20)

# Título
titulo = tk.Label(ventana, text="Panel de Control", font=("Arial", 16, "bold"))
titulo.pack(pady=(0, 20))

# Descripción
descripcion = tk.Label(ventana, text="Haz clic en el botón para ejecutar el script\nde la herramienta.", justify="center")
descripcion.pack(pady=(0, 20))

# Botón
boton_ejecutar = tk.Button(ventana, text="Ejecutar Herramienta", command=ejecutar_script, 
                           bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                           padx=10, pady=5, cursor="hand2")
boton_ejecutar.pack()

# Iniciar el bucle de la aplicación
ventana.mainloop()
