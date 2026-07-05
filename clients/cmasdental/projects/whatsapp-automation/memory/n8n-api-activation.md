---
tags: [skill, memory]
date: 2026-07-05
entityType: skill
---

# n8n API activation

- To activate: POST /api/v1/workflows/{id}/activate
- To deactivate: POST /api/v1/workflows/{id}/deactivate
- PUT with full workflow body does NOT allow changing 'active' field (read-only)
- Must use dedicated activate/deactivate endpoints

## Enlaces
- [[_index|Todas las memorias]]
