from __future__ import annotations
import argparse
from typing import List

from .services import add_task, list_tasks, get_task, update_task, delete_task, set_status
from .models import Task
from .io_handlers import export_to_json, export_to_csv, import_from_json, import_from_csv, write_txt_report
from .api import fetch_random_quote


def _print_task(t: Task) -> None:
    tags = ",".join(t.tags or [])
    print(f"[{t.id}] {t.title} | {t.status} | {t.priority} | due: {t.due_date or '-'} | tags: {tags}")
    if t.description:
        print(f"    {t.description}")


def cmd_add(args):
    task = Task(
        title=args.title,
        description=args.description,
        status=args.status,
        priority=args.priority,
        due_date=args.due_date,
        tags=args.tags,
    )
    task_id = add_task(task)
    print(f"Tarea creada con id {task_id}")


def cmd_list(args):
    filters = {
        "status": args.status,
        "priority": args.priority,
        "tag": args.tag,
    }
    tasks = list_tasks({k: v for k, v in filters.items() if v})
    if not tasks:
        print("No hay tareas.")
        return
    for t in tasks:
        _print_task(t)


def cmd_update(args):
    updates = {}
    if args.title:
        updates["title"] = args.title
    if args.description is not None:
        updates["description"] = args.description
    if args.status:
        updates["status"] = args.status
    if args.priority:
        updates["priority"] = args.priority
    if args.due_date is not None:
        updates["due_date"] = args.due_date
    if args.tags is not None:
        updates["tags"] = args.tags
    update_task(args.id, updates)
    print("Tarea actualizada.")


def cmd_delete(args):
    delete_task(args.id)
    print("Tarea eliminada.")


def cmd_complete(args):
    set_status(args.id, "done")
    print("Tarea marcada como completada.")


def cmd_export_json(args):
    path = export_to_json(args.path)
    print(f"Exportado a JSON: {path}")


def cmd_import_json(args):
    count = import_from_json(args.path)
    print(f"Importadas {count} tareas desde JSON.")


def cmd_export_csv(args):
    path = export_to_csv(args.path)
    print(f"Exportado a CSV: {path}")


def cmd_import_csv(args):
    count = import_from_csv(args.path)
    print(f"Importadas {count} tareas desde CSV.")


def cmd_report(args):
    path = write_txt_report(args.path)
    print(f"Reporte TXT generado: {path}")


def cmd_quote(args):
    quote = fetch_random_quote()
    if quote:
        print(quote)
    else:
        print("No se pudo obtener la cita. Verifique su conexión.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="task-cli", description="Gestor de Tareas CLI")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Agregar una tarea")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--description")
    p_add.add_argument("--status", choices=["pending", "in_progress", "done"], default="pending")
    p_add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    p_add.add_argument("--due-date", dest="due_date")
    p_add.add_argument("--tags", nargs="*")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="Listar tareas")
    p_list.add_argument("--status", choices=["pending", "in_progress", "done"])
    p_list.add_argument("--priority", choices=["low", "medium", "high"])
    p_list.add_argument("--tag")
    p_list.set_defaults(func=cmd_list)

    # update
    p_upd = sub.add_parser("update", help="Actualizar una tarea")
    p_upd.add_argument("id", type=int)
    p_upd.add_argument("--title")
    p_upd.add_argument("--description")
    p_upd.add_argument("--status", choices=["pending", "in_progress", "done"])
    p_upd.add_argument("--priority", choices=["low", "medium", "high"])
    p_upd.add_argument("--due-date", dest="due_date")
    p_upd.add_argument("--tags", nargs="*")
    p_upd.set_defaults(func=cmd_update)

    # delete
    p_del = sub.add_parser("delete", help="Eliminar una tarea")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(func=cmd_delete)

    # complete
    p_comp = sub.add_parser("complete", help="Marcar tarea como completada")
    p_comp.add_argument("id", type=int)
    p_comp.set_defaults(func=cmd_complete)

    # export/import json
    p_ej = sub.add_parser("export-json", help="Exportar tareas a JSON")
    p_ej.add_argument("--path")
    p_ej.set_defaults(func=cmd_export_json)

    p_ij = sub.add_parser("import-json", help="Importar tareas desde JSON")
    p_ij.add_argument("path")
    p_ij.set_defaults(func=cmd_import_json)

    # export/import csv
    p_ec = sub.add_parser("export-csv", help="Exportar tareas a CSV")
    p_ec.add_argument("--path")
    p_ec.set_defaults(func=cmd_export_csv)

    p_ic = sub.add_parser("import-csv", help="Importar tareas desde CSV")
    p_ic.add_argument("path")
    p_ic.set_defaults(func=cmd_import_csv)

    # report
    p_rep = sub.add_parser("report", help="Generar reporte TXT")
    p_rep.add_argument("--path")
    p_rep.set_defaults(func=cmd_report)

    # quote
    p_quote = sub.add_parser("quote", help="Mostrar una cita motivacional (API)")
    p_quote.set_defaults(func=cmd_quote)

    return parser


def run(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")