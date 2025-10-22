from task_manager.cli import run
from task_manager.db import init_db

if __name__ == "__main__":
    # Inicializa la BD si no existe
    init_db()
    run()