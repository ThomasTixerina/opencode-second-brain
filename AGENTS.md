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
├── raw/                               ← Fuentes inmutables (artículos, clippings)
├── wiki/                              ← Conocimiento compilado (LLM-generated)
│   ├── _index.md                      ← Catálogo completo del wiki
│   ├── entities/                      ← Personas, empresas, herramientas
│   ├── concepts/                      ← Patrones, arquitecturas, ideas
│   ├── synthesis/                     ← Análisis, comparativas, respuestas archivadas
│   └── sources/                       ← Resúmenes de fuentes ingeridas
├── memory/                            ← Memoria global (sincronizada de OpenCode)
├── daily/                             ← Daily notes globales
├── skills/                            ← Patrones reutilizables
├── references/                        ← Material de referencia
├── templates/                         ← Templater templates (9)
├── log.md                             ← Registro cronológico append-only
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
3. Leer `wiki/_index.md` y `log.md` (últimas 5 entradas)
4. **Preguntar: "¿Qué cliente?"** (cmasdental / dr-tomas-tijerina)
5. **Preguntar: "¿Qué proyecto?"** (según el cliente)
6. Leer `clients/<client>/client-context.md`
7. Leer `clients/<client>/projects/<project>/project-context.md`
8. Revisar `clients/<client>/projects/<project>/memory/` para decisiones pasadas
9. Revisar `clients/<client>/projects/<project>/daily/` para la nota de hoy

### MUST do during session

- Almacenar decisiones en `clients/<client>/projects/<project>/memory/`
- Documentar patrones reutilizables en `skills/`
- Actualizar daily note del proyecto con progreso
- Si se genera conocimiento transversal, archivarlo en `wiki/`

### MUST do at session end

1. Sync de memoria: `python scripts/sync-memory.py to-vault --client <c> --project <p>`
2. Escribir resumen en `clients/<client>/projects/<project>/daily/YYYY-MM-DD.md`
3. Si el cambio aplica globalmente, también escribir en `00-global/`
4. Commit y push si hubo cambios

## Wiki Protocol

El wiki es una capa de conocimiento compilado mantenida por IA.
A diferencia de `memory/` (que guarda decisiones de sesiones), `wiki/` guarda síntesis de fuentes, entidades, conceptos y análisis.
Las fuentes son inmutables y viven en `raw/` — el LLM nunca las modifica.

### Ingest

Cuando se agregue una fuente a `raw/` o el usuario pida procesar una fuente:

1. Leer la fuente completa de `raw/` (no modificar el original)
2. Si `--discuss`: discutir hallazgos clave con el usuario antes de escribir
3. Escribir `wiki/sources/<slug>.md` con resumen estructurado (usar template `source-summary`)
4. Identificar entidades en la fuente:
   - Si ya existen en `wiki/entities/`, actualizar sus páginas con nueva información
   - Si no existen, crear nueva página usando template `entity`
5. Identificar conceptos en la fuente:
   - Si ya existen en `wiki/concepts/`, actualizar
   - Si no existen, crear usando template `concept`
6. Si la nueva fuente contradice conocimiento existente, marcarlo con `> [!contradiction]` y `> [!superseded]` en las páginas relevantes
7. Actualizar `wiki/_index.md` (catálogo)
8. Append a `log.md`: `## [YYYY-MM-DD] ingest | Título de la fuente`

### Compound Answers

Cuando respondas una pregunta que genere conocimiento nuevo y valioso:

1. Escribir la respuesta como `wiki/synthesis/<topic>.md` (usar template `synthesis`)
2. Enlazarla desde las entidades y conceptos relevantes
3. Agregar entrada a `log.md`: `## [YYYY-MM-DD] query-archive | Tema`
4. Actualizar `wiki/_index.md`

Las respuestas archivadas no desaparecen en el historial del chat — se capitalizan en el wiki.

### Lint

Si el usuario pide "revisa el wiki" o ha pasado >24h desde el último lint:

1. Ejecutar `python scripts/lint-wiki.py` (o los checks manualmente si el script no existe aún)
2. Revisar y aplicar correcciones:
   - Contradicciones entre páginas
   - Páginas huérfanas sin inbound links
   - Claims que fuentes recientes han superado
   - Conceptos mencionados pero sin página propia
3. Escribir reporte en `wiki/lint-report-YYYY-MM-DD.md`
4. Append a `log.md`: `## [YYYY-MM-DD] lint | Hallazgos`

### Log format

Cada entrada en `log.md` sigue este formato:

```
## [YYYY-MM-DD] <tipo> | <título>

<detalle opcional>
```

Tipos de entrada: `ingest`, `query-archive`, `lint`, `synthesis`, `schema-update`.

El log es parseable con `grep "^## \[" log.md | tail -5` para ver las últimas 5 entradas.

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
- `#automation` — automation
- `#entity` — wiki entity page
- `#concept` — wiki concept page
- `#synthesis` — wiki analysis / synthesis
- `#source` — ingested source summary
- `#log` — log entry

## Templates (Templater, `Ctrl+T`)

| Template | Usage |
|----------|-------|
| `templates/daily.md` | Daily note |
| `templates/memory.md` | Decision log |
| `templates/project.md` | New project |
| `templates/reference.md` | External reference |
| `templates/skill.md` | Reusable skill |
| `templates/entity.md` | Wiki entity (person, company, tool) |
| `templates/concept.md` | Wiki concept (pattern, architecture) |
| `templates/synthesis.md` | Wiki analysis / archived answer |
| `templates/source-summary.md` | Ingested source summary |

## Automation

### Python scripts

```bash
python scripts/ingest.py raw/<file>          # Ingest a source
python scripts/ingest.py raw/<file> --discuss # Ingest with human discussion
python scripts/ingest.py --all               # Process all pending sources in raw/

python scripts/lint-wiki.py                  # Health check the wiki
python scripts/lint-wiki.py --fix            # Auto-fix some issues

python scripts/wiki-watch.py                 # Background watcher (polling)
python scripts/compact_memory.py --vault .    # Hierarchical memory compaction
```

### Watcher

`wiki-watch.py` corre en background con polling cada 60s y:
- Detecta archivos nuevos en `raw/` (no ejecuta ingesta automática — solo notifica)
- Ejecuta lint si ha pasado >24h desde el último
- No consume tokens en idle — solo llama al LLM cuando hay trabajo real

### Task Scheduler (Windows)

```powershell
# Registrar tareas programadas
powershell scripts\setup-automation.ps1

# Tareas registradas:
#   - lint-wiki.py cada 24h
#   - compact_memory.py cada 7 días
#   - wiki-watch.py al iniciar sesión
```
