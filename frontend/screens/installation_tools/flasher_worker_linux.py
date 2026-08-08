import os
import sys
import tempfile
import argparse
import subprocess
import json
import traceback
import time

def write_progress(file_path, status, percent=0, text="", error=""):
    data = {
        "status": status,
        "percent": percent,
        "text": text,
        "error": error
    }
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="USB Flasher Worker (Linux)")
    parser.add_argument("--iso", required=True, help="Path to ISO file")
    parser.add_argument("--drive", required=True, type=str, help="Device path like /dev/sdb")
    parser.add_argument("--progress", required=True, help="Path to progress JSON file")
    parser.add_argument("--worker-linux", action="store_true", help="Internal flag when running from packaged executable")
    args = parser.parse_args()
    
    prog_file = args.progress
    drive_path = args.drive
    iso_path = args.iso
    
    write_progress(prog_file, "cleaning", 0, "Preparando disco y desmontando particiones...")
    
    try:
        # Asegurarnos de que tenemos root
        if os.geteuid() != 0:
            raise PermissionError("El worker de Linux debe ejecutarse como root (uid=0).")
            
        # Desmontar cualquier particion montada del disco destino
        # Buscamos particiones como /dev/sdb1, /dev/sdb2, etc.
        try:
            lsblk_out = subprocess.check_output(['lsblk', '-lno', 'NAME', drive_path], text=True)
            for line in lsblk_out.splitlines():
                part = line.strip()
                if part and part != os.path.basename(drive_path):
                    part_path = f"/dev/{part}"
                    subprocess.run(['umount', '-f', part_path], stderr=subprocess.DEVNULL)
        except Exception as e:
            pass
            
        # Limpiar tabla de particiones vieja profundamente para evitar volúmenes "zombies"
        try:
            subprocess.run(['wipefs', '-a', drive_path], check=False)
            # Destruir MBR/GPT escribiendo ceros en los primeros 16MB
            subprocess.run(['dd', 'if=/dev/zero', f'of={drive_path}', 'bs=1M', 'count=16'], stderr=subprocess.DEVNULL)
            # Crear tabla de particiones completamente nueva y vacía
            subprocess.run(['parted', '-s', drive_path, 'mklabel', 'msdos'], stderr=subprocess.DEVNULL)
        except:
            pass
            
        write_progress(prog_file, "writing", 0, "0")
        
        # DD Write
        iso_size = os.path.getsize(iso_path)
        chunk_size = 1024 * 1024 * 4  # 4 MB chunks (optimo para Linux)
        written = 0
        
        cancel_flag = os.path.join(tempfile.gettempdir(), "rookie_flash_cancel.flag")
        
        last_sync = 0
        
        with open(iso_path, 'rb') as f_in, open(drive_path, 'wb') as f_out:
            while True:
                if os.path.exists(cancel_flag):
                    write_progress(prog_file, "error", percent, text_val, "Flasheo cancelado por el usuario.")
                    return
                    
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                    
                f_out.write(chunk)
                written += len(chunk)
                
                percent = written / iso_size
                text_val = f"{percent * 100:.2f}".replace('.', ',')
                write_progress(prog_file, "writing", percent, text_val)
                
                # Sincronizar físicamente al USB cada ~100MB para que la barra de progreso sea real
                if written - last_sync >= 100 * 1024 * 1024:
                    f_out.flush()
                    os.fsync(f_out.fileno())
                    last_sync = written
                
            write_progress(prog_file, "writing", 1.0, "100,00")
            f_out.flush()
            os.fsync(f_out.fileno())
            
        # Sincronizar el sistema de archivos del kernel
        subprocess.run(['sync'])
        write_progress(prog_file, "done", 1.0, "100,00")
        
    except PermissionError as e:
        write_progress(prog_file, "error", 0, "", f"Error de Permisos: {str(e)}")
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        write_progress(prog_file, "error", 0, "", error_msg)

if __name__ == "__main__":
    main()
