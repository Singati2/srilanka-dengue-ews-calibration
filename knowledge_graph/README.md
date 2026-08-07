# Knowledge Graph + Agent Graph — research integrity audit

Lightweight, **deterministic**, stdlib-only tooling that makes it hard for an incorrect,
unsupported, stale, contradictory, or unreproducible scientific claim to reach submission.
No LLM is used in any check (prompt §17); every finding is code-derived and evidence-linked.

## Run
```bash
python -m agent_graph.run_audit --repo .     # summary + audit/CURRENT_KG_AGENT_AUDIT.{md,json}
python tests/test_kg_agent.py                # deterministic tests
```
Exit code is non-zero when the repo is not submission-ready (usable as a CI gate).

## What it builds
- `knowledge_graph/schema.py` (+ generated `schema/*.yaml`): entities, relations, analysis-status ontology.
- `knowledge_graph/ingest.py`: deterministic ingestion of git, manuscript (numbers, citations,
  placeholders, sections), results/checksums, scripts (seeds, B, leakage flags), references → `graph/project_graph.json`.
- `agent_graph/agents.py`: 12 deterministic gate agents (Repository, Data Provenance, Temporal
  Leakage, Spatial, Statistical, Calibration, Reproducibility, Reference, Claim/traceability,
  Manuscript Consistency, Adversarial Reviewer, Submission Declarations).
- `agent_graph/run_audit.py`: release gates → `SUBMISSION READY: YES/NO`.

## Design rules
Prefer clear provenance, small deterministic tools, explicit failures, transparent nulls.
Data stays quarantined and git-ignored; only code + a safe audit report are produced.
