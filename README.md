# 🧠 opencode-second-brain

**Un segundo cerebro portable para Obsidian + OpenCode + n8n**  
**A portable second brain for Obsidian + OpenCode + n8n**

---

## 🇪🇸 Español — ¿Qué es esto?

Este vault de Obsidian es un **segundo cerebro** listo para usar. Viene con:

- **5 plantillas** para notas diarias, proyectos, memoria, skills y referencias
- **Plugins preconfigurados** (Dataview, Templater, Kanban, Omnisearch, Excalidraw)
- **AGENTS.md** para que OpenCode/Gemini CLI lean y escriban tu cerebro automáticamente
- **Scripts puente** para sincronizar con OpenCode y Gemini
- **Workflows de n8n** (opcional) para automatizar desde la nube

> 💡 No necesitas saber programar para usarlo. Solo instalar Obsidian y 5 plugins.

### ⚡ Cómo empezar (5 pasos, sin programación)

| Paso | Acción |
|------|--------|
| **1** | [Descargar e instalar Obsidian](https://obsidian.md/download) |
| **2** | Clonar o descargar este repositorio:<br>• **Con git:** `git clone https://github.com/ThomasTixerina/opencode-second-brain.git`<br>• **Sin git:** Botón verde "Code" → "Download ZIP" → extraer |
| **3** | Abrir Obsidian → "Open folder as vault" → seleccionar la carpeta |
| **4** | Ir a Settings → Community Plugins → Browse → instalar y **habilitar** cada uno:<br>🔹 Dataview · 🔹 Templater · 🔹 Kanban · 🔹 Omnisearch · 🔹 Excalidraw |
| **5** | Presionar **Ctrl+T** dentro de cualquier nota para insertar una plantilla |

¡Listo! El vault ya funciona con todas las configuraciones incluidas.

### 🤖 Integración con OpenCode

Si usas [OpenCode CLI](https://opencode.ai):

```bash
opencode ruta/a/second-brain
```

OpenCode leerá automáticamente `AGENTS.md` y sabrá cómo navegar el vault, leer memorias, y sincronizar al finalizar cada sesión.

### 🌐 Automatización con n8n (opcional)

Dos workflows pre-hechos en `automation/`:

- **Vault Gateway** — Webhook para crear/actualizar archivos del vault remotamente
- **Daily Digest** — Lee la nota diaria del vault programadamente

**Para importarlos:** n8n → Settings → Import → From File → seleccionar `automation/*.workflow.json`

Cada workflow necesita que conectes tus propias credenciales (GitHub OAuth2).

### 📁 Estructura del vault

| Carpeta | Contenido |
|---------|-----------|
| `daily/` | Notas diarias (`YYYY-MM-DD.md`) |
| `projects/` | Proyectos activos |
| `memory/` | Memoria persistente (sincronizada con OpenCode) |
| `skills/` | Skills y patrones reutilizables |
| `references/` | Material de referencia externo |
| `templates/` | Plantillas Templater (5) |
| `attachments/` | Imágenes y archivos |
| `excalidraw/` | Diagramas y dibujos |
| `kanban/` | Tableros Kanban |
| `guides/` | Guías de uso |
| `automation/` | Workflows n8n exportados |
| `scripts/` | Scripts puente Python |

---

## 🇬🇧 English — What is this?

This Obsidian vault is a **second brain** ready to use out of the box. It includes:

- **5 templates** for daily notes, projects, memory, skills, and references
- **Pre-configured plugins** (Dataview, Templater, Kanban, Omnisearch, Excalidraw)
- **AGENTS.md** so OpenCode/Gemini CLI can read and write your brain automatically
- **Bridge scripts** for syncing with OpenCode and Gemini
- **n8n workflows** (optional) for cloud automation

> 💡 You don't need to know how to code. Just install Obsidian and 5 plugins.

### ⚡ Quick Start (5 steps, no coding)

| Step | Action |
|------|--------|
| **1** | [Download and install Obsidian](https://obsidian.md/download) |
| **2** | Clone or download this repo:<br>• **With git:** `git clone https://github.com/ThomasTixerina/opencode-second-brain.git`<br>• **Without git:** Green "Code" button → "Download ZIP" → extract |
| **3** | Open Obsidian → "Open folder as vault" → select the folder |
| **4** | Settings → Community Plugins → Browse → install and **enable** each:<br>🔹 Dataview · 🔹 Templater · 🔹 Kanban · 🔹 Omnisearch · 🔹 Excalidraw |
| **5** | Press **Ctrl+T** inside any note to insert a template |

That's it! The vault works with all configurations included.

### 🤖 OpenCode Integration

If you use [OpenCode CLI](https://opencode.ai):

```bash
opencode path/to/second-brain
```

OpenCode will automatically read `AGENTS.md` and know how to browse the vault, read memories, and sync at the end of each session.

### 🌐 n8n Automation (optional)

Two pre-built workflows in `automation/`:

- **Vault Gateway** — Webhook to create/update vault files remotely
- **Daily Digest** — Reads today's daily note on a schedule

**To import:** n8n → Settings → Import → From File → select `automation/*.workflow.json`

Each workflow needs your own credentials (GitHub OAuth2).

### 📁 Vault structure

| Folder | Content |
|--------|---------|
| `daily/` | Daily notes (`YYYY-MM-DD.md`) |
| `projects/` | Active projects |
| `memory/` | Persistent memory (synced from OpenCode) |
| `skills/` | Reusable skills & patterns |
| `references/` | External reference material |
| `templates/` | Templater templates (5) |
| `attachments/` | Images & files |
| `excalidraw/` | Diagrams & drawings |
| `kanban/` | Kanban boards |
| `guides/` | Usage guides |
| `automation/` | Exported n8n workflows |
| `scripts/` | Python bridge scripts |

---

## 📜 License

MIT — use freely, modify, share.
