# Project Context — Rakazo (agente AI self-hosted)

#project

## Identificación

- **Proyecto:** Rakazo — agente AI open source, self-hosted, alternativa a Grok Bot
- **Repo:** https://github.com/elie222/rakazo (Apache-2.0, ~7.3k estrellas)
- **Uso previsto:** asistente personal con bots persistentes ("Chief"), memoria, rutinas y acceso a computadora
- **Máquina:** `C:\Users\user` — Windows, Docker Desktop 29.1.5 (backend WSL2/Linux)
- **Inicio:** 2026-11-06

## Qué es y qué NO es

Rakazo es un **agente con herramientas**: cada bot tiene conversaciones, memoria, rutinas y una
"computer" (contenedor Docker con navegador, terminal, archivos y escritorio gráfico). No es un chat
de LLM: es infraestructura de agente. Por eso exige modelos con **tool-calling** y, para las capturas
del escritorio, **visión**.

## Dos instalaciones en la máquina (importante)

| Ruta | Qué es | Estado |
|------|--------|--------|
| `C:\Users\user\rakazo` | **Checkout del código** (`pnpm dev`). Editable, hot reload, sin `restart:` | Detenido. Solo para desarrollo |
| `C:\Users\user\rakazo-stack` | **Stack de imágenes publicadas** (`ghcr.io/elie222/rakazo/app:edge`). Es la instancia real | **Activo** |

Las dos usan bases de datos **separadas**: el checkout usa el contenedor `rakazo-dev-postgres`
(puerto 54318, detenido); el stack usa su propio volumen `pgdata`. La cuenta y los bots viven en el
stack. Arrancar `pnpm dev` muestra una instancia vacía distinta.

## Configuración activa del stack

```
C:\Users\user\rakazo-stack\
  docker-compose.images.yml   (copia de infra/compose del repo)
  .env                        (secretos generados + OpenRouter)
  start.cmd / stop.cmd
```

`.env` clave:

```env
RAKAZO_IMAGE=ghcr.io/elie222/rakazo/app
RAKAZO_IMAGE_TAG=edge
SANDBOX_PROVIDER=docker
SANDBOX_COMPUTER_EGRESS=open        # Docker Desktop no puede aplicar reglas iptables
PI_DEFAULT_PROVIDER=openrouter
PI_DEFAULT_MODEL=nvidia/nemotron-3.5-super-vl:free
BETTER_AUTH_URL=https://tomastijerina.taile52a98.ts.net
WEB_ORIGIN=https://tomastijerina.taile52a98.ts.net
API_URL=https://tomastijerina.taile52a98.ts.net
RAKAZO_HOST=tomastijerina.taile52a98.ts.net
```

Servicios: postgres, api, worker, web, supervisor (+ one-shot migrate, data-init, computer).
Todos los permanentes con `restart: unless-stopped`.

## Acceso

| Vía | URL |
|-----|-----|
| Local | `http://127.0.0.1:5173` |
| Tailscale HTTPS | `https://tomastijerina.taile52a98.ts.net` |
| Celular | App Rakazo (App Store `id6801531099` / Play `com.rakazo.app`) + Tailscale, "Use a custom server" con la URL https |

