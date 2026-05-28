---
tags: [project, memory, project]
date: 2026-05-27
entityType: project
---

# project-miconsuluno

- Sistema de gestión de clínicas médicas (PHP 8.2 + MySQL 8.0 en Docker)
- Basado en OSPOS fork con extensiones médicas (~44 tablas)
- Stack: miconsul-app (puerto 8000), miconsul-db (MySQL), n8n, PostgreSQL, Redis
- n8n como capa de automatización: webhooks para registro pacientes, correos, reportes
- Red Docker: miconsul_network
- n8n lee/escribe directamente la misma BD MySQL que la app PHP

## Enlaces
- [[memory/_index|Todas las memorias]]
