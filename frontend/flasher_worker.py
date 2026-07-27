import os
import sys
import tempfile
import argparse
import subprocess
import json
import traceback
import tempfile
import ctypes
from ctypes.wintypes import DWORD, HANDLE
import msvcrt

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
    parser = argparse.ArgumentParser(description="USB Flasher Worker")
    parser.add_argument("--iso", required=True, help="Path to ISO file")
    parser.add_argument("--drive", required=True, type=int, help="PhysicalDrive Number")
    parser.add_argument("--progress", required=True, help="Path to progress JSON file")
    parser.add_argument("--worker", action="store_true", help="Internal flag when running from packaged exe")
    args = parser.parse_args()
    
    prog_file = args.progress
    drive_num = args.drive
    iso_path = args.iso
    
    write_progress(prog_file, "cleaning", 0, "Preparando disco...")
    
    try:
        # Diskpart clean con reintentos y clear readonly
        dp_script = f"select disk {drive_num}\nattributes disk clear readonly\nclean\n"
        dp_path = os.path.join(tempfile.gettempdir(), "dp_clean_worker.txt")
        
        for attempt in range(3):
            with open(dp_path, "w") as f:
                f.write(dp_script)
                
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            res = subprocess.run(["diskpart", "/s", dp_path], capture_output=True, text=True, creationflags=creationflags)
            
            if res.returncode == 0:
                break
            
            import time
            time.sleep(1.5)
            
        try:
            os.remove(dp_path)
        except: pass
        
        if res.returncode != 0:
            write_progress(prog_file, "error", 0, "", f"Diskpart error (Acceso denegado). Asegúrate de cerrar cualquier ventana del Explorador de Windows que esté viendo el USB.\nDetalles:\n{res.stdout}")
            return
            
        write_progress(prog_file, "writing", 0, "0")
        
        # DD Write
        drive_path = rf"\\.\PhysicalDrive{drive_num}"
        iso_size = os.path.getsize(iso_path)
        chunk_size = 1024 * 1024 * 1  # 1 MB chunks
        written = 0
        
        cancel_flag = os.path.join(tempfile.gettempdir(), "rookie_flash_cancel.flag")
        
        FSCTL_LOCK_VOLUME = 0x00090018
        FSCTL_DISMOUNT_VOLUME = 0x00090020
        
        with open(iso_path, 'rb') as f_in, open(drive_path, 'r+b', buffering=0) as f_out:
            # Bloquear el disco físico para evitar que Windows intente montarlo
            # a mitad de escritura (lo cual invalida nuestro handle y causa Errno 9).
            try:
                hDrive = msvcrt.get_osfhandle(f_out.fileno())
                bytes_returned = DWORD()
                ctypes.windll.kernel32.DeviceIoControl(
                    HANDLE(hDrive), FSCTL_LOCK_VOLUME, None, 0, None, 0, ctypes.byref(bytes_returned), None
                )
                ctypes.windll.kernel32.DeviceIoControl(
                    HANDLE(hDrive), FSCTL_DISMOUNT_VOLUME, None, 0, None, 0, ctypes.byref(bytes_returned), None
                )
            except Exception as e:
                pass # Si falla el bloqueo, continuamos y esperamos que Windows no moleste.

            # Leer el primer chunk (MBR/GPT) pero NO escribirlo aún.
            first_chunk = f_in.read(chunk_size)
            if first_chunk:
                # Escribimos ceros en el disco para avanzar el puntero, o hacemos seek
                # Hacemos seek en el disco destino para saltarnos el primer chunk
                f_out.seek(len(first_chunk))
                written += len(first_chunk) # Simulamos que ya se escribió para el %

            while True:
                if os.path.exists(cancel_flag):
                    write_progress(prog_file, "error", percent, text_val, "Flasheo cancelado por el usuario.")
                    return
                    
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                
                original_len = len(chunk)
                
                # Windows requiere alineamiento de sectores. Rellenamos el último chunk.
                if original_len % 4096 != 0:
                    padding_size = 4096 - (original_len % 4096)
                    chunk += b'\0' * padding_size
                    
                f_out.write(chunk)
                written += original_len
                
                percent = written / iso_size
                text_val = f"{percent * 100:.2f}".replace('.', ',')
                write_progress(prog_file, "writing", percent, text_val)
            
            # Al final, volver al inicio y escribir el primer chunk! (Magia anti-Windows)
            if first_chunk:
                f_out.seek(0)
                original_len = len(first_chunk)
                if original_len % 4096 != 0:
                    padding_size = 4096 - (original_len % 4096)
                    first_chunk += b'\0' * padding_size
                f_out.write(first_chunk)

            # Forzar que todos los datos lleguen al USB físicamente
            write_progress(prog_file, "writing", 1.0, "100,00")
            f_out.flush()
            os.fsync(f_out.fileno())
                
        write_progress(prog_file, "done", 1.0, "100,00")
        
    except PermissionError:
        write_progress(prog_file, "error", 0, "", "Error de Permisos. Windows bloqueó el acceso físico.")
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        write_progress(prog_file, "error", 0, "", error_msg)

if __name__ == "__main__":
    main()
