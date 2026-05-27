---
tags: [workflow, memory]
date: 2026-05-27
entityType: workflow
---

# vault-gateway

- Vault Gateway workflow (v20) successfully deployed to n8n cloud, creates files in ThomasTixerina/second-brain via GitHub API.
- Workflow structure: Webhook (POST /vault-gateway) → Code (Base64 Encode Content) → HTTP Request (PUT GitHub API)
- Credentials: OAuth2 'GitHub account' (ID: gASlu5EsJ3zXmgNu)
- API URL: https://tomas-tixerina.app.n8n.cloud/api/v1, auth: X-N8N-API-KEY header
- n8n instance: tomas-tixerina.app.n8n.cloud

## Enlaces
- [[memory/_index|Todas las memorias]]
