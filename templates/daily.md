---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [daily]
---

# <% tp.date.now("YYYY-MM-DD dddd") %>

## 🎯 Enfoque del día

- 

## ✅ Hecho

- 

## 🧠 Aprendizajes

- 

## 🔗 Enlaces

- [[_index|Volver al MOC]]

```dataview
TABLE rows.Hecho AS "Completado"
FROM "daily"
FLATTEN file.lists AS Hecho
WHERE Hecho.checked
GROUP BY file.link
SORT file.day DESC
LIMIT 7
```
