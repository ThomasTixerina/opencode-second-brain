---
tags: [guide, obsidian, plugins]
date: 2026-05-27
---

# Guía de Plugins de Obsidian

Este vault usa 5 plugins de la comunidad. A continuación su función y cómo se usan.

---

## 1. Dataview

**Propósito:** Motor de consultas para tratar el vault como una base de datos.

**Uso en este vault:**
- `_index.md` usa queries Dataview para listar notas por tipo (daily, memory, projects, references) automáticamente
- Las queries son tipo `LIST FROM "daily"` y `TABLE` con metadatos

**Instalación:** Community Plugins → buscar `Dataview` → Install → Enable

---

## 2. Templater

**Propósito:** Template engine avanzado que reemplaza templates core de Obsidian.

**Uso en este vault:**
- Carpeta `templates/` contiene 5 templates: `daily.md`, `memory.md`, `project.md`, `reference.md`, `skill.md`
- Se activa automáticamente al crear archivos nuevos (`trigger_on_file_creation: true`)
- Sintaxis `<% tp.* %>` para fechas, títulos, etc.

**Instalación:** Community Plugins → buscar `Templater` → Install → Enable

---

## 3. Kanban

**Propósito:** Tableros Kanban dentro de Obsidian (markdown-based).

**Uso en este vault:**
- `kanban/Proyectos Kanban.md` — tablero central de proyectos con Dataview queries embedidas
- Formato markdown con `- [ ]` para cards y `##` para columnas

**Instalación:** Community Plugins → buscar `Kanban` → Install → Enable

---

## 4. Omnisearch

**Propósito:** Búsqueda full-text mejorada sobre todo el vault.

**Uso en este vault:**
- Busca en todas las notas con peso por tipo de contenido (basename > h1 > h2 > h3)
- Muestra excerpts y path en resultados
- Atajo: `Ctrl+Shift+F`

**Instalación:** Community Plugins → buscar `Omnisearch` → Install → Enable

---

## 5. Excalidraw

**Propósito:** Dibujo y diagramas visuales dentro de Obsidian.

**Uso en este vault:**
- Diagramas guardados en `excalidraw/` (tema oscuro por defecto)
- Exportación embed para incluir en notas markdown
- Atajo: `Ctrl+Shift+D` (o click en ribbon icon)

**Instalación:** Community Plugins → buscar `Excalidraw` → Install → Enable

---

## Instalación paso a paso

1. ⚙️ **Settings** → **Community plugins**
2. Desactivar **Restricted mode** → Confirmar
3. Click **Browse** (junto a Restricted mode)
4. Buscar cada plugin por nombre (ver tabla arriba)
5. Click **Install** → luego **Enable**

Una vez instalados, los archivos `data.json` ya pre-configurados en `.obsidian/plugins/*/` se cargan automáticamente. No es necesario configurar nada más.
