# 🧠 Second Brain — AI Agent Guidelines

This vault is a portable second brain for AI-assisted knowledge management.
It works with OpenCode, Gemini CLI, Obsidian, and n8n.

## Vault structure

```
second-brain/
├── AGENTS.md          ← You are here (AI entry point)
├── _index.md          ← Map of Content (MOC)
├── projects/          ← Active projects
├── skills/            ← Reusable skills & patterns
├── memory/            ← Persistent memory (synced from OpenCode)
├── daily/             ← Daily notes
├── references/        → Reference material
├── templates/         ← Templater templates (5)
├── attachments/       ← Images & files
├── excalidraw/        ← Diagrams & drawings
├── kanban/            ← Kanban boards
├── guides/            ← Setup & usage guides
└── scripts/           ← Bridge & sync tools
```

## AI agent protocol

### MUST do at session start
1. Read this `AGENTS.md`
2. Check `projects/` for context on current workspace
3. Check `memory/` for past decisions
4. Read today's note in `daily/` (if it exists)

### MUST do during session
- Store decisions in `memory/` using the memory template (`templates/memory.md`)
- Document reusable patterns in `skills/`
- Update daily note with progress

### MUST do at session end
1. Run memory sync: `python scripts/sync-memory.py to-vault`
2. Write a session summary to `daily/YYYY-MM-DD.md`
3. Commit and push if changes were made

## Bridge tools

```bash
python scripts/bridge.py list           # List vault structure
python scripts/bridge.py read <path>    # Read a note
python scripts/bridge.py search <q>     # Search vault content
python scripts/bridge.py daily          # Open/create today's note

python scripts/sync-memory.py to-vault          # JSONL → vault .md
python scripts/sync-memory.py from-vault        # vault .md → JSONL
python scripts/sync-memory.py import-sessions   # Session backups → daily/
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
