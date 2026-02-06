from __future__ import annotations

import json
import difflib
from pathlib import Path

from .utils import write_text, read_text, sha256_file, canonical_json, safe_relpath

def _unified_diff(a: str, b: str, fromfile: str, tofile: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            a.splitlines(),
            b.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        )
    ) + "\n"

def build_updates_diff(pack_root: Path, out_dir: Path) -> Path:
    snap_dir = pack_root / "artifact" / "snapshots"
    if not snap_dir.exists():
        raise FileNotFoundError(f"Missing snapshots folder: {snap_dir}")

    snaps = sorted([p for p in snap_dir.glob("*.json") if p.is_file()])
    if not snaps:
        raise FileNotFoundError("No snapshot json files found.")

    diff_root = out_dir / f"UPDATES_DIFF_{pack_root.name}"
    diffs_dir = diff_root / "diffs"
    diffs_dir.mkdir(parents=True, exist_ok=True)

    diffs_written = 0
    chain = []
    for i, p in enumerate(snaps):
        obj = json.loads(read_text(p))
        chain.append((obj.get("update_id"), obj.get("ts_utc"), obj.get("status"), obj.get("policy_ref")))

        if i == 0:
            continue
        a = read_text(snaps[i-1])
        b = read_text(snaps[i])
        if a == b:
            continue
        dp = diffs_dir / f"diff_{i-1:02d}_to_{i:02d}.diff.txt"
        write_text(dp, _unified_diff(a, b, snaps[i-1].name, snaps[i].name))
        diffs_written += 1

    summary = []
    summary.append("# REMAudit-AI — Update-by-Update Diff (Single Incident)")
    summary.append("")
    summary.append(f"Pack: `{pack_root}`")
    summary.append("")
    summary.append(f"Total snapshots: **{len(snaps)}**")
    summary.append(f"Diffs written: **{diffs_written}**")
    summary.append("")
    summary.append("## Update Chain")
    for (uid, ts, st, pol) in chain:
        summary.append(f"- {uid} `{ts}` status=`{st}` policy=`{pol}`")
    summary.append("")
    summary.append("## How to Read")
    summary.append("- `diffs/` contains unified diffs between consecutive snapshots.")
    summary.append("- This proves whether the AI behavior/policy context changed over time.")
    summary.append("")
    write_text(diff_root / "UPDATES_DIFF_SUMMARY.md", "\n".join(summary))

    files = []
    for p in diff_root.rglob("*"):
        if not p.is_file():
            continue
        rel = safe_relpath(p, diff_root)
        if rel == "manifest.json":
            continue
        files.append({"path": rel, "sha256": sha256_file(p)})

    manifest = {
        "diff_type": "AI_UPDATE_CHAIN_DIFF",
        "source_pack": str(pack_root),
        "diffs_written": diffs_written,
        "files": sorted(files, key=lambda x: x["path"]),
    }
    write_text(diff_root / "manifest.json", canonical_json(manifest))
    return diff_root
