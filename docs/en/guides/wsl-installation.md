# WSL (Windows Subsystem for Linux) Installer

This guide explains how the built-in WSL installation flow works for Windows users. Due to the evolution of the application, the installation system has been split into two distinct modes accessible from the `WslInstallScreen` screen.

---

## Why a WSL Installer?

Rookie Linux Develop requires Linux-exclusive tools (`xorriso`, `squashfs-tools`, etc.) to manipulate and rebuild the ISO image. To allow Windows users to generate the ISO natively without complex virtual machines, the application relies on a Linux subsystem using WSL.

## The Two Installation Modes

The system now offers two approaches, separated into two independent screens:

### Mode 1: Install to use the app (`WslAppInstallScreen`)
This is a simplified flow, ideal for users who just want to build their Rookie Linux ISO image and don't care about using Linux on Windows for other things.
It is divided into two manual steps (due to the need to restart):

1. **Phase 1: Enable WSL**: Silently and interactively executes the command:
   ```powershell
   wsl --install --no-distribution
   ```
   After this, the app warns via a dialog box that **the PC must be restarted**.

2. **Phase 2: Install Distro (Post-Restart)**: Once restarted, the user uses this second step to install the base distribution (Ubuntu) necessary for the backend operations without launching annoying consoles.
   ```powershell
   wsl --install -d Ubuntu --no-launch
   ```

The installations feature confirmation windows to alert about the need for administrator permissions and the time required.

### Mode 2: WSL as main system (`WslMainInstallScreen`)
This is an advanced dashboard for users who want to explore WSL further.

1. **System Status**: Asynchronously displays whether WSL, WSL 2, and virtualization are enabled on the system, detecting the default version via `wsl --status`.
2. **Global Enablement**: Allows you to install WSL with one click.
3. **Distribution Management**: Dynamically scans (`wsl -l -o` and `wsl -l -v`) to list all available distributions and those already installed.
4. Allows selecting one or multiple distributions and queuing them for visual installation with interactive progress bars based on simulation and threads.

---

## Automatic Validations and Monitoring

To ensure a smooth installation, both screens implement modern mechanisms:

- **Confirmation windows (msg_ask_yes_no)**: Prevent destructive actions or accidental installations.
- **Automatic redirection**: After completing the processes in App Mode, the user is returned to the main menu to avoid empty interactions.
- **Asynchronous Execution (Background Threads)**: All PowerShell commands (with `RunAs` or `Start-Process`) are executed in a separate thread, preventing the `CustomTkinter` GUI from freezing during lengthy installations.
