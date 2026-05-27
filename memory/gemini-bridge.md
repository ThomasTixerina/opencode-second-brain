---
tags: [memory, ai]
date: 2026-05-27
---

# Gemini Bridge — Fase 2

## Contexto

Puente entre Gemini CLI y la vault de Obsidian implementado como una Gemini CLI skill + script Python.

## Qué se creó

1. **Gemini skill `second-brain`** — habilita a Gemini CLI para leer/escribir/buscar en la vault
2. **Bridge script** (`scripts/bridge.py`) — CLI tool con comandos: `read`, `write`, `search`, `daily`, `list`, `template`
3. **Batch shortcut** (`scripts/bridge.bat`) — acceso rápido desde terminal

## Cómo usarlo

- Gemini CLI detecta automáticamente la skill `second-brain` cuando el contexto lo requiere
- Bridge script: `python scripts/bridge.py <command>`
- Gemini CLI headless mode: `gemini -p "tu prompt con contexto de vault"`

## Alternativas consideradas

- **Gemini Extension** — más complejo, requiere Node.js. Skill es más simple y directo
- **MCP Server** — sobreingeniería para lectura/escritura de archivos
- **Python API directa** — menos integración con el ecosistema Gemini CLI

## Lecciones aprendidas

- Las skills de Gemini CLI se instalan como un solo `SKILL.md` en `~/.gemini/skills/<name>/`
- El bridge script necesita `PYTHONIOENCODING=utf-8` en Windows por los emojis
- La vault es accesible desde cualquier herramienta porque es markdown plano

## Enlaces

- [[projects/second-brain-plan|Proyecto Segundo Cerebro]]
- [[skills/memory-bridge|Skill: Memory Bridge]]
