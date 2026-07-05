---
tags: [session, memory]
date: 2026-07-05
entityType: session
---

# voice-widget-bridge-2026-06-09

- Objetivo: implementar bridge IPC entre Voice Widget y OpenCode, y corregir bug en push-to-talk
- Arquitectura: BridgeServer TCP + subprocess opencode run --format json (one-shot por comando)
- BridgeClient: socket TCP + send_command() con reintentos
- PTT fix: stop_event threading.Event en push_to_talk, checkeado en while loop
- voice-bridge.py: entry point standalone
- audio.py: bridge-aware type_keys() con fallback SendKeys, set_bridge_client(), get_bridge_client()
- app.py: bridge discovery en _start_agent, auto-spawn bridge subprocess, _on_bridge_resp callback, _ptt_stop_event, _start_bridge()
- voice.ps1: flag --bridge para standalone y para --widget --bridge
- Toda la sintaxis verificada correcta, bridge.py importable

## Enlaces
- [[_index|Todas las memorias]]
