# Knowledge-Graph + Agent-Graph — Implementation Report

**Date:** 2026-08-06 · **Branch:** `agent/kg-agent-implementation` · **Prompt:** `prompts/CLAUDE_KNOWLEDGE_GRAPH_AGENT_GRAPH_DENGUE_PROJECT.md`

A lightweight, **deterministic, stdlib-only** research-integrity audit system. No LLM is used in any
check (prompt §17); every finding is code-derived and evidence-linked. The goal (final instruction)
is to make it hard for an incorrect, unsupported, stale, contradictory, or unreproducible claim to
reach submission — via clear provenance, small tools, and explicit failures.

## 1. Files created
```
knowledge_graph/__init__.py
knowledge_graph/schema.py                 # 47 entity types, 27 relations, 7-status ontology
knowledge_graph/schema/{entities,relations,constraints}.yaml   # generated from schema.py
knowledge_graph/ingest.py                 # git/manuscript/results/scripts/references -> graph
knowledge_graph/graph/project_graph.json  # 913 nodes / 592 edges (generated)
knowledge_graph/README.md
agent_graph/__init__.py
agent_graph/agents.py                     # 12 deterministic gate agents
agent_graph/run_audit.py                  # CLI: python -m agent_graph.run_audit --repo .
audit/CURRENT_KG_AGENT_AUDIT.{md,json}    # generated audit
tests/test_kg_agent.py                    # 7 deterministic tests
requirements-audit.txt                    # stdlib-only; networkx optional
.github/workflows/research-audit.yml      # CI: tests + audit artifact
```
## 2. Files modified
None outside the new tooling. **No manuscript, result, or frozen artifact was altered** (prompt
§0.3, §25). Data stays quarantined and git-ignored; only code + a safe report are produced.

## 3–4. Tests run / results
`python tests/test_kg_agent.py` → **7/7 PASS** (schema vocab; graph builds + manuscript found;
placeholder detection regression; submission blocks on placeholders; every analysis has a valid
status; all agents return valid status; audit is deterministic across runs).

## 5. Graph statistics
913 nodes, 592 edges. Node mix: 531 NumericClaim, 100 AuditFinding, 49 Script, 47 Reference,
45 ManuscriptSection, 42 DOI, 40 GitCommit, 22 Checksum, 8 Analysis (each with an explicit status),
+ Model/Comparator/Manuscript/GitTag.

## 6. Critical contradictions found
- **None outstanding in the current manuscript.** The KG's contradiction query specifically checks
  for the "development-inclusive proper-score intervals were not computed" statement co-occurring
  with computed DI results — that contradiction **was present in v42 and is now resolved** (the DI
  proper-score run was executed and the sentences retired), so the check passes.
- The Adversarial Reviewer finds **no non-negated overclaim terms**: every instance of
  "causal climate", "cases prevented", "national generalizability", etc. sits inside an explicit
  disclaimer — an honesty signal, not a violation.

## 7. Reproducibility blockers
- **122 absolute machine-specific paths** in tracked files (`/home/...`, `/Users/...`) — portability
  risk; mostly in the M6 geomatics notebooks and some scripts. *Fix:* parameterize via env var /
  `Path(__file__)`-relative roots.
- **Result traceability REVIEW:** 117/278 four-decimal effect values in the manuscript cannot be
  matched to a **committed** result file — expected, because raw result CSV/JSON are quarantined
  (git-ignored) by design. The committed `audit_v42/02_headline_results_matrix.csv` covers the
  headline set; the rest live only in quarantine. *Not a defect*, but it means an external reader
  cannot re-trace every number without the data — worth stating in the reproducibility note.

## 8. Manuscript blockers
- **MANUSCRIPT CONSISTENCY REVIEW:** the manuscript asserts a public GitHub repo/commit; this must
  be verified from a clean, unauthenticated environment before submission (do not trust the prose).
- Abstract within limit (299 words), 0 em-dashes — clean.

