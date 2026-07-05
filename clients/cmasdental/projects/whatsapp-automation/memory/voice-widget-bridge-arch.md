---
tags: [architecture, memory]
date: 2026-07-05
entityType: architecture
---

# voice-widget-bridge-arch

- BridgeServer: TCP server + subprocess opencode run --format json
- BridgeClient: socket TCP con send_command()
- discover_bridge() lee ~/.opencode/bridge.json
- type_keys() prefiere bridge, fallback a SendKeys
- push_to_talk() acepta stop_event threading.Event para cortar grabación inmediatamente

## Enlaces
- [[_index|Todas las memorias]]
