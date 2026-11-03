---
tags: [log]
---

# Bitácora del Segundo Cerebro

> Registro cronológico de ingestas, consultas archivadas, lint passes y cambios al esquema.

## [2026-07-08] ingest | Super Second Brain ? Architecture & Implementation

Fuente: `super-second-brain-architecture.md` → `wiki/sources/super-second-brain-architecture.md`
Entidades: Andrej Karpathy
Conceptos: LLM Wiki, Human-in-the-loop ingestion, Structured JSON ingestion interface

## [2026-10-07] project | Trilogía Dentista Millonario

Proyecto nuevo: `clients/dr-tomas-tijerina/projects/dentista-millonario/`. Skill `nobel-bestseller-engine`. Tomo 1 "El arte de la Guerra Dental" (borrador exportado del Google Doc a `manuscritos/libro-1.md`); tomos 2 y 3 con índice semilla. Fase 0 (intake) iniciada.

## [2026-10-21] query-archive | MCP de Google Stitch — catálogo de herramientas

Instalados stitch (oficial, remoto) y stitch-local (@_davideast/stitch-mcp) en la config global de OpenCode. 16 tools oficiales + 3 exclusivas (build_site, get_screen_code, get_screen_image). Archivo: `wiki/synthesis/mcp-google-stitch-herramientas.md`

## [2026-10-26] skill | OpenCode Skills — Arquitecto y Revisor de Planes

Instalados globalmente en `C:\Users\user\.config\opencode\skills\`: `grill-me` + `grilling` (mattpocock/skills, ~300k stars) y `architect` + `reviewer` + `decision-log` (garethrhughes/skills, compatibilidad opencode), con `RULES.md` y overlays `rules/`. Flujo: @grill-me → @architect → usuario acepta propuesta → decision-log (ADR) → implementar → @reviewer (PASS / PASS WITH COMMENTS / BLOCK). Convención de aviso automático añadida a `C:\Users\user\.config\opencode\AGENTS.md`. Nota: `skills/opencode-skills-arquitecto.md`

## [2026-11-02] atiende | Fase 4 cerrada + Fase 4B-lite (Baileys) implementada y apagada

Fases 1-4 completas. Canal de pruebas Baileys dentro del worker (ADR-0010), sesión cifrada, QR en Canales y borrado desde el panel; revisión `@reviewer` PASS WITH COMMENTS. `WHATSAPP_BAILEYS_ENABLED="false"` hasta conseguir un chip o eSIM con SMS/voz. 111 pruebas; typecheck, lint y build limpios. Código de la app sin commits. Nota: `clients/dr-tomas-tijerina/projects/atiende/daily/2026-11-02.md`.
