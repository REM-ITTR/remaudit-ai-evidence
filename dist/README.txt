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

