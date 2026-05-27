---
tags: [skill, ai]
category: ai
---

# Memory Bridge — OpenCode ↔ Obsidian

## Descripción

Puente entre las `memory` tools de OpenCode (MCP memory server) y la vault de Obsidian. Permite que el conocimiento que OpenCode acumula en sesiones se refleje como notas en el segundo cerebro.

## Cuándo usarlo

- Al final de cada sesión de OpenCode
- Cuando se toma una decisión importante
- Cuando se aprende algo que debe persistir

## Cómo se implementa

1. OpenCode escribe notas `.md` directamente en `second-brain/memory/`
2. Las notas siguen el [[templates/memory|template de memoria]]
3. Obsidian las indexa automáticamente (están en la vault)
4. `memory-global` de OpenCode puede alimentarse leyendo la vault

## Relacionado con

- [[memory/_index|Memoria Persistente]]
- [[projects/second-brain-plan|Proyecto Segundo Cerebro]]

## Enlaces

- [[skills/_index|Todas las skills]]
