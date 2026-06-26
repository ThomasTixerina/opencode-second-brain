# Segundo Cerebro

> Mapa del vault — agencia de automatización.

## Estructura

| Carpeta | Propósito |
|---------|-----------|
| `clientes/` | Información de clientes, contactos, contexto |
| `proyectos/` | Workflows, automatizaciones, estado |
| `infraestructura/` | Servidores MCP, APIs, credenciales (referencias) |
| `decisiones/` | ADRs (Architecture Decision Records) |
| `templates/` | Plantillas para clientes, proyectos, notas |
| `skills/` | Skills de OpenCode, guías de stack |
| `notas-rapidas/` | Capturas rápidas, ideas sueltas |

## Stack

- **Frontend**: Flet
- **Backend**: FastAPI (async)
- **DB**: Supabase (Postgres)
- **CRM**: Odoo 18 (local) / Odoo 19 (online)
- **Automatización**: n8n (dev local / cloud prod)
- **AI**: OpenCode con MCP servers
