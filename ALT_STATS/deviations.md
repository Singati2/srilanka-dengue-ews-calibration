# deviations.md — append-only after the lock

## D1 — Matched no-climate predictions regenerated, not read from a stored V6 file
- date: 2026-07-15 · author: Phase 2 analyst (Claude) · affected spec: Section 0.1 frozen inputs
- reason: V6 never stored the matched no-climate per-observation probabilities as a file; the
  matched pair is defined by committed, deterministic, reproduce-gated V6 code. Regenerated
  via the verbatim frozen pipelines and frozen into ALT_STATS/frozen/ with checksums.
- results viewed when decided: NO (decided during input-freezing, before any score computed).
- expected impact: none on validity — regenerated Colombia M5_recal matches the committed
  frozen file to 1.11e-16; SL M1/M4/M5 reproduce to <1e-6. Provenance caveat only.
- approval: recorded in PHASE1_GATE.md gate decision. · commit: (lock commit below)

## D2 — Development-inclusive proper-score intervals not computed
- date: 2026-07-15 · affected spec: Section 4 · reason: refit-both-models bootstrap not
  re-executed this session (Phase 1 gate NOT_REPRODUCED for the refit pipelines). Per the
  gate rule, conditional intervals only. · results viewed: NO · impact: DI intervals absent
  by design; stated in all reports. · approval: PHASE1_GATE.md.

## D4 — Final conditional intervals moved to B=10,000 (revised plan)
- date: 2026-07-19 · author: Phase 2 analyst (Claude) · affected spec: revised plan
  CLAUDE_CODE_PHASE2_ALT_STATS_REVISED.md Section 7.2 (final interval B=10,000, seed 20260719;
  B=1000 seed-20260612 parity retained).
- change: the committed conditional proper-score intervals used B=5000 (seed 20260612); the
  revised plan sets the FINAL reported interval to B=10,000 (seed 20260719).
- results had been viewed: yes (B=5000 already reported); this is a Monte-Carlo refinement, not a
  metric or estimand change. Point estimates are identical (verified as a gate); interval endpoints
  moved only in the last reported digit and every conclusion is unchanged (all NLL/Brier intervals
  still exclude zero). Generator: src/score_route_a_b10000.py; output: results/route_a_B10000.csv.
- scope: applies to the PRIMARY dNLL and key-secondary dBrier. Secondary discrimination bootstrap
  (dAUC, dPR-AUC) at B=10,000 was computationally impractical in this environment; those secondary
  intervals are retained from the committed B=5000 conditional run (immaterial refinement).
