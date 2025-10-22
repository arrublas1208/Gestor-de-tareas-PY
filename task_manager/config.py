from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Base de datos SQLite
DB_PATH = DATA_DIR / "tasks.db"

# Archivos por defecto para import/export
DEFAULT_JSON_EXPORT = DATA_DIR / "tasks_export.json"
DEFAULT_CSV_EXPORT = DATA_DIR / "tasks_export.csv"
DEFAULT_TXT_REPORT = DATA_DIR / "tasks_report.txt"

# Configuración general
APP_NAME = "Gestor de Tareas CLI"
APP_VERSION = "1.0.0"

# Tiempo de espera para peticiones HTTP
HTTP_TIMEOUT = 10