# WSL (Windows Subsystem for Linux) Installer

This guide explains how the built-in WSL installation flow (in the `WslInstallScreen`) works for Windows users who need to build ISOs.

---

## Why a WSL Installer?

Rookie Linux Develop requires Linux-exclusive tools (`xorriso` and `squashfs-tools`) to manipulate and rebuild the ISO image. To allow Windows users to generate the ISO directly from their primary operating system, the application automates the installation and configuration of a Linux subsystem (Ubuntu) using WSL (Windows Subsystem for Linux).

## Installation Architecture: The Two-Phase Flow

Installing WSL on a clean Windows system requires a mandatory operating system reboot after enabling the underlying features (Virtual Machine Platform). Therefore, the installation process was split into two sequential phases, entirely controlled by the frontend:

### Phase 1: Feature Enablement
1. The user clicks on "Install WSL".
2. The application silently and interactively executes the command:
   ```powershell
   wsl --install --no-distribution
   ```
3. Immediately after, PowerShell is invoked to enable the "VirtualMachinePlatform" feature:
   ```powershell
   Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
   ```
4. The application informs the user that **they must restart their PC** and provides a button to do it immediately or postpone it.

### Phase 2: Distribution Installation (Post-Reboot)
Once the user restarts their machine and reopens the application:
1. The installation screen checks the WSL status by running `wsl --status`.
2. If it detects that the features are already enabled but there is no default system, it automatically starts the second phase, which downloads and installs the "Ubuntu" distribution:
   ```powershell
   wsl --install -d Ubuntu
   ```
3. Finally, the application executes commands inside the new WSL environment to update repositories (`apt update`) and install the key dependencies for the app (`xorriso` and `squashfs-tools`).

---

## Automatic Validation and Monitoring

To ensure the installation does not fail or hang, the system runs real-time checks:

- **Command Detection:** Before starting, it verifies if the `wsl` command is available in the user's `PATH`.
- **Status Monitoring (`is_wsl_installed()`):** It runs continuous polling that checks if the default distribution is configured and responds to basic commands.
- **Asynchronous Execution (Background Threads):** All PowerShell and WSL commands are executed in a separate thread (`threading.Thread`). This captures `stdout` and `stderr` through `subprocess.Popen`, avoiding blocking the graphical interface (GUI) of `CustomTkinter` and allowing real-time console printing on the screen.
