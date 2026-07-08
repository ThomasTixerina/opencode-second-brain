---
tags: [concept]
category: pattern
related:
created: 2026-07-08
updated: 2026-07-08
---

# LLM Wiki

## Definición

- Patr?n de base de conocimiento donde los LLMs generan el contenido pero un humano (o agente) controla qu? se escribe, manteniendo calidad y relevancia.

## Contexto

- Acu?ado por Andrej Karpathy. El Super Second Brain implementa este patr?n con ingest.py (LLM genera JSON), commit (agente revisa y ejecuta), y watcher (solo notifica).

## Implementación

- El pipeline raw/ ? ingest.py draft ? LLM llena JSON ? ingest.py commit ? wiki/ implementa el patr?n: el LLM hace la s?ntesis, el agente decide cu?ndo y qu? commitear.

## Fuentes

- [[wiki/sources/super-second-brain-architecture]]

## Enlaces

- [[wiki/_index|Wiki principal]]
