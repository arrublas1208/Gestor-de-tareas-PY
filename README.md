# Gestor de Tareas CLI (Python)

Proyecto mini, profesional y 100% Python para tu portafolio. Muestra organización por módulos, manejo de archivos (CSV/JSON/TXT), estructuras de datos, SQLite, consumo de una API pública y una interfaz CLI con `argparse`.

## Objetivos
- CRUD de tareas con SQLite.
- Importación/exportación a CSV y JSON; reporte en TXT.
- Validación de datos y manejo de excepciones.
- Consumo de API pública (cita motivacional) con `requests`.
- Estructura modular, funciones reutilizables y comentarios claros.

## Estructura del proyecto
```
python/
├─ main.py
├─ requirements.txt
├─ data/
│  ├─ sample_tasks.csv
│  ├─ sample_tasks.json
│  ├─ motd.txt
└─ task_manager/
   ├─ __init__.py
   ├─ config.py
   ├─ db.py
   ├─ exceptions.py
   ├─ utils.py
   ├─ models.py
   ├─ services.py
   ├─ io_handlers.py
   ├─ api.py
   └─ cli.py
```

## Instalación
1) Crear entorno virtual (Windows PowerShell):
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias:
```
pip install -r requirements.txt
```

3) Inicializar BD (automático al ejecutar el programa):
```
python main.py --help
```

## Uso rápido (CLI)
- Agregar tarea:
```
python main.py add --title "Comprar leche" --description "Ir al super" --priority high --due-date 2025-10-25 --tags compras supermercado
```

- Listar tareas (todas o por filtros):
```
python main.py list
python main.py list --status pending
python main.py list --priority high
python main.py list --tag python
```

- Actualizar tarea:
```
python main.py update 1 --status in_progress --priority medium
```

- Completar y eliminar:
```
python main.py complete 1
python main.py delete 2
```

- Exportar/Importar:
```
python main.py export-json --path data\tareas.json
python main.py import-json data\sample_tasks.json
python main.py export-csv --path data\tareas.csv
python main.py import-csv data\sample_tasks.csv
```

- Reporte TXT:
```
python main.py report --path data\reporte.txt
```

- Cita motivacional (API):
```
python main.py quote
```

## Decisiones de diseño
- SQLite (`sqlite3`): Tabla `tasks` con `status` y `priority` validados; `tags` en JSON.
- Validación y normalización: `models.Task` valida estado, prioridad, fecha y etiquetas.
- Estructuras de datos: diccionarios para filtros/estadísticas, listas y sets para etiquetas únicas.
- Manejo de errores: Excepciones específicas (`DataValidationError`, `NotFoundError`) y mensajes amigables en CLI.
- IO de archivos: `io_handlers.py` gestiona CSV/JSON/TXT con codificación UTF-8.
- API pública: `quotable.io` para una cita breve y segura.

## Extensiones posibles (ideas)
- Tests unitarios con `pytest`.
- Interfaz web ligera con Flask.
- Recordatorios y notificaciones.
- Campos adicionales (estimación de tiempo, subtareas).

## Licencia
Uso libre para tu portafolio.