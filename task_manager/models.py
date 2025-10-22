from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import json

from .exceptions import DataValidationError
from .utils import now_iso, parse_date, normalize_tags

VALID_STATUSES = {"pending", "in_progress", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


@dataclass
class Task:
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[str] = None  # ISO string
    tags: List[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        # Normalizar valores
        if self.status not in VALID_STATUSES:
            raise DataValidationError("Estado inválido. Use pending, in_progress o done.")
        if self.priority not in VALID_PRIORITIES:
            raise DataValidationError("Prioridad inválida. Use low, medium o high.")
        self.due_date = parse_date(self.due_date) if self.due_date else None
        self.tags = normalize_tags(self.tags or [])
        if not self.title or not self.title.strip():
            raise DataValidationError("El título es obligatorio.")

    def to_db_tuple(self) -> tuple:
        # Asegurar timestamps
        created = self.created_at or now_iso()
        updated = now_iso()
        return (
            self.title,
            self.description,
            self.status,
            self.priority,
            self.due_date,
            json.dumps(self.tags, ensure_ascii=False),
            created,
            updated,
        )

    @staticmethod
    def from_row(row) -> "Task":
        tags = []
        try:
            if row["tags"]:
                tags = json.loads(row["tags"]) or []
        except Exception:
            tags = []
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            priority=row["priority"],
            due_date=row["due_date"],
            tags=tags,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d