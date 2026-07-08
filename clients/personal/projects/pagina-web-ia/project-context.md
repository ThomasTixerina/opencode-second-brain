# Pagina Web Creada por IA

**Estado:** Activo
**Stack:** HTML/Tailwind (CDN), n8n, Supabase
**Ubicacion:** `C:\Users\user\pagina-web-ia\`

## Descripcion
Sistema de "fabrica de sitios web con IA" — pipeline de 6 capas que genera
landing pages y sitios web profesionales usando agentes especializados.

## Capas
0. Brief obligatorio (cliente llena)
1. Inteligencia de Mercado
2. Diseno UI/UX (Stitch MCP)
3. Especificacion Tecnica (PM agent)
4. Construccion (HTML/Tailwind o Next.js)
5. Datos/Backend (Supabase MCP)
6. QA/DevOps/Entrega

## REGLA: Sin brief, no se escribe codigo
Ver `AGENTS.md` para la regla completa.

## Comandos
```powershell
cd pagina-web-ia
# Seguir workflow startcycle.md para generar un sitio
```

## Archivos clave
| Archivo | Proposito |
|---------|-----------|
| `AGENTS.md` | Roles del equipo + regla "sin brief" |
| `.agents/workflows/startcycle.md` | Pipeline completo (6 pasos) |
| `.agents/skills/design-to-code.md` | Stitch → Design DNA |
| `.agents/skills/qa-checklist.md` | Checklist de QA |
| `.agents/skills/deploy.md` | Deployment skill |
| `.agents/skills/animation-guidelines.md` | Reglas de motion design |
| `.agents/skills/supabase-schema.md` | Supabase MCP rules |
| `docs/brief-template.md` | Brief maestro para clientes |
| `docs/Technical_Specification.md` | Spec tecnica |
| `docs/DESIGN.md` | Design DNA |
| `docs/MCP-GUIDE.md` | Guia de conexion Supabase |
| `tasks.md` | Task list persistente |

## Primer proyecto: Dr. Tomas Tijerina

**Tipo:** Landing B2B de Consultoría IA para profesionales de salud
**Cliente ideal:** Dentistas, médicos, especialistas, clínicas
**Servicios:** Transformación digital, n8n, marketing, Odoo ERP, IA, estrategia

### Datos del cliente
- **Nombre:** Dr. Tomás Gerardo Tijerina Morales
- **WhatsApp:** 528123546885
- **Dirección:** Av. Lincoln #4516, Col. Valle de las Mitras, Monterrey, Nuevo León
- **Sitio web:** www.drtomastijerina.com
- **Redes:** bit.ly/rrssdrtomastijerina
- **Email:** contacto@drtomastijerina.com

### Estado actual
- Landing HTML/Tailwind completada (hero, servicios, métricas, metodología, testimonios, contacto)
- WhatsApp configurado con mensaje predefinido
- Pendiente: multimedia (fotos, screenshots, video hero)
- Ver `tasks.md` para lista completa

### Archivos del proyecto
```
projects/dr-tijerina/
├── index.html                    ← Landing principal
├── brief.md                      ← Brief completo
├── assets/
│   ├── README.md                 ← Instrucciones de multimedia
│   ├── img/                      ← Fotos y screenshots
│   ├── video/                    ← Videos
│   └── logo/                     ← Logo
└── docs/
    ├── media-guide.md            ← Guía de拍摄 completa
    ├── Technical_Specification.md
    └── DESIGN.md
```

## Proximos pasos
- Completar multimedia del Dr. Tijerina (fotos, screenshots, video)
- QA y deploy
- Probar Stitch MCP en opencode
- Configurar Supabase MCP para proyecto de staging
