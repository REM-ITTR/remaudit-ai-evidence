from __future__ import annotations

import argparse
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from .evidence_pack import build_ai_evidence_pack
from .incident_updates_diff import build_updates_diff
from .utils import read_text

def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def cmd_build(args: argparse.Namespace) -> None:
    incident_dir = Path(args.incident_dir)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    pack = build_ai_evidence_pack(incident_dir=incident_dir, out_dir=out_dir, run_id=_run_id())
    print(f"OK: wrote evidence pack -> {pack}")

def cmd_updates_diff(args: argparse.Namespace) -> None:
    pack_root = Path(args.pack)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not pack_root.exists():
        raise SystemExit(f"Pack not found: {pack_root}")
    diff_root = build_updates_diff(pack_root=pack_root, out_dir=out_dir)
    print(f"OK: wrote updates diff -> {diff_root}")

def cmd_verify(args: argparse.Namespace) -> None:
    pack_root = Path(args.pack)
    mpath = pack_root / "manifest.json"
    if not mpath.exists():
        raise SystemExit(f"manifest.json not found: {mpath}")

    m = json.loads(read_text(mpath))
    ok = True

    def sha256(p: Path) -> str:
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(1024*1024), b""):
                h.update(chunk)
        return h.hexdigest()

    for item in m.get("files", []):
        p = pack_root / item["path"]
        got = sha256(p)
        exp = item["sha256"]
        if got != exp:
            ok = False
            print("FAIL", item["path"])
        else:
            print("OK  ", item["path"])

    print("\nRESULT:", "PASS ✅" if ok else "FAIL ❌")

def main() -> None:
    ap = argparse.ArgumentParser(prog="remaudit-ai")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Build AI incident evidence pack from a local incident folder")
    p_build.add_argument("--incident-dir", required=True)
    p_build.add_argument("--out", required=True)
    p_build.set_defaults(fn=cmd_build)

    p_ud = sub.add_parser("updates-diff", help="Generate update-by-update diffs from a built pack")
    p_ud.add_argument("--pack", required=True)
    p_ud.add_argument("--out", required=True)
    p_ud.set_defaults(fn=cmd_updates_diff)

    p_v = sub.add_parser("verify", help="Verify a pack's SHA-256 manifest")
    p_v.add_argument("--pack", required=True)
    p_v.set_defaults(fn=cmd_verify)

    args = ap.parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()
