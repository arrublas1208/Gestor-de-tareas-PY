from __future__ import annotations
import json
import csv
from pathlib import Path
from typing import List, Iterable

from .services import list_tasks, add_task
from .models import Task
from .config import DEFAULT_JSON_EXPORT, DEFAULT_CSV_EXPORT, DEFAULT_TXT_REPORT


# JSON

def export_to_json(path: Path | None = None) -> Path:
    path = Path(path or DEFAULT_JSON_EXPORT)
    tasks = [t.to_dict() for t in list_tasks()]
    with path.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    return path


def import_from_json(path: Path) -> int:
    with Path(path).open("r", encoding="utf-8") as f:
        tasks_data = json.load(f)
    count = 0
    for td in tasks_data:
        # Proteger campos calculados
        td.pop("id", None)
        td.pop("created_at", None)
        td.pop("updated_at", None)
        task = Task(**td)
        add_task(task)
        count += 1
    return count


# CSV

CSV_HEADERS = [
    "title",
    "description",
    "status",
    "priority",
    "due_date",
    "tags",  # separadas por coma
]


def export_to_csv(path: Path | None = None) -> Path:
    path = Path(path or DEFAULT_CSV_EXPORT)
    tasks = list_tasks()
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for t in tasks:
            writer.writerow({
                "title": t.title,
                "description": t.description or "",
                "status": t.status,
                "priority": t.priority,
                "due_date": t.due_date or "",
                "tags": ",".join(t.tags or []),
            })
    return path


def import_from_csv(path: Path) -> int:
    count = 0
    with Path(path).open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags = [t.strip() for t in (row.get("tags") or "").split(",") if t.strip()]
            task = Task(
                title=row.get("title") or "",
                description=row.get("description") or None,
                status=row.get("status") or "pending",
                priority=row.get("priority") or "medium",
                due_date=row.get("due_date") or None,
                tags=tags,
            )
            add_task(task)
            count += 1
    return count


# TXT Report

def write_txt_report(path: Path | None = None) -> Path:
    path = Path(path or DEFAULT_TXT_REPORT)
    tasks = list_tasks()
    # Estadísticas usando estructuras: dicts y sets
    stats = {
        "total": len(tasks),
        "by_status": {},
        "by_priority": {},
        "unique_tags": set(),
    }
    for t in tasks:
        stats["by_status"][t.status] = stats["by_status"].get(t.status, 0) + 1
        stats["by_priority"][t.priority] = stats["by_priority"].get(t.priority, 0) + 1
        for tag in (t.tags or []):
            stats["unique_tags"].add(tag)
    lines: List[str] = []
    lines.append("Reporte de tareas\n")
    lines.append(f"Total: {stats['total']}\n")
    lines.append("Por estado:\n")
    for s, c in stats["by_status"].items():
        lines.append(f"- {s}: {c}\n")
    lines.append("Por prioridad:\n")
    for p, c in stats["by_priority"].items():
        lines.append(f"- {p}: {c}\n")
    lines.append("Etiquetas únicas:\n")
    if stats["unique_tags"]:
        lines.append("- " + ", ".join(sorted(stats["unique_tags"])) + "\n")
    else:
        lines.append("- (sin etiquetas)\n")

    with path.open("w", encoding="utf-8") as f:
        f.writelines(lines)
    return path