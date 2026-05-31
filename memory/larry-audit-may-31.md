---
tags: [larry, audit, memory, n8n]
date: 2026-05-31
entityType: audit
---

# Auditoría de Larry Assistant (31 de Mayo, 2026)

Se realizó una auditoría completa del flujo `WhatsApp AI Assistant - Cmasdental (Fixed).workflow.ts` (ID: `FGqn32nnIgMkHC0v`) recientemente descargado. Aquí se detallan los hallazgos en los 4 puntos críticos del sistema:

## 1. Descarga y Procesamiento Multimedia (Audio/Imagen)
*   **Detección y Extracción:** En `FilterExtract`, se obtienen correctamente las URLs de YCloud usando `msg.audio.link` y `msg.image.link`.
*   **Whisper (Audio):** En `DownloadAudio`, se forzó el guardado temporal como `audio.ogg` para evitar rechazos en el nodo de OpenAI Transcribe.
*   **Vision (Imagen):** En `DescribeImage`, se inyecta la imagen en Base64 utilizando la sintaxis de n8n para unir el MimeType dinámico: `data:' + $('Filter & Extract').item.json.mediaMime + ';base64,' + $binary.data.data`.
*   *Estatus:* **Robusto y sin errores.**

## 2. Comportamiento y System Prompt del Agente (AiAgent)
*   **Personalidad:** Eres Larry, empático y humano. Se limitan las respuestas a 2-3 líneas para evitar textos excesivamente largos.
*   **Reglas de Interacción:** Saluda solo al inicio absoluto, maneja el dolor con empatía, no presiona para agendar y recopila datos uno por uno.
*   **Precios y Ubicaciones:** Utiliza los precios de referencia de 2026 en efectivo y aclara el diagnóstico gratuito. Al preguntar por sucursales, solicita el municipio antes de listar.
*   *Estatus:* **Bien estructurado.** Se depende fuertemente del Regex en el siguiente nodo por si el modelo emite texto adicional junto al JSON final.

## 3. Ruteo y Parseo de Citas (ParseOutput / BranchLookup)
*   **ParseOutput:** Utiliza un bloque `try/catch` para intentar parsear el JSON directo del agente. Si falla, aplica la expresión regular `/\{"action":"(?:schedule_appointment|escalate)","data":\{.*\}\}/s` para extraer el JSON limpio.
*   **BranchLookup:** Contiene la base de datos de las 24 sucursales oficiales con horarios y enlaces a Google Maps.
*   **Normalización:** Emplea una función `normalize(str)` para remover acentos y realizar búsquedas de coincidencia parcial tolerantes. Si no encuentra la sucursal, responde al usuario con la lista de opciones disponibles de forma conversacional.
*   *Estatus:* **Excelente.** La normalización de acentos previene fallos comunes de coincidencia de texto.

## 4. Notificaciones y Tiempos de Espera (Timeout / Escalamientos)
*   **Webhook de Sucursal:** `SendToBranchWhatsapp` envía el template `notificacion_cita_cmasdental` a la sucursal correspondiente.
*   **Espera de Confirmación:** El nodo `WaitForConfirmation` espera 30 minutos a que la sucursal responda mediante el portal web de confirmación.
*   **Errores Críticos Identificados:**
    *   `SendTimeoutNotification` (Notificación de sucursal inactiva) tiene hardcodeado el número de destino como `'528113090909'`.
    *   `SendEscalation` (Notificación de quejas de pacientes) también tiene hardcodeado el número de destino como `'528113090909'`.
    *   *Problema:* `528113090909` es el número del Bot de WhatsApp YCloud (el remitente/remite). Si YCloud no permite que el bot se envíe mensajes a sí mismo, o si el administrador de la clínica usa un número personal diferente, el administrador nunca recibirá las alertas de queja ni las alertas de sucursal inactiva.
*   *Estatus:* **Requiere Corrección.** Se debe cambiar el número de destino en estos dos nodos por el número personal real del administrador.

## Enlaces
- [[memory/_index|Todas las memorias]]
- [[projects/second-brain-plan|Plan del Segundo Cerebro]]
