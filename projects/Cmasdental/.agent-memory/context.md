---
title: "Contexto activo del agente"
updated: 2026-06-27 07:11
tags:
  - memoria-agente
  - contexto-activo
  - cmasdental
---

# Contexto activo del agente

- **Proyecto**: Cmasdental Larry (WhatsApp AI Assistant)
- **Workflow Activo**: `WhatsApp AI Assistant - Cmasdental (Fixed)` (ID: `FGqn32nnIgMkHC0v`)
  - Webhook Trigger Path: `whatsapp-ycloud` (con autenticacion `headerAuth` activa en produccion)
  - Nodo AI Agent: usa `OpenAI account 3` (`w0MFn0zydLysuX2W`) + Session Memory
  - Corregido error de sintaxis en `systemMessage` del nodo `AI Agent`
- **Predecesor desactivado**: `C+Dental Asistente Principal v2` (ID: `m3S7UtHEavKgbR4j`)

## Estado al 2026-06-27 - PRODUCCION OPERATIVA

### Prueba end-to-end completada exitosamente
- Flujo completo WhatsApp -> YCloud -> n8n -> AI Agent (Larry) -> YCloud -> WhatsApp funcionando.
- El AI capturo: nombre, telefono, servicio, sucursal, fecha, hora de forma conversacional.
- 10+ ejecuciones exitosas en produccion tras recarga de balance OpenAI.

### Fix aplicado: Send to Branch WhatsApp
- **Problema**: el nodo usaba template `notificacion_cita_cmasdental` que NO existe en YCloud.
- **Solucion**: cambiado a `type: text` usando `branch_message` (ya construido en `Prepare Pending`).
  - Endpoint: `https://api.ycloud.com/v2/whatsapp/messages/sendDirectly`
  - Campo: `branch_message` (contiene nombre, telefono, servicio, fecha, hora, sucursal, link confirmacion)
- **Pendiente verificar**: que el mensaje de notificacion llegue al WhatsApp de cada sucursal en cita real.

### Numeros de sucursal a vigilar (posibles duplicados)
- `528119772433` -> asignado a Independencia Y Santa Cruz (confirmar si es intencional)
- `528141622736` -> asignado a Colosio Y Eloy Cavazos (confirmar si es intencional)

## Pendientes

- [ ] Validar que la notificacion al branch WhatsApp llega correctamente en cita real
- [ ] Confirmar si numeros duplicados (Santa Cruz/Independencia y Colosio/Eloy Cavazos) son correctos
- [ ] Crear template `notificacion_cita_cmasdental` en YCloud (recordatorio a pacientes, flujo separado)
- [ ] Corregir warnings del nodo `Describe Image` (parametros no reconocidos: modelId, inputType, imageUrl, text)

## Credenciales en uso (IDs n8n)
- `epMcls2auF34IekT` -> YCloud Webhook Header Auth (autenticacion webhook entrante)
- `yTz9CXQoW45EmRDm` -> YCloud API (envio de mensajes salientes)
- `w0MFn0zydLysuX2W` -> OpenAI account 3

## YCloud
- Numero principal Cmasdental: +528113090909 (WABA ID: 1105621184957446)
- Webhook secret: whsec_597d97bf6ad64b31b524c76bb6528a93 (firma HMAC-SHA256 en header YCloud-Signature)
- Templates aprobadas: nueva_cita_cmasdental, bienvenida_presentacion, bienvenida_contacto, bienvenida_servicios, saludo_inicial
