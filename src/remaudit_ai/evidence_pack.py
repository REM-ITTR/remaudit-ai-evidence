from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List

from .utils import write_text, read_text, sha256_file, canonical_json, safe_relpath

def build_ai_evidence_pack(incident_dir: Path, out_dir: Path, run_id: str) -> Path:
    if not incident_dir.exists():
        raise FileNotFoundError(f"incident-dir not found: {incident_dir}")

    pack_root = out_dir / f"REMAuditAI_INCIDENT_{run_id}_{incident_dir.name}"
    raw_dir = pack_root / "raw"
    art_dir = pack_root / "artifact"

    raw_dir.mkdir(parents=True, exist_ok=True)
    art_dir.mkdir(parents=True, exist_ok=True)

    frozen_files = ["incident.json", "updates.jsonl", "policy_v1.txt", "policy_v2.txt"]
    for fn in frozen_files:
        src = incident_dir / fn
        if src.exists():
            (raw_dir / fn).write_bytes(src.read_bytes())

    incident = json.loads(read_text(incident_dir / "incident.json"))
    updates_path = incident_dir / "updates.jsonl"
    updates: List[Dict[str, Any]] = []
    if updates_path.exists():
        for line in read_text(updates_path).splitlines():
            line = line.strip()
            if not line:
                continue
            updates.append(json.loads(line))

    lines = []
    lines.append("# REMAudit-AI — Incident Evidence Report")
    lines.append("")
    lines.append(f"Incident ID: `{incident.get('incident_id')}`")
    lines.append(f"Title: {incident.get('title')}")
    lines.append(f"System: {incident.get('system')}")
    lines.append(f"Date (UTC): {incident.get('date_utc')}")
    lines.append("")
    lines.append("## Update Chain")
    for u in updates:
        lines.append(f"- {u.get('update_id')} `{u.get('ts_utc')}` status=`{u.get('status')}` policy=`{u.get('policy_ref')}`")
    lines.append("")
    lines.append("## Notes")
    lines.append(str(incident.get("notes", "")).strip() or "(none)")
    lines.append("")
    write_text(art_dir / "AI_INCIDENT_REPORT.md", "\n".join(lines) + "\n")

    snap_dir = art_dir / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    for u in updates:
        snap = {
            "update_id": u.get("update_id"),
            "ts_utc": u.get("ts_utc"),
            "status": u.get("status"),
            "policy_ref": u.get("policy_ref"),
            "prompt": u.get("prompt"),
            "output": u.get("output"),
        }
        write_text(snap_dir / f"{u.get('update_id')}.json", canonical_json(snap))

    files = []
    for p in pack_root.rglob("*"):
        if not p.is_file():
            continue
        rel = safe_relpath(p, pack_root)
        if rel == "manifest.json":
            continue
        files.append({"path": rel, "sha256": sha256_file(p)})

    manifest = {
        "pack_type": "AI_INCIDENT_EVIDENCE",
        "run_id": run_id,
        "source_incident_dir": str(incident_dir),
        "files": sorted(files, key=lambda x: x["path"]),
    }
    write_text(pack_root / "manifest.json", canonical_json(manifest))
    return pack_root
