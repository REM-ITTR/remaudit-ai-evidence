#!/usr/bin/env bash
set -euo pipefail

MD="docs/REMAudit-AI_Incident_Evidence_Memorandum.md"
PDF="docs/REMAudit-AI_Incident_Evidence_Memorandum.pdf"

if [ ! -f "$MD" ]; then
  echo "Missing: $MD"
  exit 1
fi

rm -f "$PDF"

pandoc "$MD" -o "$PDF" --pdf-engine=weasyprint

echo "OK: wrote $PDF ($(wc -c < "$PDF") bytes)"
