---
tags: [global, index]
updated: 2026-11-06
---

# Master Index — Estado Global de Proyectos

> Última actualización: 2026-11-06

## cmasdental

### whatsapp-automation
✅ Producción operativa — Asistente IA (Larry) para citas WhatsApp. Flujo end-to-end funcionando: WhatsApp → YCloud → n8n → OpenAI → YCloud → WhatsApp.

---

## dr-tomas-tijerina

### atiende
🟠 Fases 1–4 cerradas — Asistente de IA con WhatsApp dual (YCloud + Baileys de pruebas). Fase 4B-lite implementada y apagada (`WHATSAPP_BAILEYS_ENABLED=false`) hasta emparejar un chip con número real. ADRs `0001–0010`. Código en `C:\Users\user\CRM-Whatsapp` (sin commits). Carpeta: `clients/dr-tomas-tijerina/projects/atiende/`.

### miconsuluno
🟡 Desarrollo — Dashboard dental Python Flet. App de escritorio funcional, modo web con bugs de rendering conocidos.

### nestjs-supabase-auth
🟡 Desarrollo — Librería TypeScript para autenticación Supabase con NestJS y Passport.

### rakazo
✅ Producción — Agente AI self-hosted (alternativa open source a Grok Bot). Stack Docker de imágenes en `C:\Users\user\rakazo-stack` + checkout de código en `C:\Users\user\rakazo`. Acceso local y por Tailscale HTTPS (`https://tomastijerina.taile52a98.ts.net`), apps iOS/Android, autoarranque con Windows, modelo gratuito de OpenRouter. Carpeta: `clients/dr-tomas-tijerina/projects/rakazo/`.

### voice-cli
✅ Producción — Agente de voz TTS (Groq Whisper + edge-tts). Instalado como tarea de inicio en segundo plano.

### dentista-millonario
🟡 Escritura — Trilogía de libros "Dentista Millonario" (skill nobel-bestseller-engine). Tomo 1 "El arte de la Guerra Dental" con borrador redactado; tomos 2 y 3 solo índice. Fase 0 (intake) en curso. Carpeta: `clients/dr-tomas-tijerina/projects/dentista-millonario/`.

---

## second-brain

### wiki (Super Second Brain)
✅ Fase 2 — Pipeline de ingesta de conocimiento tipo LLM Wiki (Karpathy). `raw/` → `wiki/{sources,entities,concepts,synthesis}`. Scripts: `ingest.py`, `lint-wiki.py`, `wiki-watch.py`. Automación vía Task Scheduler (setup-automation.ps1). Wiki Protocol documentado en AGENTS.md.
