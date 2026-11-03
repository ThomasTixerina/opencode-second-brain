---
tags: [project, atiende, whatsapp, status]
date: 2026-10-27
entityType: project
---

# Atiende

App para crear, configurar y poner a trabajar un asistente de IA que atiende a
los clientes de un negocio local por WhatsApp y chat web: responde con la
información del negocio, agenda en Google Calendar, avisa y pasa a una persona
cuando hace falta. La agencia la instala por cliente; todo se configura desde
el panel.

## Ubicaciones

- **Código:** `C:\Users\user\CRM-Whatsapp` (repo local, sin commits aún)
- **Propuesta formal:** `docs/proposals/0001-atiende-asistente-whatsapp.md`
- **Copia del plan de trabajo:** `C:\Users\user\.opencode\plan\atiende-plan.md`
- **Index de propuestas:** `docs/proposals/README.md`

## Estado al 2-nov-2026

- Fases 1–4 completas: andamiaje/auth/panel, motor de conversaciones con
  OpenRouter, integraciones (Calendar best-effort) y canales WhatsApp con
  YCloud: cola de salida, ventana de 24 h, plantillas, recordatorios y panel de
  Canales.
- **Fase 4B-lite (canal de pruebas Baileys) implementada y revisada**:
  veredicto `PASS WITH COMMENTS`, sin bloqueantes. Conector dentro del worker
  (ADR-0010), sesión cifrada `v1:` (ADR-0005), QR solo ADMIN en Canales y
  borrado de sesión desde el panel (ADR-0006).
- `WHATSAPP_BAILEYS_ENABLED="false"` hasta tener un chip o eSIM con SMS/voz.
  Un eSIM de datos (Airalo, Holafly) no sirve para emparejar WhatsApp.
- 111 pruebas en 16 archivos; typecheck, lint y `next build` limpios.
- Código de la app **sin commits** (solo el commit de docs `10ef118`); el repo
  espera petición explícita.
- Deuda conocida de 4B: acuses de entrega/lectura, reinicio del conector tras
  borrar sesión, fallback de LID sin `senderPn` y 21 avisos de `npm audit`.

### Grietas de implementación (histórico)

- Prisma 7 exige `prisma.config.ts` (URL fuera del schema, con
  `datasource.url` y `shadowDatabaseUrl`); 1-1 con FK necesita `@unique`
  (`logoAssetId`/`avatarAssetId`).
- Windows: `spawn` de `.cmd` exige `shell: true` (node 26, EINVAL).
- Horarios multi-turno viajan como `hoursJson` desde el editor cliente.
- `scripts/dev.mjs` debe quitar las comillas del `.env` como Next; si no, el
  worker lee `"true"` y nunca enciende el conector.

## Stack

Next.js 16 App Router, React 19, TypeScript, Tailwind 4, shadcn/ui, Prisma 7.10
con PostgreSQL (`@prisma/dev` en local, sin necesidad de Docker), Zod 4, SDK de
OpenAI apuntando a OpenRouter (modelo por defecto `anthropic/claude-haiku-5.5`).

Dos procesos con la misma imagen: `web` (panel, API, OAuth, widget, SSE, demo) y
`worker` (turnos de IA, scheduler, transporte WhatsApp). PostgreSQL es estado,
cola y bus de eventos.

## Decisiones clave

- Canal WhatsApp **dual por adaptador**: `YCloudProvider` oficial (clientes) y
  `BaileysProvider` solo pruebas, tras interfaz `WhatsAppProvider`.
- Un proveedor activo por instalación; Baileys apagado por defecto en producción.
- Citas en dos pasos: propuesta y confirmación explícita del cliente.
- Handoff silencia al asistente y marca atención; híbrido palabras clave + modelo.
- Ventana de 24 h por `lastInboundAt`; fuera solo plantillas ya aprobadas.
- Auth propia con sesiones en base y `scrypt`; sin Auth.js.
- Cifrado AES-256-GCM versionado; tokens nunca al navegador.
- Producción: compose único con Traefik y sin puertos publicados.

## Pendientes

1. Conseguir un chip o eSIM con SMS/voz y emparejar el QR de Baileys
   (`WHATSAPP_BAILEYS_ENABLED="true"` solo durante la prueba). Nunca la línea
   personal ni el número principal del negocio.
2. Probar el ciclo completo por Baileys: entrante → respuesta del asistente →
   salida. Después, verificar un envío real por YCloud (faltan API key y
   número).
3. Cerrar la deuda de 4B: acuses de entrega/lectura, reinicio del conector tras
   reset y fallback de LID.
4. No ejecutar `sync-memory.py to-vault --client dr-tomas-tijerina --project
   atiende`: el script copia toda la memoria global (47 entidades) al subárbol
   del proyecto porque no filtra por proyecto. La copia se borró el 2-nov.

## Enlaces

- [[second-brain/00-global/master-index|Master index]]
- Documentación YCloud: `https://docs.ycloud.com/reference/introduction`
