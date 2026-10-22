---
tags: [synthesis, reference, ai, mcp]
type: analysis
sources:
  - https://stitch.withgoogle.com/docs/mcp/setup/
  - https://github.com/davideast/stitch-mcp
created: 2026-10-21
---

# MCP de Google Stitch — Instalación y catálogo de herramientas

## Tesis

Existen dos servidores MCP para Google Stitch (la herramienta de diseño UI con IA de Google Labs), y ambos están **instalados y configurados** en `C:\Users\user\.config\opencode\opencode.json` desde el 2026-10-21:

1. **`stitch`** — el servidor **oficial de Google** (remoto, HTTP). El más usado. 16 herramientas.
2. **`stitch-local`** — el de la comunidad (**`@_davideast/stitch-mcp`**, por Dave East, dev de Google Labs). Proxy local. Expone las mismas 16 **+ 3 exclusivas**.

Ambos usan la **misma API Key** de Stitch.

## Evidencia

### Instalación (config de OpenCode, global)

```jsonc
"stitch": {
  "type": "remote",
  "url": "https://stitch.googleapis.com/mcp",
  "enabled": true,
  "headers": {
    "X-Goog-Api-Key": "<STITCH_API_KEY>"
  }
},
"stitch-local": {
  "type": "local",
  "command": ["npx", "-y", "@_davideast/stitch-mcp", "proxy"],
  "enabled": true,
  "environment": {
    "STITCH_API_KEY": "<STITCH_API_KEY>"
  }
}
```

### Obtener la API Key

1. Ir a https://stitch.withgoogle.com/settings
2. Sección **API Keys** → **Create API Key**
3. La misma key sirve para los dos servidores

### Las 16 herramientas del servidor oficial

**Proyectos**
| Herramienta | Función |
|-------------|---------|
| `create_project` | Crea un proyecto de diseño |
| `list_projects` | Lista proyectos (filtro `view=owned` / `view=shared`) |
| `get_project` | Detalle del proyecto, incluye `screenInstances` |
| `delete_project` | Elimina un proyecto |

**Pantallas**
| Herramienta | Función |
|-------------|---------|
| `generate_screen_from_text` | Genera pantalla desde prompt (`modelId`: `GEMINI_3_FLASH` o `GEMINI_3_1_PRO`) |
| `edit_screens` | Edita pantallas por texto (`selectedScreenIds`) |
| `generate_variants` | Genera variantes (count, creative range, aspects) |
| `list_screens` | Pantallas de un proyecto |
| `get_screen` | Pantalla con `htmlCode` y `screenshot` |

**Design Systems**
| Herramienta | Función |
|-------------|---------|
| `create_design_system` | Crea tokens (colores, tipografías, roundness, spacing) |
| `update_design_system` | Actualiza tokens |
| `list_design_systems` | Lista los de un proyecto |
| `apply_design_system` | Aplica a `selectedScreenInstances` |

**Design Markdown (DESIGN.md)**
| Herramienta | Función |
|-------------|---------|
| `create_design_system_from_design_md` | Design system desde archivo DESIGN.md |
| `upload_design_md` | Sube un DESIGN.md |

**Archivos**
| Herramienta | Función |
|-------------|---------|
| `download_file` | Descarga HTML/imágenes/screenshots |

### Las 3 herramientas exclusivas de `stitch-local`

| Herramienta | Función |
|-------------|---------|
| `build_site` | Genera un sitio **Astro** mapeando pantallas a rutas (`projectId` + `routes[{screenId, route}]`) |
| `get_screen_code` | Descarga el HTML del diseño |
| `get_screen_image` | Descarga el screenshot en base64 |

Combinación típica: el oficial **genera** el diseño → `stitch-local` **exporta** el código a tu entorno de desarrollo.

### CLI de stitch-local (sin MCP)

```bash
npx @_davideast/stitch-mcp init        # Asistente de auth + config MCP
npx @_davideast/stitch-mcp doctor      # Diagnóstico
npx @_davideast/stitch-mcp serve -p <id>   # Preview en Vite dev server
npx @_davideast/stitch-mcp site -p <id>    # Genera proyecto Astro
npx @_davideast/stitch-mcp view --projects # Navegador interactivo
npx @_davideast/stitch-mcp tool [name]     # Invoca tools desde terminal
```

### Popularidad (GitHub, oct-2026)

| Repo | ⭐ | Nota |
|------|---|------|
| `google-labs-code/stitch-skills` | 8,538 | Skills de agente para el MCP oficial |
| `davideast/stitch-mcp` | 982 | El MCP de comunidad más usado |
| `gemini-cli-extensions/stitch` | 479 | Extensión oficial para Gemini CLI |
| `Kargatharaakash/stitch-mcp` | 121 | Alternativa "universal" |

## Contradicciones

- La documentación oficial recomienda **OAuth + gcloud** para entornos zero-trust, pero para uso personal la **API Key es más práctica** (no expira cada hora como el access token de gcloud).
- `davideast/stitch-mcp` se declara **experimental y no afiliado a Google**, pese a estar mantenido por un empleado de Google Labs. Usar bajo esa premisa.

## Conclusión

Instalación completa y verificada (el handshake HTTP 200 y `list_projects` devolvieron el proyecto *"Dr. Tomás Tijerina Hero Section"*). **Requiere reiniciar OpenCode** para que carguen las herramientas de `stitch-local`, que tarda 10–30 s la primera vez por la descarga vía npx.

## Enlaces

- [[wiki/_index|Wiki principal]]
- [[wiki/entities/andrej-karpathy|Andrej Karpathy]]
