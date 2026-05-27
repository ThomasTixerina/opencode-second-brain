---
tags: [project]
status: active
started: 2026-05-27
---

# Proyecto: Segundo Cerebro Interconectado

## Objetivo

Conectar **Gemini CLI + OpenCode CLI + Obsidian** como un segundo cerebro unificado donde el conocimiento persiste, se relaciona y es accesible desde cualquier herramienta.

## Stack

- Obsidian (vault local markdown)
- Gemini CLI (Google AI)
- OpenCode CLI (asistente de código)
- n8n (automatización)
- GitHub (sincronización)

## Notas fundacionales

- [[references/video-obsidian-ia-memoria|Video 1: Obsidian + IA Memoria]]
- [[references/video-obsidian-desde-cero|Video 2: Obsidian desde cero]]

## Fases

- [x] **Fase 1** — Vault fundacional (estructura, templates, config)
- [x] **Fase 2** — Puente Gemini ↔ Obsidian
- [x] **Fase 3** — Puente OpenCode ↔ Obsidian
- [x] **Fase 4** — GitHub sync
- [x] **Fase 5** — Automatización con n8n
- [ ] **Fase 6** — Plugins estratégicos ⬅️

## Plugins instalados (Fase 6)

| Plugin | Propósito | Estado |
|--------|-----------|--------|
| Dataview | Motor de consultas SQL-like sobre el vault | ✅ Config listo |
| Templater | Sistema de templates avanzado (reemplaza core Templates) | ✅ Config listo |
| Kanban | Tableros visuales de proyectos | ✅ Config listo |
| Omnisearch | Búsqueda full-text mejorada | ✅ Config listo |
| Excalidraw | Dibujos y diagramas integrados | ✅ Config listo |

> **Nota:** Los plugins deben instalarse desde Community Plugins en Obsidian. Las configs pre-creadas se activan automáticamente al instalar.

## Tareas

- [x] Crear estructura de vault
- [x] Configurar .obsidian
- [x] Crear templates
- [x] Configurar GitHub repo
- [x] Escribir script Gemini-to-Obsidian
- [x] Conectar memory tools de OpenCode con vault
- [x] Crear Vault Gateway (webhook → GitHub)
- [x] Crear Daily Digest (cron → GitHub)
- [x] Configurar plugin data.json (Dataview, Templater, Kanban, Omnisearch, Excalidraw)
- [x] Convertir templates a Templater syntax
- [x] Agregar Dataview queries al MOC
- [x] Crear Kanban board ejemplo
- [ ] Abrir Obsidian → instalar los 5 plugins desde Community Plugins
- [ ] En Templater: configurar hotkey para insertar template (Ctrl+T por defecto)
- [ ] Verificar que `tp.date.now()` funciona correctamente en las templates

## Enlaces

- [[_index|Map of Content]]
- [[kanban/Proyectos Kanban|Tablero Kanban]]
