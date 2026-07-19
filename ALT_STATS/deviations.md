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