## 9. Unresolved author inputs (SUBMISSION DECLARATIONS = FAIL → SUBMISSION READY: NO)
- **9 unresolved placeholders**: 8 × `[AUTHOR INPUT REQUIRED: …]` (ethics, funding, competing
  interests, CRediT, ORCIDs, corresponding author, OpenDengue version ID, archival DOI) + 1
  `[DOI to verify]`. These are author-supplied and block submission; none can be fabricated.
- LICENSE is **MIT** (the earlier GitHub "NOASSERTION" was auto-detector formatting; the file text
  is a valid MIT license — not a blocker).

## 10. Exact next actions
1. Author completes the 8 declaration fields + verifies the archival DOI (only blocker to READY).
2. Verify the public GitHub repo/commit from a clean environment; keep the claim only if it resolves.
3. Parameterize the 122 absolute paths (portability); re-run `python -m agent_graph.run_audit`.
4. Add a one-line reproducibility note that raw results are quarantined, so full number-tracing
   requires the data package (headline values are in `audit_v42/02_headline_results_matrix.csv`).

---

# Harsh External-Reviewer Verdict

Scored 1–10, deliberately not inflated.

| Dimension | Score | Rationale |
|---|---|---|
| Scientific question | **8** | Sharp, well-motivated: does climate add calibrated decision value beyond a *matched* recent-surveillance model? The right question, rarely asked this way. |
| Novelty | **6** | Genuine but modest — first decision-curve net benefit + matched climate-block ablation for population-level dengue elevated-activity forecasting; the underlying null is not itself new (Johansson 2016, Benedum 2020). |
| Study design | **6** | Sound matched-comparator core, but the interpretable estimand is post-hoc and the Colombia arm is a selected, COVID-window subset. |
| Comparator fairness | **8** | Exemplary: an independently refit no-climate model sharing all non-climate structure — the correct way to isolate a climate block. |
| Calibration | **8** | CITL/slope/ICI + time-updated recalibration + intercept-shift sensitivity; well above field norm. |
| Decision-curve analysis | **8** | Correct Vickers formulation, threshold grid, and now the Vickers 2023 caveat that net-benefit CI-inference is contested (applied symmetrically). |
| Statistical inference | **7** | Conditional vs development-inclusive correctly separated; the DI proper-score run closed the prior conditional-only asymmetry. Post-hoc estimand + modest power keep it below 8. |
| Spatial validity | **5** | Modest cluster counts (26 RDHS / 31 depts), borderline residual autocorrelation; diagnostics honest but underpowered. |
| Generalizability | **4** | Explicitly limited — selected Colombia subset, two settings, not external validation; the paper says so. |
| Reproducibility | **6** | Strong scaffolding (tags, seeds, checksums, frozen artifacts, lockfile) but not bit-identical, 122 absolute paths, raw results quarantined. |
| Transparency | **9** | Outstanding — self-auditing, honest null, documents its own corrected interval and post-lock bug; no non-negated overclaims. |
| Manuscript consistency | **7** | Internally consistent after this session's fixes (asymmetry retired, em-dashes gone); the unverified public-repo claim is the open item. |
| Submission readiness | **3** | Blocked: 8 author-declaration placeholders + DOI unresolved. Science is close; paperwork is not. |

**Overall recommendation: MAJOR REVISION / NOT YET READY FOR SUBMISSION.** The scientific content is
defensible and unusually honest — a legitimate near-null with a real methods contribution — and would
plausibly reach *minor* revision on science alone. It is held out of submission by author-supplied
declarations and one availability claim to verify, not by a scientific defect. This matches the
independent 6-seat expert-council verdict.

**Interpretation target (§29) — supported by the evidence:** *In two retrospective settings, adding
climate to a structurally matched recent-surveillance model produced at most modest incremental
probability or decision value at short horizons, sensitive to calibration, comparator structure,
development-inclusive uncertainty, and setting-specific limitations.* The repository supports this
statement and does not support a stronger one.
