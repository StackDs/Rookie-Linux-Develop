# Rookie Linux Develop — Documentation

> Custom ISO image generation tool for Linux development environments.

---

## What is this project?

**Rookie Linux Develop** is a desktop application (Windows and Linux) that allows anyone — with no prior experience — to generate a fully equipped Linux ISO for software development. The resulting ISO includes IDEs, programming languages, databases, container tools, and ready-to-use configurations right from the first boot.

The app guides the user from start to finish: from selecting the distribution, through downloading and building the image, to flashing the USB.

---

## Documentation Structure

```
docs/
├── README.md                           ← You are here
├── LICENSE.md                          ← Project MIT License
├── architecture/                       Explanations of how the project works internally
│   ├── BACKEND_ARCHITECTURE.md         Bash script logic and the builder system
│   ├── frontend-architecture.md        How Python screens (CTk) communicate
│   └── iso-creation-flow.md            How build_iso.sh injects preseed/kickstart
├── getting-started/                    For developers who want to contribute
│   ├── development-environment.md      How to start main.py and its dependencies
│   └── compilation.md                  How to use compile/ to generate .rar files
├── guides/                             Guides on how to use and extend the project
│   ├── adding-distro.md                Add new distros in builder/templates/
│   ├── adding-scripts.md               Add tools in scripts/
│   └── usb-management.md               How the flasher_worker works
└── reference/                          Strict technical reference
    ├── supported-distros.md            ISO details (versions, preseed vs ks.cfg)
    ├── script-catalog.md               List of everything installable
    └── screen-structure.md             Map of frontend/screens/
```

---

## Quick Index

### 🏗 Architecture
- [Backend and Scripts](./architecture/BACKEND_ARCHITECTURE.md) — How Bash scripts work
- [Python Frontend](./architecture/frontend-architecture.md) — Screen system with CustomTkinter
- [ISO Creation Flow](./architecture/iso-creation-flow.md) — Injection of preseed and kickstart

### 🚀 Getting Started (For Developers)
- [Development Environment](./getting-started/development-environment.md) — Run the project locally
- [Compilation and Distribution](./getting-started/compilation.md) — Generate executables with PyInstaller

### 📖 Guides
- [Add a Distribution](./guides/adding-distro.md) — Add Ubuntu, Fedora, etc.
- [Add Installation Scripts](./guides/adding-scripts.md) — New tools in the ISO
- [USB Management](./guides/usb-management.md) — How the flasher works on Linux and Windows

### 📋 Reference
- [Supported Distros](./reference/supported-distros.md) — Table of versions and ISOs
- [Script Catalog](./reference/script-catalog.md) — Everything that gets installed
- [Screen Map](./reference/screen-structure.md) — All frontend screens

---

## Tech Stack

| Layer | Technology |
|------|-----------|
| GUI | Python 3 + CustomTkinter + Pillow |
| Backend (build) | Bash (build_iso.sh, download_iso.sh) |
| Installer Automation | Cloud-Init (preseed) / Kickstart (ks.cfg) |
| Post-boot Scripts | Modular Bash (`scripts/`) |
| Packaging | PyInstaller |
| Supported Platforms | Native Linux · Windows (via WSL) |

---

## High Level Flow

```
User selects distro
         │
         ▼
download_iso.sh downloads official ISO
         │
         ▼
build_iso.sh modifies the ISO:
  ├─ Injects preseed/kickstart (unattended install)
  ├─ Injects scripts/ (post-boot config)
  └─ Repackages ISO with xorriso
         │
         ▼
Custom ISO saved in output/
         │
         ▼
flasher_worker writes ISO to USB
```

---

## ⚠️ Distributions Status

| Distribution | Status |
|---|---|
| Ubuntu | ✅ Stable |
| Linux Mint | ✅ Stable |
| Pop!_OS | ✅ Stable |
| **Fedora** | 🚧 **In development** — Kickstart automation is in testing phase. Not recommended for production use. |

---

## Note on Authorship and AI Assistance

This project was developed with the assistance of **artificial intelligence (Google Gemini)** in multiple aspects:

- 📄 **Documentation**: The structure, organization, and technical writing of this documentation.
- 🖥️ **Frontend**: The GUI design, screen navigation logic, and visual components in Python/CustomTkinter.
- 💻 **Source Code**: Parts of the backend, build scripts, and the integration logic between components.

The original ideas, project goals, architecture decisions, and overall direction are authored by the developer.

This documentation reflects the project's state at the time of generation. It is recommended to check the source files directly for any technical doubts.
