---
tags: [project, memory, project]
date: 2026-05-27
entityType: project
---

# miconsuluno_mcp

- MCP Server en Python para MiConsulUno (gestión clínica PHP legacy + MySQL)
- Expone ~30 herramientas CRUD y métricas como herramientas MCP
- Location: C:\Users\user\n8n-miconsul\miconsuluno_mcp
- Paquete Python instalable (pyproject.toml, src layout)
- 28 tools registradas + 3 resources
- Dependencias: mcp>=1.0.0, pymysql>=1.0.0, python-dotenv>=1.0.0
- Fase 1 de 4 del plan de modernización de MiConsulUno
- MCP Server Python exponiendo CRUD de MiConsulUno (PHP+MySQL) como tools
- Src layout: pyproject.toml + src/miconsuluno_mcp/
- 28 tools: pacientes, citas, servicios, materiales, doctores, sucursales, ventas, metrics
- 3 resources: daily KPIs, sucursales, especialidades
- pip install -e . para desarrollo; entry point: miconsuluno-mcp
- Fase 1 del plan de modernización

## Enlaces
- [[memory/_index|Todas las memorias]]
