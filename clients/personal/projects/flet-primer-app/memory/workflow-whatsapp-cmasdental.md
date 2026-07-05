---
tags: [workflow, memory]
date: 2026-07-05
entityType: Workflow
---

# Workflow WhatsApp Cmasdental

- Workflow ID: FGqn32nnIgMkHC0v
- Usa YCloud API para WhatsApp
- AI Agent con GPT-4o-mini
- Calendar Service funciona correctamente (crea eventos en Google Calendar)
- Confirmation Portal funciona (HTML se renderiza)
- Chat route verificada funcionando
- Schedule route no probada aún
- Branch Lookup solo tiene 1 sucursal hardcodeada (Centro) - necesita 25
- System message tiene fecha hardcodeada
- No tiene knowledge base externa
- Larry v2: system message acortado y más directo
- Reglas: primer mensaje siempre con nombre Larry, un dato a la vez, JSON solo cuando paciente confirma
- ParseOutput usa regex para extraer JSON del texto del AI
- FilterExtract inyecta [HOY ES ...] al inicio del mensaje para contexto de fecha
- Larry v3: emojis, escalamiento de quejas, consent info
- 23 nodos total (3 nuevos: FilterEscalate, SendEscalation, SendEscalationResponse)
- Escalamiento envía alerta al paciente y respuesta de confirmación
- Pending: admin number still goes to patient phone - needs correction
- 33 nodos total - Sistema completo
- CheckCooldown: cooldown 30 min por número, guarda en staticData
- MarkCooldown: marca timestamp en staticData cuando se escala
- FilterTimeout + SendTimeoutNotification: timeout 5 min en espera de confirmación
- Timeout notifica al admin 528113090909 si sucursal no responde

## Enlaces
- [[_index|Todas las memorias]]
