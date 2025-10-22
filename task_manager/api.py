import requests
from typing import Optional

from .config import HTTP_TIMEOUT

QUOTABLE_URL = "https://api.quotable.io/random"


def fetch_random_quote() -> Optional[str]:
    try:
        resp = requests.get(QUOTABLE_URL, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        content = data.get("content")
        author = data.get("author")
        if content and author:
            return f"\"{content}\" — {author}"
        return content or None
    except Exception:
        return None