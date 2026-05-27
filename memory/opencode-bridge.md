---
tags: [memory, ai]
date: 2026-05-27
---

# OpenCode Bridge — Fase 3

## Contexto

Puente entre OpenCode CLI y la vault de Obsidian. OpenCode ahora lee/escribe en la vault siguiendo un protocolo estricto al inicio/fin de cada sesión.

## Qué se creó

1. **Sync script** (`scripts/sync-memory.py`) — sincronización bidireccional entre JSONL memory stores y vault .md
2. **Protocolo de vault** en AGENTS.md — instrucciones detalladas para OpenCode al inicio/fin de sesión
3. **Import de sesiones** — los `.opencode-sessions/` se importan a `daily/` del vault

## Cómo funciona

```
OpenCode memory tools (JSONL)  ──sync-memory.py──▶  vault/memory/*.md
OpenCode sessions (.md)        ──import-sessions─▶  vault/daily/*.md
vault notes                    ──sync-memory.py──▶  stdout (JSONL)
```

## Flujo de sesión

1. **Inicio:** OpenCode revisa `projects/`, `memory/`, `daily/` para contexto
2. **Durante:** usa `memory` tools y escribe notas directamente en vault
3. **Fin:** corre `sync-memory.py to-vault` + escribe resumen en `daily/`

## Lecciones aprendidas

- El JSONL de memory tiene formato `{type, name, entityType, observations}`
- `sync-memory.py to-vault` transforma entities en notas con frontmatter YAML
- `import-sessions` adapta el formato legacy de `.opencode-sessions` a Obsidian

## Enlaces

- [[projects/second-brain-plan|Proyecto Segundo Cerebro]]
- [[skills/memory-bridge|Skill: Memory Bridge]]
- [[memory/gemini-bridge|Gemini Bridge — Fase 2]]
