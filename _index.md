# Segundo Cerebro — Map of Content

> "No se trata de recordar más rutas, sino de entender mejor el camino."

## 🧠 Núcleo

- [[memory/_index|Memoria Persistente]] — contexto de sesiones, decisiones, aprendizajes
- [[skills/_index|Skills & Patrones]] — conocimiento reutilizable para IA y humanos
- [[projects/_index|Proyectos Activos]] — cada proyecto con su espacio

## 📡 Canales

| Canal | Propósito | Bridge |
|-------|-----------|--------|
| OpenCode CLI | Asistente de codigo interconectado | `memory/` tools + scripts |
| Gemini CLI | Asistente generativo | API + scripts Python |
| n8n | Automatización de flujos | Workflow triggers |
| Supabase | Backend de datos estructurados | SQL queries |

## ⚡ Rutinas

- [[daily/<% tp.date.now("YYYY-MM-DD") %>|Nota Diaria]] — hoy
- [[templates/project|Nuevo Proyecto]] — template para proyectos
- [[templates/skill|Nueva Skill]] — template para skills
- [[templates/reference|Nueva Referencia]] — template para referencias

## 📁 Archivos

```
second-brain/
├── _index.md              ← estás aquí
├── projects/              ← proyectos activos
├── skills/                ← skills y patrones
├── memory/                ← memoria persistente
├── daily/                 ← notas diarias
├── references/            ← material de referencia
├── templates/             ← templates reutilizables
├── attachments/           ← imágenes, archivos adjuntos
├── excalidraw/            ← dibujos y diagramas
├── kanban/                ← tableros kanban
└── .obsidian/             ← configuración del vault
```

## 📊 Resumen del Vault

```dataview
TABLE length(rows) AS "Notas"
FROM "" AND -"templates" AND -".obsidian"
GROUP BY file.folder
SORT file.folder ASC
```

## 📌 Proyectos Activos

```dataview
TABLE started AS "Inicio", status AS "Estado"
FROM #project
WHERE status = "active"
SORT started DESC
```

## 🧠 Memorias Recientes

```dataview
LIST
FROM #memory
SORT file.ctime DESC
LIMIT 10
```

## 📅 Daily Notes Recientes

```dataview
LIST
FROM "daily"
SORT file.day DESC
LIMIT 14
```

## 🔗 Tags principales

- `#project` — proyectos activos
- `#skill` — skills técnicas
- `#memory` — fragmentos de memoria
- `#reference` — referencia externa
- `#ai` — relacionado con inteligencia artificial
- `#automation` — automatizaciones y workflows
