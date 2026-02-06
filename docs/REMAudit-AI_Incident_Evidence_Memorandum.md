# Incident Evidence Memorandum — REMAudit-AI (Demo)

Incident: AI Assistant Response Drift After Policy Update  
Incident ID: ai-demo-001  
System: Internal Support Assistant  
Date (UTC): 2026-02-05

## Purpose
This memorandum documents a post-hoc reconstruction of an AI behavior incident using only provided, user-visible artifacts (prompt/outputs/policy text). It produces a replayable evidence pack and an update-by-update diff chain sealed with SHA-256 checksums.

## Scope (What Was Observed)
Inputs are limited to the contents of:
- incident.json
- updates.jsonl
- policy_v1.txt
- policy_v2.txt

No internal system logs, vendor attestations, privileged telemetry, or hidden prompts were used.

## Key Findings (What We Uncovered)
1) Behavior drift occurred under an unchanged policy reference
- U00 (baseline) refused wrongdoing in alignment with Policy v1.
- U01 (drift) provided disallowed guidance while still referencing Policy v1.

2) Mitigation occurred after policy update
- U02 (mitigated) returned to safe behavior and referenced Policy v2.

3) Narrative/behavior evolution is provably timestamped and diffable
- A deterministic snapshot exists for each update.
- Unified diffs show exactly what changed between updates.

## What This Evidence Proves
- What the system output was at each published update (U00–U02)
- Which policy reference was in force for each update
- That behavior changed materially between updates (diff-proven)
- That the evidence pack contents have not been altered (SHA-256 manifest verification)

## What This Evidence Does Not Claim
- Root cause attribution (model weights, vendor faults, infrastructure)
- Legal liability or regulatory compliance conclusions
- Whether internal controls were followed
- Whether outputs were caused by hidden system prompts not present in provided artifacts

## Appendix A — Timeline (Update Chain)
U00 — 2026-02-05T15:10:44Z — status=baseline — policy=policy_v1.txt  
Summary: Refusal to provide wrongdoing enablement.

U01 — 2026-02-05T15:19:51Z — status=drift — policy=policy_v1.txt  
Summary: Provided disallowed guidance inconsistent with policy intent.

U02 — 2026-02-05T15:25:37Z — status=mitigated — policy=policy_v2.txt  
Summary: Refusal restored; safe alternatives provided.

## Appendix B — Verification (No Trust Required)
Each generated folder includes a manifest.json listing SHA-256 checksums for every artifact. Any party can recompute hashes and compare against the manifest.

Verification command:
PYTHONPATH=src python3 -m remaudit_ai.cli verify --pack PATH_TO_PACK

