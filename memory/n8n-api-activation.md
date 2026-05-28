---
tags: [skill, memory]
date: 2026-05-27
entityType: skill
---

# n8n API activation

- To activate: POST /api/v1/workflows/{id}/activate
- To deactivate: POST /api/v1/workflows/{id}/deactivate
- PUT with full workflow body does NOT allow changing 'active' field (read-only)
- Must use dedicated activate/deactivate endpoints

## Enlaces
- [[memory/_index|Todas las memorias]]
