# REVISION_MANIFEST — v44 biomath reframe candidate

**Task:** mathematical-gap analysis of the true current Paper 1 (v44) + a separate applied-biomathematics / decision-theoretic candidate. Writing/formalization only. No analysis run.

## Canonical source (preserved, unchanged)
- Path: `manuscript_v44/revised_manuscript.tex`
- Branch / commit: `agent/v44-round4-geomatics-execution` / `4b3287ccf11538cf5e54ce3b81dd4c9fbd2fafb6`
- SHA256 **before and after** this work: `08fad12b9188b98faa7566d21769ac71fc3356248afeff91868cebfb07e46915` (identical ⇒ unmodified)
- Also preserved unchanged: `manuscript_v43/revised_manuscript.tex` (`60fa9b36…`), `manuscript/dengue_ews_manuscript.tex` (`a521e850…`)

## What was produced (all NEW, untracked; nothing staged/committed/pushed)

### `analysis/v44_biomath_gap_analysis/`
| File | Purpose |
|---|---|
| `SOURCE_MANUSCRIPT_RESOLUTION.md` | Canonical-source resolution (path/branch/SHA/why); M6/WP4/WP5 not integrated; lineage ambiguity |
| `V44_MATHEMATICAL_GAP_ANALYSIS.md` | 15 concepts classified (AE/INF/MU/MC/NS/DEF) + 15 gap questions; verdict: candidate justified as a thin layer |
| `BIOMATH_FRAMING_VALIDITY.md` | Is it applied biomathematics? Qualified yes (decision theory/math-epi); not mechanistic |
| `NOVELTY_CLAIM_AUDIT.md` | Unsafe vs defensible claims; keep one hedged "first"; frame math as "we make explicit" |

### `manuscript_v44_biomath_candidate/`
| File | Purpose |
|---|---|
| `revised_manuscript_biomath.tex` | Candidate = canonical v44 + formalization layer (framework subsection, notation table, four-level Intro, question-form Results headings, estimand/biological-relevance Discussion framing); figure-safe; portable preamble |
| `BIOMATH_NOTATION_TABLE.md` | Symbol → empirical-object map |
| `BIOMATH_SECTION_CROSSWALK.md` | Every change vs canonical (additive/framing only) |
| `BIOMATH_NUMERIC_CROSSWALK.md` | Every number → canonical location + status (all VERIFIED/SOURCE_ONLY; none NOT_TRACEABLE) |
| `BIOMATH_REFRAME_RATIONALE.md` | Why it qualifies; math + empirical contribution; limits |
| `BIOMATH_TITLE_ASSESSMENT.md` | Title families; PLOS vs applied-math recommendations |
| `BIOMATH_CLAIM_BOUNDARY.md` | Allowed vs not-yet-allowed claims; status tags |
| `BIOMATH_HARSH_REVIEW.md` | 4 internal review passes + verdict |
| `REVISION_MANIFEST.md` | This file |
| `build.sh` | Fail-fast two-PDF build |
| `revised_manuscript_biomath_internal_review.pdf` | Compiled, line-numbered, 28 pp |
| `revised_manuscript_biomath_grayscale.pdf` | Compiled, grayscale build, 28 pp |

## Faithfulness proof (see `BIOMATH_NUMERIC_CROSSWALK.md`)
- Candidate created by byte-for-byte copy of the canonical file, then additive edits only.
- `diff` of non-comment lines: only title, one extended abstract sentence, five headings, and eight `\includegraphics`→`\safeincludegraphics` swaps changed; **no numeric results line removed**.
- Result-grade numeric census: **241/241 numbers preserved** (the one flagged token was in a rewritten provenance *comment*).

## Firewall (M6 / WP4 / WP5)
No geomatics result imported. Spatial-exposure operator and the geomatics incremental estimand $\Delta V_G$ appear only as framework / PENDING. No M6 leakage figure, no WP4 spatial-CV performance, no WP5 population-weighted result.

## Build
`bash build.sh` (TinyTeX/full TeX). Preamble guards `threeparttable, microtype, placeins, setspace, fancyhdr, lineno` with `\IfFileExists` fallbacks so it compiles on minimal TeX and identically on Overleaf/full TeX. `submission_figs/*.pdf` are gitignored/absent; `\safeincludegraphics` renders a labeled placeholder — no figure was created or modified. Grayscale build currently equals the color build (no internal color marks; figures are external and links are black).

## What was NOT done (per task restrictions)
No model fit/refit; no metric/AUC/PR-AUC/Brier/NLL/calibration/decision-curve recomputed; no new CI/bootstrap; no outcome/threshold/horizon/split/hierarchy change; no primary/secondary status change; no mechanistic model; no new data; no M6/WP4/WP5 promotion; no preregistration invented; nothing staged, committed, pushed, tagged, merged, released, archived, uploaded, or submitted.

## Open (author-owned) submission blockers (from canonical Declarations)
Ethics determination; ORCIDs; funding; competing interests; CRediT confirmation; archival DOI (Zenodo) + code license; OpenDengue v1.3 Figshare version-record id. These are unchanged from the canonical manuscript and are not resolvable by this formalization task.

---

## Tightening pass (decision-theoretic revision) — 2026-08-09
Second formalization-only pass; goal = reduce ornament, sharpen the estimand, keep venue-appropriate. No science changed.

**Hashes.** Canonical sources unchanged (v44 `08fad12b…`, v43 `60fa9b36…`, top-level `a521e850…`). Candidate `revised_manuscript_biomath.tex`: `c6fd87b4…` (before this pass) → `86b91e2a…` (after).

**Key changes** (detail in `BIOMATH_SECTION_CROSSWALK.md`):
- Metric-oriented value functionals $V_k$ (larger=better; Brier/NLL negated); central estimand $\Delta V_{C,k}=V_k(\mathcal I^{SC})-V_k(\mathcal I^{S})$.
- Removed from main Methods → Discussion/SI: σ-algebra filtration (→ plain admissibility iff), spatial-exposure operator $\mathcal A_w$, geomatics estimand $\Delta V_G$, textbook Brier/NLL formulas.
- Title → decision-analytic default (no "nested information sets"); "biomathematics" absent from title/abstract.
- Discussion: three-way "biological relevance ≠ incremental predictive value ≠ incremental decision value" + pending-extensions note.
- Framework displayed equations 8 → 6 (Methods total ~7).
- Novelty sentence marked `NEEDS_EXTERNAL_VERIFICATION` (in-.tex comment + audit).

**New docs this pass:** `MATCHED_COMPARATOR_STRUCTURE.md`, `BIOMATH_HARSH_REVIEW_V2.md`, `V44_VS_BIOMATH_DECISION_MEMO.md`. Updated: `BIOMATH_NOTATION_TABLE.md`, `BIOMATH_SECTION_CROSSWALK.md`, `BIOMATH_NUMERIC_CROSSWALK.md`, `BIOMATH_TITLE_ASSESSMENT.md`, `NOVELTY_CLAIM_AUDIT.md`.

**Verification.** All 241 result-grade numbers preserved (only the header-comment token differs). Both PDFs recompiled (28 pp). Harsh-review V2 verdict: `ADOPT_HYBRID_LIGHT_FORMALIZATION`.
