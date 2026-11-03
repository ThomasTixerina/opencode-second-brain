---
tags: [skill, ai]
category: ai
created: 2026-10-26
updated: 2026-10-26
---

# OpenCode Skills — Arquitecto y Revisor de Planes

## Descripción

Kit de skills instalado globalmente en `C:\Users\user\.config\opencode\skills\` (2026-10-26) para que un arquitecto revise y presione los planes que OpenCode genera antes de implementar. Dos orígenes:

| Skill | Origen | Qué hace | Cómo se activa |
|---|---|---|---|
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) (~300k stars, MIT) | Stub de invocación manual; llama a `grilling` | 🔴 Manual: `@grill-me` en el prompt (`disable-model-invocation: true`) |
| `grilling` | mattpocock/skills | Entrevista implacable en rondas: design tree, pregunta toda la "frontier" con respuesta recomendada; termina cuando no quedan supuestos sin resolver | 🟢 Automático (o `@grilling`) — se dispara con "gríllame", "stress-test", "presiona este plan" |
| `architect` | [garethrhughes/skills](https://github.com/garethrhughes/skills) (compatibilidad opencode) | Escribe propuesta formal en `docs/proposals/NNNN-titulo.md` con diagrama Mermaid, alternativas, impactos y Acceptance Criteria testables | 🟢 Automático (o `@architect`) |
| `reviewer` | garethrhughes/skills | Revisa feature doc → propuesta → código; seguridad, performance, IaC, observabilidad. Veredicto **PASS / PASS WITH COMMENTS / BLOCK** con severidades Blocker/Major/Minor y trazabilidad a Acceptance Criteria | 🟢 Automático (o `@reviewer`) |
| `decision-log` | garethrhughes/skills | Dueño único de los ADRs: los crea en `docs/decisions/` cuando una propuesta se acepta | 🟢 Automático — lo invoca `architect` tras aceptar la propuesta |

Dependencias copiadas junto a los skills: `RULES.md` + `rules/` (overlays `typescript.md` NestJS/Next y `dotnet.md`). El `reviewer` usa el overlay typescript por defecto si el `CLAUDE.md` del proyecto no declara `## Active Skillset`.

## Cuándo usarlo

- **Tareas grandes / cambios de arquitectura**: usar el flujo completo de 6 pasos (abajo).
- **Tareas pequeñas**: no invocar nada — los skills se auto-cargan solo si la tarea coincide.
- **Plan YA generado por OpenCode (plan mode)**: NO usar `grill-me` (interroga al usuario, no al plan); usar `@architect` ("revisa este plan y conviértelo en propuesta") o `@reviewer` (Fase 2 de su revisión).
- **Solo la idea, sin plan**: `@grill-me` en sesión fresca, plan mode apagado.

## Cómo se implementa

El flujo natural (el usuario no necesita invocar uno a uno — solo `grill-me` es manual):

```
1. @grill-me    → te interroga en rondas hasta cerrar TODO el árbol de decisiones
                  (sesión fresca, sin plan escrito todavía, plan mode apagado)
2. @architect   → convierte lo acordado en propuesta formal
                  docs/proposals/0001-titulo.md + diagrama Mermaid
3. TÚ           → lees la propuesta, la aceptas (Status: Accepted)
4. decision-log → se dispara solo → ADR en docs/decisions/
5. Implementas  (cualquier agente, normal)
6. @reviewer    → revisa propuesta + código → veredicto PASS / PASS WITH COMMENTS / BLOCK
```

**Convención de aviso (instrucción permanente en `~/.config/opencode/AGENTS.md`):** cuando el agente detecte y cargue automáticamente uno de estos skills, debe avisar en una línea qué skill se activó, qué hace y en qué punto del flujo estamos.

**Permisos opcionales** en `opencode.json`:

```jsonc
{
  "permissions": [
    { "action": "skill", "resource": "*", "effect": "allow" },
    { "action": "skill", "resource": "grill-me", "effect": "allow" }
  ]
}
```

## Relacionado con

- [[skills/memory-bridge|Memory Bridge — OpenCode ↔ Obsidian]]
- Entidad en memoria global: "OpenCode Skills Instalados"

## Enlaces

- [[skills/_index|Todas las skills]]
- Fuentes: https://github.com/mattpocock/skills · https://github.com/garethrhughes/skills · https://opencode.ai/v2/docs/skills
