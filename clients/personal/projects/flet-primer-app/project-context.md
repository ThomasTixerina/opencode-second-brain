# Flet Primer App

**Estado:** Activo
**Stack:** Flet 0.85.3, Python 3.13.7
**Ubicación:** `C:\Users\user\flet-primer-app\`

## Descripción

Proyecto de aprendizaje y prototipado con Flet para Python. App de escritorio nativa (FLET_APP) con componentes UI interactivos.

## Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Entry point de la app Flet |
| `venv/` | Entorno virtual (gitignored) |
| `requirements.txt` | Dependencias: flet, python-dotenv |

## Funcionalidades implementadas

- Formulario de contacto con campos: Nombre, Email, Fecha (DatePicker), Mensaje
- Validación de campos requeridos
- Diálogo de confirmación al enviar
- Tema claro

## Comandos

```powershell
.\venv\Scripts\Activate.ps1   # Activar entorno
python main.py                 # Ejecutar app
```

## Dependencias

- `flet>=0.84.0`
- `python-dotenv>=1.0.0`

## Próximos pasos

- Validación de email con regex
- Guardar datos a JSON/DB
- Más campos (selectores, checkboxes)
- Navegación entre vistas
- Tema oscuro toggle
