---
tags: [project, memory, ai, n8n, larry]
date: 2026-05-28
ai-generated: true
---

# Larry Assistant (Cmasdental) - Reparaciones Multimodales y Routing (Mayo 28)

El día de hoy se diagnosticó y reparó exhaustivamente el flujo n8n (ID: FGqn32nnIgMkHC0v) de Larry Assistant.

## Problemas Encontrados y Soluciones

1. **Fallo en Descarga de Audios/Imágenes (YCloud):**
   - *Problema:* El flujo armaba la URL manualmente con el ID, lo cual era incorrecto y causaba error de descarga.
   - *Solución:* Se extrajo la propiedad `msg.audio.link` y `msg.image.link` que YCloud ya provee de forma nativa en el payload.

2. **Fallo en Procesamiento de Modelos (OpenAI Whisper y Vision):**
   - *Problema:* Whisper rechazaba audios sin extensión; Vision intentaba leer un payload binario mal formateado.
   - *Solución:* Se forzó la descarga con extensión (`audio.ogg`, `image.jpeg`). Para Vision, se configuró `gpt-4o-mini` y se construyó correctamente la expresión Base64 en n8n (`{{ 'data:' + $('Filter & Extract').item.json.mediaMime + ';base64,' + $binary.data.data }}`).

3. **Fallo en Ruteo de JSON (Parse Output):**
   - *Problema:* El modelo AI conversaba antes de lanzar el JSON de la agenda, rompiendo el regex original.
   - *Solución:* Se actualizó el Regex para extraer limpiamente el bloque JSON (`/\{"action":"(?:schedule_appointment|escalate)","data":\{.*\}\}/s`) y se actualizó el System Prompt para prohibir estrictamente texto adicional al emitir el JSON final.

4. **Fallo Crítico de Notificación a Sucursal (Send to Branch WhatsApp):**
   - *Problema:* YCloud descartaba la petición porque el JSON Payload estaba totalmente malformado (faltaba `to`, `from`, `type`, y envoltura `template`).
   - *Solución:* Se aplicó un parche al archivo TypeScript y se subió vía n8n-as-code un `jsonBody` perfectamente estructurado bajo la norma Template API de YCloud.

## Roadmap para la Próxima Sesión
- **Pruebas JSON Raw:** Realizar pruebas crudas (Raw JSON) alimentando diferentes modelos de IA para validar consistencia y eficientizar cargas de trabajo delegadas.
- **Multi-plataforma:** Avanzar con Larry Meta y Larry TikTok.