# Second Brain — AI Agent Guidelines

This vault is a portable second brain for AI-assisted knowledge management.
Works with OpenCode, Gemini CLI, Obsidian, and n8n.

## Vault structure

```
second-brain/
├── AGENTS.md                          ← You are here (AI entry point)
├── 00-global/                         ← Conocimiento transversal
│   ├── master-index.md                ← Mapa de todos los proyectos
│   └── conventions.md                 ← Convenciones técnicas globales
├── clients/                           ← Clientes (organizaciones/personas)
│   ├── cmasdental/                    ← Cliente: Cmasdental
│   │   ├── client-context.md          ← Contexto del negocio
│   │   ├── memory/                    ← Decisiones y contexto persistente
│   │   ├── daily/                     ← Daily notes del cliente
│   │   └── projects/
│   │       └── whatsapp-automation/   ← Proyecto activo
│   │           ├── project-context.md
│   │           ├── memory/
│   │           └── daily/
│   └── dr-tomas-tijerina/             ← Cliente: Dr. Tomás Tijerina (proyectos propios)
│       ├── client-context.md
│       ├── memory/
│       ├── daily/
│       └── projects/
│           ├── miconsuluno/
│           │   ├── project-context.md
│           │   ├── memory/
│           │   └── daily/
│           ├── nestjs-supabase-auth/
│           │   ├── project-context.md
│           │   ├── memory/
│           │   └── daily/
│           └── voice-cli/
│               ├── project-context.md
│               ├── memory/
│               └── daily/
├── memory/                            ← Memoria global (sincronizada de OpenCode, legado temporal)
├── daily/                             ← Daily notes globales (legado temporal)
├── skills/                            ← Patrones reutilizables
├── references/                        ← Material de referencia
├── templates/                         ← Templater templates (5)
├── attachments/                       ← Images & files
├── excalidraw/                        ← Diagrams & drawings
├── kanban/                            ← Kanban boards
├── guides/                            ← Setup & usage guides
└── scripts/                           ← Bridge & sync tools
```

## AI Agent Protocol

### MUST do at session start

1. Leer este `AGENTS.md`
2. Leer `00-global/master-index.md`
3. **Preguntar: "¿Qué cliente?"** (cmasdental / dr-tomas-tijerina)
4. **Preguntar: "¿Qué proyecto?"** (según el cliente)
5. Leer `clients/<client>/client-context.md`
6. Leer `clients/<client>/projects/<project>/project-context.md`
7. Revisar `clients/<client>/projects/<project>/memory/` para decisiones pasadas
8. Revisar `clients/<client>/projects/<project>/daily/` para la nota de hoy

### MUST do during session

- Almacenar decisiones en `clients/<client>/projects/<project>/memory/`
- Documentar patrones reutilizables en `skills/`
- Actualizar daily note del proyecto con progreso

### MUST do at session end

1. Sync de memoria: `python scripts/sync-memory.py to-vault --client <c> --project <p>`
2. Escribir resumen en `clients/<client>/projects/<project>/daily/YYYY-MM-DD.md`
3. Si el cambio aplica globalmente, también escribir en `00-global/`
4. Commit y push si hubo cambios

## Bridge tools

```bash
python scripts/bridge.py list                              # List vault structure
python scripts/bridge.py read <path>                       # Read a note
python scripts/bridge.py search <q>                        # Search vault content
python scripts/bridge.py daily                             # Open/create today's note (global)

python scripts/sync-memory.py to-vault                     # JSONL → vault memory/ (global)
python scripts/sync-memory.py to-vault --client <c>        # → clients/<c>/memory/
python scripts/sync-memory.py to-vault --client <c> --project <p>  # → clients/<c>/projects/<p>/memory/
python scripts/sync-memory.py from-vault                   # vault memory/ → stdout as JSONL
python scripts/sync-memory.py import-sessions              # Session backups → vault daily/ (global)
python scripts/sync-memory.py import-sessions --client <c> --project <p>  # → clients/<c>/projects/<p>/daily/
```

## Tags

- `#project` — active project
- `#skill` — technical skill / pattern
- `#memory` — persistent memory fragment
- `#reference` — external reference
- `#daily` — daily note
- `#ai` — AI-related
- `#automation` — automation / n8n

## Templates (Templater, `Ctrl+T`)

| Template | Usage |
|----------|-------|
| `templates/daily.md` | Daily note |
| `templates/memory.md` | Decision log |
| `templates/project.md` | New project |
| `templates/reference.md` | External reference |
| `templates/skill.md` | Reusable skill |

## Automation (optional)

Two n8n workflows are available in `automation/`:
- `vault-gateway.workflow.json` — Webhook to create/update vault files via GitHub API
- `daily-digest.workflow.json` — Scheduled daily note reader

Import them into any n8n instance (Settings → Import → From File).
