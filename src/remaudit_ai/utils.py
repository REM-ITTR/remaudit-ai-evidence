from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

def safe_relpath(p: Path, root: Path) -> str:
    return str(p.relative_to(root)).replace("\\", "/")
