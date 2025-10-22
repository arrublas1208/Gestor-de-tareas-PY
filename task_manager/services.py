from __future__ import annotations
import sqlite3
from typing import List, Optional, Dict, Any

from .db import get_connection, init_db
from .models import Task
from .exceptions import NotFoundError


def add_task(task: Task) -> int:
    conn = get_connection()
    try:
        init_db(conn)
        cur = conn.execute(
            """
            INSERT INTO tasks (title, description, status, priority, due_date, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            task.to_db_tuple(),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_tasks(filters: Optional[Dict[str, Any]] = None) -> List[Task]:
    filters = filters or {}
    where = []
    params = []
    if status := filters.get("status"):
        where.append("status = ?")
        params.append(status)
    if priority := filters.get("priority"):
        where.append("priority = ?")
        params.append(priority)
    if tag := filters.get("tag"):
        where.append("tags LIKE ?")
        params.append(f"%\"{tag}\"%")  # busca en JSON
    sql = "SELECT * FROM tasks"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY due_date IS NULL, due_date ASC, priority DESC, created_at DESC"
    conn = get_connection()
    try:
        init_db(conn)
        rows = conn.execute(sql, params).fetchall()
        return [Task.from_row(r) for r in rows]
    finally:
        conn.close()


def get_task(task_id: int) -> Task:
    conn = get_connection()
    try:
        init_db(conn)
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise NotFoundError(f"No existe la tarea con id {task_id}")
        return Task.from_row(row)
    finally:
        conn.close()


def update_task(task_id: int, updates: Dict[str, Any]) -> None:
    # Cargar actual y aplicar cambios validados con Task
    current = get_task(task_id)
    for k, v in updates.items():
        setattr(current, k, v)
    # recrear para validar
    validated = Task(**current.to_dict())
    conn = get_connection()
    try:
        init_db(conn)
        conn.execute(
            """
            UPDATE tasks SET title=?, description=?, status=?, priority=?, due_date=?, tags=?, updated_at=datetime('now')
            WHERE id=?
            """,
            (
                validated.title,
                validated.description,
                validated.status,
                validated.priority,
                validated.due_date,
                json_dump(validated.tags),
                task_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def delete_task(task_id: int) -> None:
    conn = get_connection()
    try:
        init_db(conn)
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    finally:
        conn.close()


def set_status(task_id: int, status: str) -> None:
    update_task(task_id, {"status": status})


def find_by_tag(tag: str) -> List[Task]:
    return list_tasks({"tag": tag})


def json_dump(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False)