---
tags: [skill, automation]
category: automation
---

# n8n Workflow Automation

## Descripción

Automatización de flujos usando n8n-as-code. Los workflows se definen como `.workflow.ts` y se sincronizan con una instancia de n8n.

## Cuándo usarlo

- Para integrar servicios (Slack, Gmail, Supabase, etc.)
- Para disparar acciones cuando cambia la vault de Obsidian
- Para crear dashboards y notificaciones

## Cómo se implementa

```bash
# Estado del workspace
npx --yes n8nac workspace status --json

# Push de workflow
npx --yes n8nac push workflow.workflow.ts --verify

# Test
npx --yes n8nac test <workflowId> --prod
```

## Relacionado con

- [[projects/second-brain-plan|Proyecto Segundo Cerebro]]

## Enlaces

- [[skills/_index|Todas las skills]]
