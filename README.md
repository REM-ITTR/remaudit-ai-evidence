## Demo (local)

Generate a fresh run and package the deliverables:

```bash
mkdir -p runs
PYTHONPATH=src python3 -m remaudit_ai.cli build \
  --incident-dir examples/ai_incident_sample \
  --out runs

PYTHONPATH=src python3 -m remaudit_ai.cli updates-diff \
  --pack "$(ls -1dt runs/REMAuditAI_INCIDENT_* | head -n 1)" \
  --out runs

./scripts/package_demo.sh
ls -lh dist
