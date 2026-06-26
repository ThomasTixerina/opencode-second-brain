# Configuración OpenCode — MCP Servers

> Archivo funcional (fuente de verdad): `~/.config/opencode/.env`
> No duplicar valores sensibles aquí. Este documento es solo referencia.

---

## API Keys activas

| Variable | Propósito | Fuente / Notas |
|----------|-----------|----------------|
| `CONTEXT7_API_KEY` | Documentación técnica de librerías | context7.dev |
| `BRAVE_API_KEY` | Búsqueda web | brave.com/search |
| `FIRECRAWL_API_KEY` | Web scraping + research | firecrawl.dev |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | API de GitHub | github.com/settings/tokens (fine-grained, repo + issues) |
| `STITCH_API_KEY` | Diseño UI con IA | stitch.google.com |

## Odoo — Credenciales por tenant

| Tenant | URL | DB | User | Archivo fuente |
|--------|-----|----|------|----------------|
| CmasDental (local) | `http://localhost:8069` | `odoo_cmasdental` | `admin` | `~/.config/opencode/opencode.json` |
| CorpoDental (local) | `http://localhost:8069` | `odoo_corpodental` | `ttijerina@gmail.com` | `~/.config/opencode/opencode.json` |
| Online (SaaS) | `https://drtomastijerina.com` | `drtomastijerina` | `ttijerina@gmail.com` | `~/.config/opencode/opencode.json` |

**Odoo online requiere API key** (Enterprise). Pendiente configurar.

## Servidores con auth por OAuth

| Server | Acción para conectar |
|--------|---------------------|
| `supabase` | `opencode mcp auth supabase` (abre navegador) |
| `supabase-vault` | `opencode mcp auth supabase` (mismo login) |

## n8n

| Modo | Tipo | Dónde está configurado |
|------|------|------------------------|
| Local (`n8n-dev`) | MCP HTTP en `localhost:5678/mcp-server/http` | `~/.config/opencode/opencode.json` |
| Cloud (`n8n-cloud`) | vía `n8n-mcp` package con API key | `~/Odoo/opencode.json` |

## Notas

- El servidor `memory` global está deshabilitado (`enabled: false` en `opencode.json`)
- Los API keys están únicamente en `~/.config/opencode/.env` (nunca duplicar en el vault)
- Chrome DevTools MCP requiere Chrome abierto con `--remote-debugging-port=9222`
