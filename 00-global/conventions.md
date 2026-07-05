---
tags: [global, conventions]
updated: 2026-07-04
---

# Conventions — Estándares Técnicos Transversales

## TypeScript
- Comillas simples (`'string'`), trailing commas, sin punto y coma
- Named exports. `const` > `let`. Interfaces > types para shapes
- Strict mode

## PHP (MiConsulUno)
- PSR-12 coding standard, PSR-4 autoloading
- PHPStan nivel 0
- Jenkins CI (sin GitHub Actions)
- Dev deps: `squizlabs/php_codesniffer`

## Python
- PEP 8, snake_case, pathlib para rutas
- Type hints en todas las funciones
- Singletons globales para DB/session
- Named exports, sin wildcard imports

## Git
- Conventional commits: `type(scope): description`
- Tipos: feat, fix, docs, style, refactor, test, chore
- No commitar: `.env`, `node_modules/`, `dist/`, config IDE

## n8n
- Usar `n8nac` para validación antes de push
- Consultar schema con `n8nac skills node-info <nodeName>`
- Decoradores: `@workflow`, `@node`, `@links` de `@n8n-as-code/transformer`
- Sub-nodos AI: `this.Agent.uses({ ai_languageModel: this.Model.output })` — nunca `.out().to()`
- Preferir `{{ $json.field }}` sobre legacy `$node["Name"].json.field`
- Target: `tomas-tixerina.app.n8n.cloud`

## NotebookLM
- Active notebook: Python Fullstack Knowledge (ID: `python-fullstack-knowledge`)
- Consultar antes de implementar patrones Python/Flet/DB

## Memoria Dual (OpenCode)
- `memory` — por proyecto (`%USERPROFILE%\.opencode-memory\<ruta-sanitizada>.jsonl`)
- `memory-global` — entre proyectos (`%USERPROFILE%\.opencode-memory\global.jsonl`)

## Obsidian Vault
- Frontmatter YAML obligatorio (tags, date, updated)
- Tags: client, project, skill, memory, reference, daily
- Usar Dataview para queries sobre el vault
- Templates con Templater syntax (`Ctrl+T`)
