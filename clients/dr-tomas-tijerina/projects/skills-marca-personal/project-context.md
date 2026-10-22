# Skills de Marca Personal

## Estado actual
🟢 Activo — Skill `personal-brand-site` implementado, pendiente de prueba real.

## Objetivo del proyecto
Crear un skill de OpenCode que genere sitios web de marca personal **bilingües (ES/EN)** a partir de las redes sociales de una persona. Primero se prueba con los datos del Dr. Tomás Tijerina; después se vende a terceros.

## Arquitectura / stack
- **Skill**: `C:\Users\user\.agents\skills\personal-brand-site\`
- **Runtime**: OpenCode (formato estándar `SKILL.md` + `references/` + `assets/`)
- **Diseño**: MCP de Google Stitch si está disponible, fallback a HTML directo
- **Output**: `index.html` único con Tailwind CDN (cero build, portable)
- **Deploy**: Cloudflare Pages (preferido) / GitHub Pages / Netlify Drop
- **Demo**: `cloudflared tunnel --url http://localhost:8080`

## Decisiones tomadas
- **2026-10-21** — 1 skill con 5 fases internas, no 3 skills separados (un solo comando end-to-end, cada fase invocable单独)
- **2026-10-21** — Bilingüe ES/EN con paridad real vía `data-es`/`data-en`, HTML visible = idioma por defecto (SEO-safe)
- **2026-10-21** — HTML único + Tailwind CDN en lugar de Astro/Next, para que los compradores no necesiten Node
- **2026-10-21** — Stitch **opcional** con fallback obligatorio, para que nadie se quede sin poder usarlo
- **2026-10-21** — LinkedIn = esqueleto (estructura); IG/TikTok = estética; X = voz; YouTube = autoridad; FB = prueba social; web previa = hechos

## Estructura del skill
```
personal-brand-site/
├── SKILL.md                      ← pipeline + reglas conversacionales
├── references/
│   ├── phase-0-intake.md         ← URLs + idioma + objetivo
│   ├── phase-1-recon.md          ← scrapear redes → perfil.md
│   ├── phase-2-strategy.md       ← posicionamiento + copy bilingüe
│   ├── phase-3-design.md         ← Stitch o spec visual
│   ├── phase-4-build.md          ← index.html + checklist técnica
│   └── phase-5-deploy.md         ← publicar + instrucciones de update
└── assets/
    └── perfil-template.md        ← fuente de verdad por persona
```

## Pendientes activos
- [ ] Probar el skill end-to-end con los datos propios (Fase 0 → 5)
- [ ] Generar el sitio personal del Dr. Tomás Tijerina como prueba
- [ ] Validar el toggle bilingüe en móvil real vía túnel
- [ ] Definir modelo de venta (Gumroad vs Polar) y precio
- [ ] Empaquetar para venta: README de instalación + demo grabada
- [ ] Listar en agentskills.io / skills.sh

## Enlaces
- Skill instalado: `C:\Users\user\.agents\skills\personal-brand-site\`
- Referencias estudiadas: `GPZ12138/personal-website-claude-skill`, `debgotwired/website-builder-skill`, `Leonxlnx/taste-skill`, `gabelul/stitch-kit`
- Síntesis Stitch: [[wiki/synthesis/mcp-google-stitch-herramientas|MCP de Google Stitch]]
