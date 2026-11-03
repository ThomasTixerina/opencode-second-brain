---
tags: [configuracion, memory]
date: 2026-11-02
entityType: configuracion
---

# OpenCode Skills Instalados

- 2026-10-26: Skills de arquitecto/plan-review instalados globalmente en C:\Users\user\.config\opencode\skills\
- grill-me + grilling (de mattpocock/skills, ~300k stars MIT): entrevista implacable para presionar/stress-testear planes; grill-me es stub de invocacion manual via /grill-me, grilling es el motor de la entrevista en rondas por design tree
- architect + reviewer + decision-log (de garethrhughes/skills, compatibilidad opencode): architect escribe propuestas en docs/proposals/, reviewer emite veredicto PASS/PASS WITH COMMENTS/BLOCK con trazabilidad a Acceptance Criteria, decision-log crea ADRs en docs/decisions/
- Dependencias copiadas junto a los skills: RULES.md y rules/ (overlays typescript.md y dotnet.md); reviewer usa por defecto overlay typescript si CLAUDE.md no declara Active Skillset
- El usuario los pidio para que un arquitecto revise los planes que OpenCode genera antes de implementar
- Nota completa en el vault: C:\Users\user\second-brain\skills\opencode-skills-arquitecto.md (tabla de skills + flujo de 6 pasos), con entrada en log.md tipo skill
- Instrucción permanente añadida a C:\Users\user\.config\opencode\AGENTS.md: cuando un agente detecte/cargue auto o manualmente uno de estos skills, debe avisar al usuario en una línea qué skill se activó, qué hace y en qué punto del flujo está (@grill-me → @architect → aceptar propuesta → decision-log → implementar → @reviewer)
- Petición del usuario (2026-10-26): quiere ser avisado automáticamente cuando un skill se auto-active, con explicación de qué hace cada uno y el flujo completo
- 2026-10-27 PROYECTO ATIENDE (CRM-Whatsapp): flujo completo ejecutado por primera vez end-to-end — grilling cerró el árbol (12 huecos + ronda de verificación con 6 preguntas: backups sí, alertas sí, admin agencia sí, commits sí, número personal WABA para pruebas, arrancar Fase 1)
- Propuesta docs/proposals/0001-atiende-asistente-whatsapp.md ACEPTADA; ADRs 0001-0008 en docs/decisions/ (0007 backup diario + alerta salud, 0008 admin agencia via seed — de mi auditoría grilling); commit 10ef118 en repo CRM-Whatsapp
- El Aviso de flujo (AGENTS.md) FUNCIONÓ: el agente de la sesión plan abrió su revisión con 'Aviso de flujo: se activó architect...' y el usuario fue avisado del punto del flujo en cada paso
- Fase 1 (andamiaje: package.json, next.config.ts, config Zod, auth, Prisma) corriendo en la sesión plan ses_e8573a4b1ffdZNOzSlDz1YbKCU; la sesión build NO toca código para evitar conflictos de dos agentes en un repo
- Pendiente: paso 6 del flujo — @reviewer cuando haya código; credenciales externas bloquean Fase 4 (OPENROUTER_API_KEY, OAuth Google, WABA+número YCloud, chip desechable Baileys)

## Enlaces
- [[memory/_index|Todas las memorias]]
