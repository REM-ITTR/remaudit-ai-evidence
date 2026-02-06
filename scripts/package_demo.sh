#!/usr/bin/env bash
set -euo pipefail

# ---- CONFIG (edit if you change run ids) ----
PACK="runs/REMAuditAI_INCIDENT_20260206T103939Z_ai_incident_sample"
UPDATES="runs/UPDATES_DIFF_REMAuditAI_INCIDENT_20260206T103939Z_ai_incident_sample"
MEMO="docs/REMAudit-AI_Incident_Evidence_Memorandum.pdf"

OUTDIR="dist"
mkdir -p "$OUTDIR"

if [ ! -d "$PACK" ]; then
  echo "ERROR: PACK folder not found: $PACK"
  exit 1
fi

if [ ! -d "$UPDATES" ]; then
  echo "ERROR: UPDATES folder not found: $UPDATES"
  exit 1
fi

if [ ! -f "$MEMO" ]; then
  echo "ERROR: MEMO PDF not found: $MEMO"
  echo "Tip: create docs/REMAudit-AI_Incident_Evidence_Memorandum.pdf then rerun."
  exit 1
fi

rm -rf "$OUTDIR"/*.zip "$OUTDIR"/README.txt

EVID_ZIP="$OUTDIR/REMAuditAI_EvidencePack.zip"
UPD_ZIP="$OUTDIR/REMAuditAI_UpdatesDiff.zip"
MEMO_ZIP="$OUTDIR/REMAuditAI_MemoPDF.zip"

(
  zip -qr "$EVID_ZIP" "$PACK"
  zip -qr "$UPD_ZIP" "$UPDATES"
  zip -qr "$MEMO_ZIP" "$MEMO"
)

cat > "$OUTDIR/README.txt" <<'TXT'
REMAudit-AI — Demo Deliverables
===============================

1) REMAuditAI_EvidencePack.zip
   - Frozen incident inputs (incident.json, updates.jsonl, policy files)
   - Canonical snapshots (artifact/snapshots)
   - Human-readable report (artifact/AI_INCIDENT_REPORT.md)
   - manifest.json (SHA-256 checksums)

2) REMAuditAI_UpdatesDiff.zip
   - Update-by-update diffs of snapshots
   - UPDATES_DIFF_SUMMARY.md + diffs/
   - manifest.json (SHA-256 checksums)

3) REMAuditAI_MemoPDF.zip
   - Incident Evidence Memorandum (human-facing)

Verification (No Trust Required)
-------------------------------
Unzip a deliverable and verify SHA-256 hashes in manifest.json.

Use:
  PYTHONPATH=src python3 -m remaudit_ai.cli verify --pack PATH_TO_UNZIPPED_FOLDER

TXT

echo "OK: wrote $EVID_ZIP"
echo "OK: wrote $UPD_ZIP"
echo "OK: wrote $MEMO_ZIP"
echo "OK: wrote $OUTDIR/README.txt"