Tailscale: equipo `tomastijerina` (100.104.177.56), tailnet `taile52a98.ts.net`.
`tailscale serve --bg 5173` publica el web con certificado Let's Encrypt. Serve debe estar habilitado
a nivel de tailnet (https://login.tailscale.com/f/serve).

## Autoarranque con Windows

- Tarea programada: **"Rakazo - Docker Desktop al iniciar sesion"** (delay 20 s, ejecuta Docker Desktop).
- Entrada en `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` → `Docker Desktop`.
- Docker Desktop tenía `AutoStart: False` en `%APPDATA%\Docker\settings-store.json`.
- Cadena: login → tarea arranca Docker → contenedores con `unless-stopped` vuelven solos.
- **Sin verificar con reinicio real.** Si falla, subir el delay a 60 s.

## Modelos (OpenRouter)

La API key se tomó de `~/.local/share/opencode/auth.json` (proveedor `openrouter`).

**Cambio hecho en la cuenta de OpenRouter** (2026-11-06): Privacy → Zero Data Retention →
**"All other models" desactivado**. Sin eso todos los modelos `:free` fallaban con
`zdr-violation-by-account`. Se dejaron con ZDR: Anthropic, OpenAI, Google, SpaceXAI.
"Allow free endpoints that train" ya estaba activo (los free pueden entrenar con el contenido).

Ojo: el toggle **no se aplica hasta pulsar "Save changes"** y su API tarda ~1 min en propagar.

### Escalera de modelos, verificada con llamadas reales

| Modelo | $/M in | $/M out | Tool-calls | Veredicto |
|---|---|---|---|---|
| `nvidia/nemotron-3.5-super-vl:free` | 0 | 0 | ✅ correcto | **activo**, 1M ctx, visión |
| `deepseek/deepseek-v4.1-flash` | 0.051 | 0.567 | ✅ correcto | **mejor pago**, 1M ctx, visión |
| `anthropic/claude-haiku-5.5` | 0.10 | 0.50 | ✅ | sólido, 4x más caro |
| `qwen/qwen3.7-flash` | 0.03 | 0.13 | ❌ no llama herramientas | el más barato, inservible como agente |
| `openai/gpt-5-nano` | 0.05 | 0.40 | ❌ no llama herramientas | descartado |
| `google/gemma-4-31b-it:free` | 0 | 0 | bloqueado por ZDR de Google | descartado |

Estimación: 100 turnos/día (20k in + 800 out) ≈ $4.4/mes con DeepSeek, $7.2 con Haiku.
A ese nivel de gasto el precio deja de ser el criterio; manda la calidad.

Free tier de OpenRouter: ~1000 req/día y 20/min si la cuenta ya compró crédito. Si el bot deja de
responder un día, es el límite, no Rakazo.

## Parches locales por Windows (en el checkout)

El repo asume Unix en la ruta de arranque de desarrollo. Dos archivos modificados:

1. `apps/api/src/cli/migrate-database.ts` — usaba `execFileSync("pnpm", …)` (en Windows `pnpm` es
   `.cmd`, no es ejecutable por execFileSync) y el comando `pwd`. Ahora resuelve `packages/db`
   con `fileURLToPath(import.meta.url)`.
2. `packages/db/src/deferred-migrations.ts` — mismo `execFileSync("pnpm", …)` al lanzar
   `prisma migrate deploy`. Ahora usa `npm_execpath` + `process.execPath` en win32.

Quedan **8 call sites sin arreglar en `packages/testkit/`** (screenshots móviles y e2e). No afectan
el uso normal, pero `pnpm test:e2e` fallará en Windows.

Además, `pnpm dev` puede caerse la primera vez por una carrera con el `initdb` de Postgres (la
conexión inicial se corta cuando el contenedor reinicia internamente). Solución: relanzarlo.

## Limitación de automatización del navegador

La web de Rakazo **no expone árbol de accesibilidad** (snapshot devuelve ~15 líneas vacías), así que
las herramientas `browser.click/fill/files.upload` no sirven: requieren refs. Hay que interactuar con
`browser.evaluate` (setter nativo + `dispatchEvent('input')`) y buscar botones por `aria-label`.
Consecuencia: **no se puede adjuntar archivos por automatización**; el usuario debe arrastrarlos.

## Estado verificado (2026-11-06)

- 5/5 contenedores healthy; `https://…ts.net` → 200; consola del navegador sin errores.
- Cuenta creada (1 usuario), bot **Chief** operativo.
- Run real registrado en tabla `runs`: `openrouter` + `nvidia/nemotron-3.5-super-vl:free`, `completed`.
- Prueba con el manuscrito de *Dentista Millonario* (apertura, 4.225 chars): respuesta editorial
  concreta, citando el texto. Coste del run: **$0**.

## Comandos

```powershell
cd C:\Users\user\rakazo-stack
docker compose --env-file .env -f docker-compose.images.yml ps
docker compose --env-file .env -f docker-compose.images.yml up -d --wait
.\start.cmd     # arrancar
.\stop.cmd      # detener
docker compose --env-file .env -f docker-compose.images.yml logs --tail 50 api
```

Actualizar imágenes: `docker compose --env-file .env -f docker-compose.images.yml pull` + `up -d`.

## Secretos

`C:\Users\user\rakazo-stack\.env` — 6 secretos generados (POSTGRES_PASSWORD, POSTGRES_APP_PASSWORD,
BETTER_AUTH_SECRET, ENCRYPTION_KEY, SCREEN_PROXY_SECRET, SANDBOX_SUPERVISOR_TOKEN) + OPENROUTER_API_KEY.
**ENCRYPTION_KEY no se puede perder**: sin ella el contenido cifrado es irrecuperable.
El `.env` del checkout está en `.gitignore` (línea 14). El directorio del stack no es repo git.

## Pendientes

- [ ] Verificar el autoarranque con un reinicio real de Windows
- [ ] Probar la subida de archivos desde el celular/web (arrastrar `libro-1-v2.md`)
- [ ] Análisis del manuscrito completo (16 capítulos, 64 KB) — solo se probó la apertura
- [ ] Decidir política ZDR a largo plazo (free con entrenamiento vs pago con privacidad)
- [ ] Instalar la app en el celular y validar la conexión por Tailscale
- [ ] Opcional: arreglar los 8 `execFileSync("pnpm")` de `packages/testkit/` y mandar PR upstream
