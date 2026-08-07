# Manejo del USB (Flasher)

Esta guía explica el sistema de flasheo de USBs: cómo funciona internamente, por qué existe la arquitectura de "worker separado" y cómo difiere entre Linux y Windows.

---

## ¿Por qué un proceso separado?

Escribir una ISO en un disco requiere **privilegios de administrador** (root en Linux, Administrador en Windows). Sin embargo, la aplicación GUI no se ejecuta con estos permisos por defecto (ni debería).

La solución es un **proceso worker separado** que se ejecuta con permisos elevados, aislado de la GUI:

```
GUI (usuario normal)
    │
    ├── Lanza: pkexec python3 flasher_worker_linux.py [args]
    │           o
    │           powershell Start-Process ... -Verb RunAs
    │
    └── Monitorea: /tmp/rookie_flash_progress.json (polling cada 100ms)

Worker (root/Administrador) — proceso separado
    │
    ├── Limpia particiones del disco
    ├── Escribe la ISO con dd (Linux) o DISKPART+dd (Windows)
    └── Escribe progreso en /tmp/rookie_flash_progress.json
```

La comunicación entre la GUI y el worker es a través de un **archivo JSON temporal** en `/tmp/`. Esto evita cualquier problema de seguridad al pasar datos entre procesos de diferente nivel de privilegio.

---

## Formato del archivo de progreso

El archivo `/tmp/rookie_flash_progress.json` tiene esta estructura:

```json
{
  "status": "writing",
  "percent": 0.45,
  "text": "45,00",
  "error": ""
}
```

| Campo | Valores posibles | Descripción |
|---|---|---|
| `status` | `"cleaning"`, `"writing"`, `"done"`, `"error"` | Estado actual del proceso |
| `percent` | `0.0` – `1.0` | Porcentaje de progreso (0 a 1) |
| `text` | `"45,00"` | Texto del porcentaje formateado |
| `error` | `""` o mensaje | Detalle del error si `status == "error"` |

---

## Linux: `flasher_worker_linux.py`

### Herramientas usadas
- **`dd`**: Para escribir la ISO a bajo nivel en el dispositivo USB.
- **`wipefs`**: Para borrar todas las firmas del sistema de archivos previo.
- **`parted`**: Para eliminar la tabla de particiones y crear una nueva en blanco.
- **`pkexec`**: Para solicitar permisos de root al usuario mediante un diálogo gráfico.

### Proceso de limpieza completa

Antes de escribir la ISO, el worker realiza una **limpieza profunda** del USB para evitar el problema de "espacio reservado de particiones previas":

```bash
# 1. Desmontar todas las particiones del USB
umount /dev/sdX* 2>/dev/null

# 2. Borrar todas las firmas y sistemas de archivos
wipefs -a /dev/sdX

# 3. Eliminar tabla de particiones (crear nueva GPT vacía)
parted -s /dev/sdX mklabel gpt

# 4. Sincronizar con el kernel
partprobe /dev/sdX
```

### Escritura con dd

```bash
dd if=/ruta/a/imagen.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

El worker monitorea la salida de `dd` para extraer el porcentaje y lo escribe en el JSON.

### Cómo se detectan los USBs en Linux

La pantalla `UsbFlashScreen` ejecuta:

```bash
lsblk -J -o NAME,SIZE,TYPE,RM,MODEL
```

Y filtra los dispositivos donde `TYPE == "disk"` y `RM == 1` (removibles). El campo `RM` identifica si el dispositivo es extraíble (USB) frente a discos internos.

---

## Windows: `flasher_worker_windows.py`

### Herramientas usadas
- **DISKPART**: Para limpiar el disco y crear particiones.
- **`dd` para Windows**: Para escribir la ISO (requiere que esté disponible en `PATH` o en `%TEMP%`).
- **PowerShell** con `-Verb RunAs`: Para elevar privilegios.

### Proceso de limpieza completa

```powershell
# Script DISKPART para limpiar el USB:
select disk N
clean all    ← Limpia todo el espacio del disco
convert mbr
create partition primary
format fs=fat32 quick label="USB"
active
assign
```

### Cómo se detectan los USBs en Windows

Se ejecuta un script PowerShell que llama a `Get-Disk` y filtra los discos por:
- `BusType == "USB"` — Solo discos USB
- `IsSystem == $false` — Excluye el disco del sistema operativo

---

## Cancelación del flasheo

El usuario puede cancelar durante el proceso. La cancelación funciona mediante un **archivo de señal**:

1. La GUI crea el archivo `rookie_flash_cancel.flag` en el directorio temporal.
2. El worker verifica periódicamente si este archivo existe.
3. Si existe, el worker se detiene, limpia lo que pueda y termina.

---

## Preguntas frecuentes

### ¿Por qué el USB queda "más pequeño" después de flashear?

Cuando se escribe una ISO en un USB con `dd`, el USB adopta la estructura de particiones de la ISO. Una ISO típica de Linux tiene solo una partición de 3-5 GB, aunque el USB sea de 32 GB. Para recuperar todo el espacio hay que reformatear el USB después.

### ¿Por qué se hace una limpieza completa antes de cada flasheo?

Si se flashea el mismo USB múltiples veces sin limpiar, las particiones previas quedan "fantasma" y el sistema las suma al tamaño total de la ISO siguiente. Después de varios flasheos el USB puede quedar sin espacio útil aunque la ISO sea pequeña. La limpieza profunda antes de cada escritura soluciona este problema.

### ¿Es seguro para otros discos del sistema?

Sí. El selector de USBs solo muestra dispositivos removibles (`RM=1` en Linux, `BusType=USB` en Windows). Los discos internos del equipo no aparecen en la lista.
