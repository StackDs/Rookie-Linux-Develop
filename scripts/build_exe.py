import os
import sys
import shutil
import subprocess
import zipfile
import time

def force_remove_tree(path):
    """Elimina un directorio matando primero cualquier proceso que bloquee el exe."""
    if not os.path.exists(path):
        return
    # Cerrar el ejecutable si está corriendo para liberar el handle
    if os.name == 'nt':
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "Rookie-Linux-Builder.exe"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass
    time.sleep(1)
    # Intentar borrar; si falla usar rd /s /q (Windows) o rm -rf (Linux) como último recurso
    try:
        shutil.rmtree(path)
    except OSError:
        if os.name == 'nt':
            subprocess.run(["cmd", "/c", "rd", "/s", "/q", path], check=False)
        else:
            subprocess.run(["rm", "-rf", path], check=False)
        time.sleep(0.5)

def copy_folder_robust(src, dst):
    """Copia una carpeta usando robocopy si está disponible para mayor estabilidad."""
    if os.path.exists("C:\\Windows\\System32\\robocopy.exe"):
        # robocopy exit codes 0-7 son exitosos
        subprocess.run(["robocopy", src, dst, "/E", "/NP", "/R:3", "/W:5"], capture_output=True)
    else:
        shutil.copytree(src, dst)

def main():
    # Cambiar al directorio raiz del proyecto (un nivel arriba de scripts/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    print("Iniciando empaquetado de Rookie Linux Builder...")
    
    # 1. Instalar dependencias si faltan
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "customtkinter", "--break-system-packages"], check=False)
    
    # 2. Construir el ejecutable con PyInstaller
    print("Compilando con PyInstaller...")
    subprocess.run([
        sys.executable, "-m", "PyInstaller", 
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "Rookie-Linux-Builder",
        "frontend/main.py"
    ], check=True)
    
    # 3. Preparar directorio de distribucion
    dist_dir = "Rookie-Linux-Release"
    print(f"Preparando directorio de lanzamiento: {dist_dir}...")
    force_remove_tree(dist_dir)
    os.makedirs(dist_dir)
    
    # Mover el ejecutable
    exe_name = "Rookie-Linux-Builder.exe" if os.name == 'nt' else "Rookie-Linux-Builder"
    shutil.move(f"dist/{exe_name}", os.path.join(dist_dir, exe_name))
    
    # Copiar carpetas necesarias
    folders_to_copy = ["assets", "builder", "templates", "configs", "scripts"]
    for folder in folders_to_copy:
        if os.path.exists(folder):
            print(f"Copiando {folder}...")
            copy_folder_robust(folder, os.path.join(dist_dir, folder))
            
    # Crear carpetas vacias necesarias
    os.makedirs(os.path.join(dist_dir, "downloads", "iso"), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, "output"), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, "logs"), exist_ok=True)
    
    # 4. Crear el archivo RAR final en el Escritorio
    home_dir = os.environ.get("USERPROFILE", os.environ.get("HOME", ""))
    desktop_path = os.path.join(home_dir, "Escritorio") if os.path.exists(os.path.join(home_dir, "Escritorio")) else os.path.join(home_dir, "Desktop")
    
    rar_filename = os.path.join(desktop_path, "Rookie-Linux-Builder-Release.rar")
    
    print(f"Creando {rar_filename}...")
    
    # Check if rar is installed
    if shutil.which("rar"):
        # -ep1 excludes the base directory from the paths in the archive
        # -r recurses subdirectories
        # -y assumes yes (overwrites existing)
        subprocess.run(["rar", "a", "-ep1", "-r", "-y", rar_filename, dist_dir], check=True)
    else:
        print("Advertencia: El comando 'rar' no está instalado. Usando 'zip' como alternativa...")
        zip_filename = rar_filename.replace(".rar", ".zip")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dist_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dist_dir)
                    zipf.write(file_path, arcname)
                
    print("Limpiando carpetas temporales...")
    force_remove_tree(dist_dir)
    force_remove_tree("build")
    force_remove_tree("dist")
    if os.path.exists("Rookie-Linux-Builder.spec"):
        os.remove("Rookie-Linux-Builder.spec")
        
    print(f"¡Exito! Se ha creado el paquete en tu Escritorio.")
    print(f"Las carpetas residuales han sido limpiadas.")

if __name__ == "__main__":
    main()
