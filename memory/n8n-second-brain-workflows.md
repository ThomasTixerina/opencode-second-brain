---
tags: [project, memory, project]
date: 2026-05-27
entityType: project
---

# n8n-second-brain-workflows

- Two n8n cloud workflows created for second-brain vault integration: Vault Gateway and Daily Digest
- Vault Gateway (ID: tpkJQyuUcHqlXkdA): Webhook POST /vault-gateway → GitHub create/edit file in ThomasTixerina/second-brain
- Daily Digest (ID: FNBEmCoMXY4FY5bD): Cron daily 8am → Code (generate date path) → GitHub read daily note
- Both workflows need a GitHub OAuth2 credential configured in the n8n UI

## Enlaces
- [[memory/_index|Todas las memorias]]
