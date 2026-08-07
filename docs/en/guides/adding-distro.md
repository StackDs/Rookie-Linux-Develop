# How to add a new distribution

This guide explains the necessary steps to integrate a new Linux distribution into Rookie Linux Develop.

---

## Step 1: Decide on the automation strategy

Before creating files, you need to know which installer the target distro uses:

| Installer | Configuration | Distros that use it |
|---|---|---|
| **Subiquity** | Cloud-Init (`user-data`) | Ubuntu 20.04+, Pop!_OS |
| **Ubiquity** | preseed.cfg | Ubuntu 18.04, Linux Mint (Cinnamon) |
| **Anaconda** | Kickstart (`ks.cfg`) | Fedora, RHEL, CentOS |
| **Calamares** | Custom script | Manjaro, Garuda, EndeavourOS |

> 💡 If the distro uses Calamares, automation is more complex and requires modifying the Calamares `settings.conf` file.

---

## Step 2: Add download logic

Edit `builder/download_iso.sh` and add a new `case` in the `resolve_iso_source()` function:

```bash
my_distro)
    MY_DISTRO_VERSION="${MY_DISTRO_VERSION:-1.0}"
    ISO_NAME="${ISO_NAME:-my-distro-${MY_DISTRO_VERSION}-x86_64.iso}"
    ISO_URL="${ISO_URL:-https://mirror.my-distro.org/releases/${MY_DISTRO_VERSION}/${ISO_NAME}}"
    ;;
```

> 💡 If the download URL changes with each version (like Ubuntu or Fedora), add scraping logic. Check the `ubuntu` or `fedora` blocks as a reference.

---

## Step 3: Create the templates folder

Create the templates folder with the exact name you will use internally:

```bash
mkdir builder/templates/my_distro
```

### For Cloud-Init based distributions (Ubuntu/Pop!_OS):

Create `builder/templates/my_distro/user-data`:

```yaml
#cloud-config
autoinstall:
  version: 1
  locale: en_US
  keyboard:
    layout: us
  identity:
    hostname: rookie-linux
    username: developer
    password: "$6$..."  # Hashed password with openssl passwd -6
  storage:
    layout:
      name: lvm
  late-commands:
    - cp -r /cdrom/custom_scripts /target/opt/rookie
    - chmod +x /target/opt/rookie/install.sh
    - echo "@reboot root bash /opt/rookie/install.sh" >> /target/etc/cron.d/rookie-setup
```

Create `builder/templates/my_distro/meta-data` (can be empty):

```yaml
instance-id: rookie-linux
```

### For Kickstart distributions (Fedora):

Create `builder/templates/my_distro/ks.cfg`:

```kickstart
#version=RHEL9
lang en_US.UTF-8
keyboard --xlayouts='us'
timezone America/Bogota --utc
rootpw --lock
user --name=developer --password=rookielinux --groups=wheel

%packages
@^workstation-product-environment
%end

%post
cp -r /run/install/repo/custom_scripts /opt/rookie
chmod +x /opt/rookie/install.sh
%end
```

---

## Step 4: Add build logic in `build_iso.sh`

Add a new `elif` block in `build_iso.sh` to handle the specific injection for your distro:

```bash
elif [ "$ISO_DISTRO" = "my_distro" ]; then
    echo "=> Preparing Cloud-Init config for My Distro..."
    cp "$TEMPLATES_DIR/user-data" "$EXTRACT_DIR/nocloud/"
    cp "$TEMPLATES_DIR/meta-data" "$EXTRACT_DIR/nocloud/"
    
    echo "=> Extracting and modifying GRUB..."
    xorriso -osirrox on -indev "$ISO_PATH" -extract /boot/grub/grub.cfg "$EXTRACT_DIR/grub.cfg" 2>/dev/null || true
    sed -i 's/---/autoinstall ds=nocloud\\;s=\/cdrom\/nocloud\/ ---/g' "$EXTRACT_DIR/grub.cfg"
```

---

## Step 5: Register the distro in the frontend

### 5a. In `DistroSelectionScreen`
Add the new distro to the radio button options list:

```python
# In frontend/screens/linux_concepts/distro_selection_screen.py
self.distros = ["Ubuntu", "Linux Mint", "Fedora", "Pop!_OS", "My Distro"]
```

### 5b. In `DistroInfoScreen`
Add the informative text and folder mapping:

```python
self.folder_map = {
    ...
    "My Distro": "my_distro_screenshots",
}

self.distro_texts = {
    ...
    "My Distro": (
        "> Analyzing: My Distro\n\n"
        "Distro description..."
    )
}
```

### 5c. In `BuildProgressScreen`
Add the name-to-internal-identifier mapping:

```python
distro_map = {
    ...
    "My Distro": "my_distro",
}
```

---

## Step 6: Add screenshots (optional)

Create the `assets/DistrosScreenShots/my_distro/` folder and add three images:
- `escritorio.png` — Main desktop view
- `gestor.png` — Package or file manager
- `terminal.png` — Open terminal

Images are displayed in `DistroInfoScreen` when the user selects this distro.

---

## Step 7: Test

1. Run `python3 frontend/main.py` and verify the new distro appears in the selector.
2. Test the full flow with download (may take several minutes).
3. If you have a VM available, boot the generated ISO to verify the unattended installation works.
