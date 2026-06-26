# n8n-dev + WhatsApp AI Assistant — Sesión 31 Mayo 2026

## Stack n8n-dev (Local)

- **Ubicación**: `C:\Users\Thomas Tixerina\n8n-dev\`
- **Docker Compose**: n8n + n8n-worker + Postgres 16 + Redis 7
- **URL**: http://localhost:5678
- **Versión**: 2.22.5 (docker.n8n.io/n8nio/n8n:latest)
- **Owner**: ttijerina@gmail.com / n8nadmin
- **MCP**: POST /mcp-server/http con JWT Bearer (config en opencode.json)
- **Contenedores**: Todos corriendo sin issues

## Progreso

### Completado
- Stack n8n-dev desplegado y operativo
- MCP endpoint funcional (Streamable HTTP)
- Validado workflow SDK simple vía MCP `validate_workflow`
- Creado workflow "Asistente Dental AI" (Chat Trigger → AI Agent con GPT-4o-mini + Simple Memory) — ID: `2fjOicXO2pIfxswX`
- Analizado archivo `WhatsApp AI Assistant - Cmasdental (Fixed).json` (~53KB, 27 nodos)
- Login a n8n REST API exitoso (cookie n8n-auth)
- Creada credencial de prueba `httpHeaderAuth` (YCloud API Test) — ID: `KzBsLn3nIj8BNOnv`
- `cloudflared` ya instalado

### Pendiente (para próxima sesión)

#### Fase 1 — Crear credenciales (necesito API keys del usuario)
- [ ] **YCloud Webhook Header Auth** (`httpHeaderAuth`) — header name + value
- [ ] **YCloud API** (`httpHeaderAuth`) — API key
- [ ] **OpenAI** (`openAiApi`) — API key
- [ ] **Gmail OAuth2** (`gmailOAuth2`) — para ttijerina@gmail.com
- [ ] **Google Calendar OAuth2** (`googleCalendarOAuth2`) — para cmasdental@gmail.com

#### Fase 2 — Cloudflare Tunnel
- [ ] Ejecutar `cloudflared tunnel login` (autenticación browser)
- [ ] Crear tunnel: n8n.drtomastijerina.com → localhost:5678
- [ ] Actualizar N8N_HOST y WEBHOOK_URL en .env

#### Fase 3 — Modificar JSON
- [ ] Reemplazar `https://tomas-tixerina.app.n8n.cloud` → `https://n8n.drtomastijerina.com` (6 ocurrencias)
- [ ] Eliminar `errorWorkflow: "FVfIeC3QELt01pJx"` de settings
- [ ] Reemplazar credential IDs con los locales

#### Fase 4 — Workflow cmas-calendar
- [ ] Crear workflow: Webhook POST → Google Calendar (Create Event en cmasdental@gmail.com)
- [ ] Endpoint: POST /webhook/cmas-calendar

#### Fase 5 — Importar y activar
- [ ] Importar WhatsApp Assistant vía REST API o MCP
- [ ] Configurar YCloud webhook → URL del tunnel
- [ ] Testing con números de prueba (528112808077, 528113090909)

## Detalles Técnicos del Flujo

### Arquitectura (27 nodos)
```
Webhook (YCloud) → Filter & Extract
  ├── Filter Text → Check Cooldown
  ├── Filter Audio → Download Audio → Transcribe (Whisper) → Format Audio → Check Cooldown
  └── Filter Image → Download Image → Describe (Vision) → Format Image → Check Cooldown

Check Cooldown → Filter Cooldown → Send Cooldown Message
               → Filter Not Cooldown → AI Agent (GPT-4o-mini + Memory)
                                          → Parse Output
                                              ├── Filter Chat → Send via YCloud → Mark Cooldown
                                              ├── Filter Escalate → Prepare Escalation
                                              │                       ├── Send Escalation (WhatsApp) → Mark Cooldown
                                              │                       └── Email Escalation (Gmail)
                                              └── Filter Schedule → Branch Lookup → Prepare Pending
                                                                     → Send to Branch WhatsApp (template)
                                                                     → Wait 15min (webhook resume)
                                                                     → Check Decision
                                                                         ├── Confirmed → Schedule Appointment (webhook)
                                                                         │              → Format Confirmation
                                                                         │              → Send Schedule Confirm (WhatsApp)
                                                                         ├── Rejected → Send Rejection (WhatsApp)
                                                                         └── Timeout → Send Timeout Notification
                                                                                    → Send Timeout Patient Notification

Send to Branch WhatsApp (error) → Handle Branch Error
                                   ├── Send Branch Error Alert (WhatsApp)
                                   └── Send Branch Error Patient (WhatsApp)
```

### Credenciales Necesarias
| Tipo | Uso | ID en cloud |
|------|-----|-------------|
| `httpHeaderAuth` | YCloud Webhook Header Auth | `epMcls2auF34IekT` |
| `httpHeaderAuth` | YCloud API | `yTz9CXQoW45EmRDm` |
| `openAiApi` | OpenAI account 3 | `w0MFn0zydLysuX2W` |
| `gmailOAuth2` | Gmail account | `hKfPKOLaGML346s3` |
| `googleCalendarOAuth2` | cmasdental@gmail.com | (nueva) |

### URLs a Reemplazar (6 ocurrencias)
- Prepare Pending: `baseUrl`, `resumeUrl`, `portalUrl`
- Schedule Appointment: URL del webhook `/webhook/cmas-calendar`

## Archivos Relacionados
- `C:\Users\Thomas Tixerina\OneDrive\Desktop\n8n-Odoo-Environment\WhatsApp AI Assistant - Cmasdental (Fixed).json` — Flujo fuente
- `C:\Users\Thomas Tixerina\n8n-dev\docker-compose.yml` — Stack Docker
- `C:\Users\Thomas Tixerina\n8n-dev\.env` — Variables de entorno n8n
- `C:\Users\Thomas Tixerina\segundo cerebro\proyectos\n8n-dev-whatsapp-assistant.md` — Esta nota
