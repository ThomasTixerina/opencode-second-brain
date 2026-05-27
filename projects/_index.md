# 📁 Proyectos Activos

> Cada proyecto tiene su espacio con notas, decisiones y contexto.

## Estado

- 🟢 Activo
- 🟡 Pausado
- 🔴 Bloqueado
- ✅ Completado

## Proyectos

```dataview
TABLE status as Estado, started as Inicio
FROM #project
SORT status ASC, started DESC
```

## Templates

- [[templates/project|Template de Proyecto]]
