# ADR: Arquitectura de Agencia de Automatización

**Fecha:** 2026-05-31

## Contexto
Creación de agencia de automatización usando n8n + Odoo + Supabase.

## Decisión
- n8n local para desarrollo de workflows
- n8n cloud para producción
- Workflows se exportan como JSON desde dev y se importan a cloud tras revisión
- MCP de n8n solo conectado a instancia local (nunca a producción)
- Obsidian como segundo cerebro (reemplaza memory MCP)

## Stack
- UI: Flet
- API: FastAPI async
- DB: Supabase (Postgres + Auth + Storage)
- CRM: Odoo 18 local / Odoo 19 online
- Automatización: n8n

## Estado
✅ Aprobado
