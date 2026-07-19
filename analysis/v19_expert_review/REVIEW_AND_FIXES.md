# Expert-team review + applied fixes (v18 trimmed -> v18 reviewed)

Three specialists reviewed `paper1_plos_gph_v18_trimmed.tex` independently. Findings triaged against the source files; only verified, editable fixes applied. Manuscript science (B=1000 symmetric-null) unchanged; 0 distinct numbers lost.

## Panel 1 — epidemiology + biostatistics + decision-curve methodology
Verdict: **scientifically valid, no fatal/major analytic error, if anything over-caveated.** Positives: NB formula/threshold-grid correct; conditional-vs-development-inclusive bootstrap distinction is the sound backbone; few-cluster handling appropriate; framing defensible.

## Panel 2 — independent figure/table/chart auditor
Verdict: **no material discrepancy.** All authoritative Sri Lanka table/figure values reconcile exactly with the v12/v15/v17/v18 result files; Colombia values internally consistent across tab:colombia/tab:matcheddecomp/Fig 2/text. Only three benign roundings (Colombia M5-M1 0.0187 vs +0.0188; M5nc-M1 0.0109 vs +0.0110; ΔAUC 0.041 vs +0.040) — full-precision-vs-cell arithmetic, noted in text, no sign/zero-crossing change. **No numeric fix required.**

## Panel 3 — harsh PLOS peer reviewer
Verdict: **REJECT-AND-RESUBMIT.** Top concerns: (1) reproducibility/provenance blockers; (2) insufficient novelty (honest null); (3) equity/local-authorship on a two-LMIC study; (4) post-hoc estimand principal while prespecified null (partially resolved); (5) positive signal dissolves under development-inclusive inference (disclosed). DCA apparatus correct; interpretation restrained.

## Fixes APPLIED (verified true-in-body, editable)
1. **Abstract Colombia estimand** now named "a selected common-complete, higher-incidence municipality-week subset" (was "municipality-week") — matches the body's disclosure (both reviewers).
2. **Abstract tautology caveat** added: recent case counts already embed climate's short-horizon influence, so the small increment reflects redundancy with surveillance rather than climate being uninformative (epi panel).
3. **p*=0.30 reconciliation** (Discussion): the named anticipatory actions are low-cost, so a lower threshold may better match them, where the increment is near zero and alert-all competitive (Fig 4); the reference value should be revisited against a documented response-cost model (DCA panel).
4. **Development-inclusive interval elevated to primary** in the Sri Lanka matched table caption; conditional labeled an optimistic bound (biostat panel + harsh reviewer logic).

Build: 38 pp, exit 0, 0 undefined, 0 errors; abstract 449 words (<=500); 0 distinct numbers changed.

## Deliberately NOT applied (not editable / author-action / needs new analysis)
- Reproducibility DOI, pinned Python environment, ethics determination, the 18 SI files (only "planned"), OpenDengue v1.3 acquisition record — author-action; cannot be fabricated.
- Equity/local-authorship and "novelty" — PI/authorship decisions, not text fixes.
- Rolling-origin validation for the Sri Lanka primary and flexible calibration curves for the frozen models — require new analysis; already disclosed as limitations.
