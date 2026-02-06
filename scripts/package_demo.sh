#!/usr/bin/env bash
set -euo pipefail

OUTDIR="dist"
MEMO="docs/REMAudit-AI_Incident_Evidence_Memorandum.pdf"

mkdir -p "$OUTDIR"

# Pick newest by modified time (works even if timestamps differ lexicographically)
latest_dir () {
  local pattern="$1"
  ls -1dt $pattern 2>/dev/null | head -n 1
}

PACK="$(latest_dir "runs/REMAuditAI_INCIDENT_*")"
if [ -z "${PACK:-}" ]; then
  echo "ERROR: No evidence pack found under runs/REMAuditAI_INCIDENT_*"
  echo "Run:"
  echo "  PYTHONPATH=src python3 -m remaudit_ai.cli build --incident-dir examples/ai_incident_sample --out runs"
  exit 1
fi

# Prefer matching updates diff for same pack name; otherwise choose newest diff pack
BASENAME="$(basename "$PACK")"
UPDATES="runs/UPDATES_DIFF_${BASENAME}"
if [ ! -d "$UPDATES" ]; then
  UPDATES="$(latest_dir "runs/UPDATES_DIFF_REMAuditAI_INCIDENT_*")"
fi

if [ -z "${UPDATES:-}" ] || [ ! -d "$UPDATES" ]; then
  echo "ERROR: No updates-diff pack found under runs/UPDATES_DIFF_REMAuditAI_INCIDENT_*"
  echo "Run:"
  echo "  PYTHONPATH=src python3 -m remaudit_ai.cli updates-diff --pack \"$PACK\" --out runs"
  exit 1
fi

# Ensure memo exists
if [ ! -f "$MEMO" ]; then
  echo "MEMO PDF missing, generating via scripts/make_memo_pdf.sh..."
  ./scripts/make_memo_pdf.sh
fi

if [ ! -f "$MEMO" ]; then
  echo "ERROR: MEMO PDF not found: $MEMO"
  exit 1
fi

rm -f "$OUTDIR"/*.zip "$OUTDIR"/README.txt

EVID_ZIP="$OUTDIR/REMAuditAI_EvidencePack.zip"
UPD_ZIP="$OUTDIR/REMAuditAI_UpdatesDiff.zip"
MEMO_ZIP="$OUTDIR/REMAuditAI_MemoPDF.zip"

zip -qr "$EVID_ZIP" "$PACK"
zip -qr "$UPD_ZIP" "$UPDATES"
zip -qr "$MEMO_ZIP" "$MEMO"

cat > "$OUTDIR/README.txt" <<'TXT'
REMAudit-AI — Demo Deliverables
===============================

1) REMAuditAI_EvidencePack.zip
   - Frozen incident inputs
   - Canonical snapshots
   - Human-readable report
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

echo "OK: using PACK=$PACK"
echo "OK: using UPDATES=$UPDATES"
echo "OK: wrote $EVID_ZIP"
echo "OK: wrote $UPD_ZIP"
echo "OK: wrote $MEMO_ZIP"
echo "OK: wrote $OUTDIR/README.txt"
