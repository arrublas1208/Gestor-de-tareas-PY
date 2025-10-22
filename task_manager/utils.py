from __future__ import annotations
from datetime import datetime
from typing import Iterable, List

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def now_iso() -> str:
    return datetime.now().strftime(ISO_FORMAT)


def parse_date(date_str: str | None) -> str | None:
    if not date_str:
        return None
    try:
        # Acepta fechas en formato YYYY-MM-DD y retorna ISO con media noche
        dt = datetime.strptime(date_str, DATE_FORMAT)
        return dt.strftime(ISO_FORMAT)
    except ValueError:
        raise ValueError("La fecha debe estar en formato YYYY-MM-DD")


def normalize_tags(tags: Iterable[str] | None) -> List[str]:
    if not tags:
        return []
    # Quitar espacios, vacíos y duplicados
    cleaned = [t.strip() for t in tags if t and t.strip()]
    # Mantener orden pero eliminar duplicados con un set de vistos
    seen = set()
    result = []
    for t in cleaned:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result