---
tags: [knowledge-base, memory]
date: 2026-05-27
entityType: knowledge-base
---

# n8n-workflow-patterns

- Vault Gateway workflow: Webhook → Code (base64 encode) → HTTP Request (PUT GitHub API). For new files, works without sha. For updating existing files, requires sha parameter.
- HTTP Request node with keypair body mode and content_type:json works correctly when using a Code node for base64 encoding. Buffer is NOT available in n8n expressions but IS available in Code node JavaScript.
- n8n Code node parameter for JavaScript code is `jsCode`, not `code`. Using `code` results in empty jsCode and assertion error.

## Enlaces
- [[memory/_index|Todas las memorias]]
