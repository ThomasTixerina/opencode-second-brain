---
tags: [concept]
category: pattern
related:
created: 2026-07-08
updated: 2026-07-08
---

# Structured JSON ingestion interface

## Definición

- Uso de JSON como interfaz estructurada entre el LLM (que genera conocimiento) y el script de archivo (que escribe markdown), desacoplando razonamiento de I/O.

## Contexto

- ingest.py draft genera template JSON -> LLM lo llena -> ingest.py commit lo lee de stdin y escribe archivos markdown. Cualquier agente AI puede participar.

## Implementación

- El JSON incluye title, source_url, date, summary, key_points, entities[], concepts[]. El script parsea y escribe sources/<slug>.md, entities/<entity>.md, concepts/<concept>.md.

## Fuentes

- [[wiki/sources/super-second-brain-architecture]]

## Enlaces

- [[wiki/_index|Wiki principal]]
