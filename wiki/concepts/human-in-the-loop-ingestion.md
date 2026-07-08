---
tags: [concept]
category: pattern
related:
created: 2026-07-08
updated: 2026-07-08
---

# Human-in-the-loop ingestion

## Definición

- Pipeline de ingesta que requiere decisi?n humana antes de escribir, previniendo contaminaci?n del conocimiento por automatizaci?n ciega.

## Contexto

- El watcher (wiki-watch.py) detecta archivos nuevos en raw/ pero solo notifica. Nunca ejecuta ingest autom?tica. El humano o agente decide el momento.

## Implementación

- wiki-watch.py hace polling cada 60s -> notifica por stdout. Luego el agente corre ingest.py draft + commit manualmente.

## Fuentes

- [[wiki/sources/super-second-brain-architecture]]

## Enlaces

- [[wiki/_index|Wiki principal]]
