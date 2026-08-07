# USB Management (Flasher)

This guide explains the USB flashing system: how it works internally, why the "separate worker" architecture exists, and how it differs between Linux and Windows.

---

## Why a separate process?

Writing an ISO to a disk requires **administrator privileges** (root on Linux, Administrator on Windows). However, the GUI application does not run with these permissions by default (nor should it).

The solution is a **separate worker process** that runs with elevated permissions, isolated from the GUI:

```
GUI (normal user)
    │
    ├── Launches: pkexec python3 flasher_worker_linux.py [args]
    │           or
    │           powershell Start-Process ... -Verb RunAs
    │
    └── Monitors: /tmp/rookie_flash_progress.json (polling every 100ms)

Worker (root/Administrator) — separate process
    │
    ├── Cleans disk partitions
    ├── Writes ISO with dd (Linux) or DISKPART+dd (Windows)
    └── Writes progress to /tmp/rookie_flash_progress.json
```

Communication between the GUI and the worker is through a **temporary JSON file** in `/tmp/`. This avoids any security issues when passing data between processes with different privilege levels.

---

## Progress File Format

The `/tmp/rookie_flash_progress.json` file has this structure:

```json
{
  "status": "writing",
  "percent": 0.45,
  "text": "45.00",
  "error": ""
}
```

| Field | Possible Values | Description |
|---|---|---|
| `status` | `"cleaning"`, `"writing"`, `"done"`, `"error"` | Current process status |
| `percent` | `0.0` – `1.0` | Progress percentage (0 to 1) |
| `text` | `"45.00"` | Formatted percentage text |
| `error` | `""` or message | Error details if `status == "error"` |

---

## Linux: `flasher_worker_linux.py`

### Tools used
- **`dd`**: To write the ISO at a low level to the USB device.
- **`wipefs`**: To erase all signatures from the previous filesystem.
- **`parted`**: To delete the partition table and create a new blank one.
- **`pkexec`**: To request root permissions from the user via a graphical dialog.

### Complete Cleaning Process

Before writing the ISO, the worker performs a **deep clean** of the USB to avoid the "reserved space from previous partitions" issue:

```bash
# 1. Unmount all USB partitions
umount /dev/sdX* 2>/dev/null

# 2. Erase all signatures and filesystems
wipefs -a /dev/sdX

# 3. Delete partition table (create a new empty GPT)
parted -s /dev/sdX mklabel gpt

# 4. Sync with kernel
partprobe /dev/sdX
```

### Writing with dd

```bash
dd if=/path/to/image.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

The worker monitors the `dd` output to extract the percentage and writes it to the JSON file.

### How USBs are detected in Linux

The `UsbFlashScreen` executes:

```bash
lsblk -J -o NAME,SIZE,TYPE,RM,MODEL
```

And filters devices where `TYPE == "disk"` and `RM == 1` (removable). The `RM` field identifies if the device is removable (USB) vs internal disks.

---

## Windows: `flasher_worker_windows.py`

### Tools used
- **DISKPART**: To clean the disk and create partitions.
- **`dd` for Windows**: To write the ISO (requires it to be available in `PATH` or `%TEMP%`).
- **PowerShell** with `-Verb RunAs`: To elevate privileges.

### Complete Cleaning Process

```powershell
# DISKPART script to clean the USB:
select disk N
clean all    ← Cleans all disk space
convert mbr
create partition primary
format fs=fat32 quick label="USB"
active
assign
```

### How USBs are detected in Windows

A PowerShell script is executed that calls `Get-Disk` and filters disks by:
- `BusType == "USB"` — USB disks only
- `IsSystem == $false` — Excludes the OS disk

---

## Flash Cancellation

The user can cancel during the process. Cancellation works via a **signal file**:

1. The GUI creates the `rookie_flash_cancel.flag` file in the temporary directory.
2. The worker periodically checks if this file exists.
3. If it exists, the worker stops, cleans up what it can, and terminates.

---

## FAQ

### Why is the USB "smaller" after flashing?

When an ISO is written to a USB with `dd`, the USB adopts the ISO's partition structure. A typical Linux ISO has only a 3-5 GB partition, even if the USB is 32 GB. To recover all space, the USB must be reformatted later.

### Why do a full clean before each flash?

If the same USB is flashed multiple times without cleaning, previous "ghost" partitions remain and the system adds them to the total size of the next ISO. After several flashes, the USB may run out of usable space even if the ISO is small. Deep cleaning before each write solves this issue.

### Is it safe for other system disks?

Yes. The USB selector only shows removable devices (`RM=1` on Linux, `BusType=USB` on Windows). Internal computer disks do not appear in the list.
