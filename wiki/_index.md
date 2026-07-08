---
tags: [wiki, index]
updated: 2026-07-08
---

# Wiki de Conocimiento

> Conocimiento compilado y mantenido por IA. Cada página aquí es el resultado de ingerir fuentes, sintetizar información, y mantener conexiones entre ideas.

## Entidades

```dataview
TABLE entityType as Tipo, aliases as Aliases
FROM "wiki/entities"
SORT file.name ASC
```

## Conceptos

```dataview
TABLE category as Categoría
FROM "wiki/concepts"
SORT file.name ASC
```

## Síntesis y Análisis

```dataview
TABLE type as Tipo
FROM "wiki/synthesis"
SORT file.ctime DESC
```

## Fuentes Ingeridas

```dataview
TABLE date as Fecha, source as Fuente
FROM "wiki/sources"
SORT date DESC
```

## Templates

- [[templates/entity|Nueva Entidad]]
- [[templates/concept|Nuevo Concepto]]
- [[templates/synthesis|Nueva Síntesis]]
- [[templates/source-summary|Nuevo Resumen de Fuente]]

## Enlaces

- [[_index|Volver al MOC]]
