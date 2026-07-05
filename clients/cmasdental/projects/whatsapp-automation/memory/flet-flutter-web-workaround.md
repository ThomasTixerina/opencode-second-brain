---
tags: [knowledge, memory]
date: 2026-07-05
entityType: knowledge
---

# flet-flutter-web-workaround

- Flet web FLET_APP mode (desktop native) funciona cuando WEB_BROWSER no
- Chrome 146+ tiene bug con Flutter Web canvas rendering (Issue #184843)
- Edge Chromium tiene el mismo bug por ser Chrome-based
- firefox no disponible en este entorno
- COEP/COOP headers removidos de flet_web/fastapi/app.py:161
- canvasKitForceMultiSurfaceRasterizer: true agregado a flutterConfig
- ft.run() vs ft.app(): ambos funcionan igual para web
- ft.AppView.FLET_APP abre ventana nativa de Windows via flet.exe

## Enlaces
- [[_index|Todas las memorias]]
