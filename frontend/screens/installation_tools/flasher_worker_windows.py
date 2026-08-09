import os
import sys
import tempfile
import argparse
import subprocess
import json
import traceback
import time
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

def run_diskpart(script_text):
    """Ejecuta un script de diskpart y retorna (ok, stdout)."""
    dp_path = os.path.join(tempfile.gettempdir(), "dp_clean_worker.txt")
    with open(dp_path, "w") as f:
        f.write(script_text)
    try:
        res = subprocess.run(
            ["diskpart", "/s", dp_path],
            capture_output=True, text=True,
            creationflags=0x08000000
        )
        stdout = res.stdout or ""
        # DiskPart siempre devuelve returncode=0, hay que analizar el texto.
        # Buscamos indicadores reales de error en la salida.
        error_phrases = [
            "no se encontró el objeto especificado",
            "objeto especificado no se encontró",
            "error",
            "failed",
            "not found",
            "acceso denegado",
        ]
        # Filtramos frases de error REALES, ignorando líneas de contexto que las mencionan
        lines = stdout.lower().splitlines()
        for line in lines:
            # Ignorar línea de copyright/encabezado
            if "microsoft" in line or "copyright" in line or "version" in line:
                continue
            for phrase in error_phrases:
                if phrase in line:
                    return False, stdout
        return True, stdout
    finally:
        try:
            os.remove(dp_path)
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description="USB Flasher Worker")
    parser.add_argument("--iso", required=True, help="Path to ISO file")
    parser.add_argument("--drive", required=True, type=int, help="PhysicalDrive Number")
    parser.add_argument("--progress", required=True, help="Path to progress JSON file")
    parser.add_argument("--worker-windows", action="store_true", help="Internal flag when running from packaged exe")
    args = parser.parse_args()

    prog_file = args.progress
    drive_num = args.drive
    iso_path = args.iso

    write_progress(prog_file, "cleaning", 0, "Preparando disco...")

    try:
        # ----------------------------------------------------------------
        # PASO 1: Limpiar el disco con DiskPart
        # NOTA: No usamos "offline disk / online disk" — esos comandos son
        # para discos internos SATA/NVMe. En USBs siempre lanza un error
        # del Servicio de Disco Virtual (VDS). Solo necesitamos "clean".
        # ----------------------------------------------------------------
        dp_script = (
            f"select disk {drive_num}\n"
            f"attributes disk clear readonly\n"
            f"clean\n"
        )

        ok = False
        last_stdout = ""
        for attempt in range(3):
            ok, last_stdout = run_diskpart(dp_script)
            if ok:
                break
            time.sleep(2)

        if not ok:
            # Segundo intento con un script más mínimo (solo clean, sin format)
            # por si Windows bloqueó el formateo pero no el borrado.
            dp_minimal = (
                f"select disk {drive_num}\n"
                f"clean\n"
            )
            ok, last_stdout = run_diskpart(dp_minimal)

        if not ok:
            write_progress(
                prog_file, "error", 0, "",
                f"DiskPart no pudo limpiar el disco.\n"
                f"Cierra el Explorador de Windows si está viendo el USB e inténtalo de nuevo.\n\n"
                f"Detalles:\n{last_stdout}"
            )
            return

        # Pequeña pausa para que Windows libere los handles del disco tras el format
        time.sleep(1.5)

        write_progress(prog_file, "writing", 0, "0")

        # ----------------------------------------------------------------
        # PASO 2: Escritura DD a bajo nivel con llamadas OS (os.open / os.write)
        # ----------------------------------------------------------------
        drive_path = rf"\\.\PhysicalDrive{drive_num}"
        iso_size = os.path.getsize(iso_path)
        chunk_size = 1024 * 1024  # 1 MB chunks
        written = 0
        last_sync = 0
        percent = 0.0
        text_val = "0,00"

        cancel_flag = os.path.join(tempfile.gettempdir(), "rookie_flash_cancel.flag")

        FSCTL_LOCK_VOLUME   = 0x00090018

        fd_in = None
        fd_out = None
        try:
            fd_in = os.open(iso_path, os.O_RDONLY | os.O_BINARY)
            fd_out = os.open(drive_path, os.O_RDWR | os.O_BINARY)
            
            # Intentar bloquear el disco físico para que Windows no interfiera
            try:
                hDrive = msvcrt.get_osfhandle(fd_out)
                bytes_returned = DWORD()
                ctypes.windll.kernel32.DeviceIoControl(
                    HANDLE(hDrive), FSCTL_LOCK_VOLUME,
                    None, 0, None, 0, ctypes.byref(bytes_returned), None
                )
            except Exception:
                pass

            # Leer el primer chunk (MBR/GPT) pero escribirlo AL FINAL
            first_chunk = os.read(fd_in, chunk_size)
            if first_chunk:
                os.lseek(fd_out, len(first_chunk), os.SEEK_SET)
                written += len(first_chunk)

            while True:
                if os.path.exists(cancel_flag):
                    write_progress(prog_file, "error", percent, text_val, "Flasheo cancelado por el usuario.")
                    return

                chunk = os.read(fd_in, chunk_size)
                if not chunk:
                    break

                original_len = len(chunk)
                if original_len % 4096 != 0:
                    padding_size = 4096 - (original_len % 4096)
                    chunk += b'\0' * padding_size

                os.write(fd_out, chunk)
                written += original_len

                percent = written / iso_size
                text_val = f"{percent * 100:.2f}".replace('.', ',')
                write_progress(prog_file, "writing", percent, text_val)

                # Sincronizar físicamente al USB cada ~64MB
                if written - last_sync >= 64 * 1024 * 1024:
                    os.fsync(fd_out)
                    last_sync = written

            # Escribir el primer chunk al inicio del disco
            if first_chunk:
                os.lseek(fd_out, 0, os.SEEK_SET)
                original_len = len(first_chunk)
                if original_len % 4096 != 0:
                    padding_size = 4096 - (original_len % 4096)
                    first_chunk += b'\0' * padding_size
                os.write(fd_out, first_chunk)

            write_progress(prog_file, "writing", 1.0, "100,00")
            os.fsync(fd_out)
        finally:
            if fd_in is not None:
                try: os.close(fd_in)
                except: pass
            if fd_out is not None:
                try: os.close(fd_out)
                except: pass

        write_progress(prog_file, "done", 1.0, "100,00")

    except PermissionError as e:
        write_progress(
            prog_file, "error", 0, "",
            f"Acceso denegado al disco físico.\n"
            f"Asegúrate de que la aplicación se ejecutó como Administrador.\n\n{e}"
        )
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        write_progress(prog_file, "error", 0, "", error_msg)

if __name__ == "__main__":
    main()
