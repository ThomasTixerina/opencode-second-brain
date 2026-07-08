---
tags: [source, reference]
source: Super Second Brain ? Architecture & Implementation
url:
date: 2026-07-08
---

# Super Second Brain ? Architecture & Implementation

## Resumen

Arquitectura del Super Second Brain vault: un h?brido entre vault tradicional Obsidian y el patr?n LLM Wiki de Karpathy. Usa scripts Python puros (sin n8n), ingesta estructurada v?a JSON, y watcher con polling para automatizaci?n ligera.

## Puntos clave

1. Arquitectura h?brida combinando vault Obsidian tradicional con patr?n LLM Wiki
2. Sin n8n ? automatizaci?n pura v?a scripts Python + Windows Task Scheduler
3. Human-in-the-loop: watcher notifica pero nunca auto-ingiere
4. Interfaz JSON estructurada entre LLM y pipeline de ingesta
5. Dataview queries para cat?logos din?micos sin mantenimiento manual

## Relacionado con

- 

## Enlaces

- [[wiki/_index|Wiki principal]]
