# Rookie Linux Develop — Documentación

> Herramienta de generación de imágenes ISO personalizadas para entornos de desarrollo Linux.

---

## ¿Qué es este proyecto?

**Rookie Linux Develop** es una aplicación de escritorio (Windows y Linux) que permite a cualquier persona — sin experiencia previa — generar una ISO de Linux completamente equipada para el desarrollo de software. La ISO resultante incluye IDEs, lenguajes de programación, bases de datos, herramientas de contenedores y configuraciones listas para usar desde el primer arranque.

La app guía al usuario de principio a fin: desde la selección de la distribución, pasando por la descarga y construcción de la imagen, hasta el flasheo del USB.

---

## Estructura de la documentación

```
docs/
├── README.md                           ← Estás aquí
├── LICENCIA.md                         ← Licencia MIT del proyecto
├── arquitectura/                       Explicaciones de cómo funciona el proyecto internamente
│   ├── ARQUITECTURA_BACKEND.md         Lógica de los scripts Bash y el sistema builder
│   ├── arquitectura-frontend.md        Cómo se comunican las pantallas Python (CTk)
│   └── flujo-creacion-iso.md           Cómo build_iso.sh inyecta preseed/kickstart
├── primeros-pasos/                     Para desarrolladores que quieran contribuir
│   ├── entorno-de-desarrollo.md        Cómo levantar main.py y sus dependencias
│   └── compilacion.md                  Cómo usar compile/ para generar los .rar
├── guias/                              Guías de uso y extensión del proyecto
│   ├── como-agregar-una-distro.md      Añadir nuevas distros en builder/templates/
│   ├── como-agregar-scripts.md         Sumar herramientas en scripts/
│   └── manejo-de-usb.md                Cómo funciona el flasher_worker
└── referencia/                         Referencia técnica estricta
    ├── distros-soportadas.md           Detalles de ISOs (versiones, preseed vs ks.cfg)
    ├── catalogo-de-scripts.md          Lista de todo lo instalable
    └── estructura-de-pantallas.md      Mapa de frontend/screens/
```

---

## Índice rápido

### 🏗 Arquitectura
- [Backend y Scripts](./arquitectura/ARQUITECTURA_BACKEND.md) — Cómo funcionan los scripts Bash
- [Frontend Python](./arquitectura/arquitectura-frontend.md) — Sistema de pantallas con CustomTkinter
- [Flujo de creación de ISO](./arquitectura/flujo-creacion-iso.md) — Inyección de preseed y kickstart

### 🚀 Primeros Pasos (Para Desarrolladores)
- [Entorno de desarrollo](./primeros-pasos/entorno-de-desarrollo.md) — Ejecutar el proyecto en local
- [Compilación y distribución](./primeros-pasos/compilacion.md) — Generar ejecutables con PyInstaller

### 📖 Guías
- [Agregar una distribución](./guias/como-agregar-una-distro.md) — Añadir Ubuntu, Fedora, etc.
- [Agregar scripts de instalación](./guias/como-agregar-scripts.md) — Nuevas herramientas en la ISO
- [Manejo del USB](./guias/manejo-de-usb.md) — Cómo funciona el flasheador en Linux y Windows
- [Instalación de WSL](./guias/instalacion-wsl.md) — Flujo de instalación en dos fases para Windows

### 📋 Referencia
- [Distros soportadas](./referencia/distros-soportadas.md) — Tabla de versiones e ISOs
- [Catálogo de scripts](./referencia/catalogo-de-scripts.md) — Todo lo que se instala
- [Mapa de pantallas](./referencia/estructura-de-pantallas.md) — Todas las pantallas del frontend

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| GUI | Python 3 + CustomTkinter + Pillow |
| Backend (construcción) | Bash (build_iso.sh, download_iso.sh) |
| Automatización de instalador | Cloud-Init (preseed) / Kickstart (ks.cfg) |
| Scripts post-arranque | Bash modular (`scripts/`) |
| Empaquetado | PyInstaller |
| Plataformas soportadas | Linux nativo · Windows (vía WSL) |

---

## Flujo de alto nivel

```
Usuario selecciona distro
         │
         ▼
download_iso.sh descarga la ISO oficial
         │
         ▼
build_iso.sh modifica la ISO:
  ├─ Inyecta preseed/kickstart (instalación desatendida)
  ├─ Inyecta scripts/ (configuración post-arranque)
  └─ Reempaqueta la ISO con xorriso
         │
         ▼
ISO personalizada guardada en output/
         │
         ▼
flasher_worker escribe la ISO en el USB
```

---

## ⚠️ Estado de las distribuciones

| Distribución | Estado |
|---|---|
| Ubuntu | ✅ Estable |
| Linux Mint | ✅ Estable |
| Pop!_OS | ✅ Estable |
| **Fedora** | 🚧 **En desarrollo** — La automatización vía Kickstart se encuentra en fase de pruebas. No se recomienda para uso en producción. |

---

## Nota sobre autoría y asistencia de IA

Este proyecto fue desarrollado con la asistencia de **inteligencia artificial (Google Gemini)** en múltiples aspectos:

- 📄 **Documentación**: La estructura, organización y redacción técnica de esta documentación.
- 🖥️ **Frontend**: El diseño de la interfaz gráfica, la lógica de navegación entre pantallas y los componentes visuales en Python/CustomTkinter.
- 💻 **Código fuente**: Partes del backend, scripts de construcción y la lógica de integración entre componentes.

Las ideas originales, los objetivos del proyecto, las decisiones de arquitectura y la dirección general son autoría del desarrollador.

Esta documentación refleja el estado del proyecto al momento de su generación. Se recomienda verificar directamente los archivos fuente ante cualquier duda técnica.
