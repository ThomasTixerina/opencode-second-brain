---
tags: [bug, memory]
date: 2026-05-27
entityType: bug
---

# flet-rendering-bug

- Flutter Web no renderiza canvas en Chrome 148 y Edge Chromium 148
- Bug conocido: Flutter Issue #184843 - blank screen crossOriginIsolated=true
- Chrome 138+ removed SwiftShader fallback afecta CanvasKit
- Causa raiz: multi-threaded Skwasm falla con crossOriginIsolated=true
- Sin errores en consola JS - el engine de Flutter nunca crea el canvas
- Afecta tanto a dart2wasm+skwasm como a dart2js+canvaskit
- Solo Chromium-based browsers afectados

## Enlaces
- [[memory/_index|Todas las memorias]]
