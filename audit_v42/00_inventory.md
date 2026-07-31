# audit_v42 / 00 — Inventory (before editing)

**Date:** 2026-07-27 · **Prompt:** `claude_dengue_v42_to_v43_execution_prompt.md`

## Manuscript
- **Source (authoritative, LaTeX):** `/home/mpcrlab/Downloads/PHASE2_MANUSCRIPT_REVISION/revised_manuscript.tex` (NOT in the repo; lives in Downloads). This is the working v43 source, already carrying this session's revisions (90th-percentile matched ablation, honesty corrections, cut/dedup, em-dash removal).
- Compiled PDF: `revised_manuscript.pdf`, **33 pages**.
- The prompt's `/mnt/data/Dengue_Project (42).pdf` does **not** exist in this environment; the current `.tex` supersedes it.
- References: **46** `\bibitem`. Figures referenced: **8** (submission_figs holds 11 PDFs; 3 are unreferenced orphans: StudyArea, Fig1B_colombia_coverage, Fig3_forest — excluded from all bundles).
- **`[AUTHOR INPUT REQUIRED]` fields: 8** (unresolved; author-supplied only).

## Repository
- **Path:** `/home/mpcrlab/srilanka-dengue-ews-calibration`
- **Branch (working):** `manuscript-v43-repair` (created from `add-90th-matched-ablation`, commit `c32884c`)
- Pre-branch uncommitted state saved to `audit_v42/pre_edit_git_status.txt` (15 files, mostly untracked audit/analysis artifacts; nothing discarded).
- **Tags present (all four the manuscript cites):** `v6-analysis-frozen`, `alt-stats-plan-v1`, `alt-stats-results-v1`, `alt-stats-results-v2`.
- **License:** `LICENSE` present; GitHub license API reports **NOASSERTION** (not auto-detected as a standard SPDX license) — flagged as a submission blocker (§6.8 / license conflict noted by council seat 6).
- Environment lockfile: `analysis/environment/requirements-lock.txt` present.

## Code (key scripts)
- Matched-ablation freeze/reproduce: `ALT_STATS/src/freeze_matched_predictions.py`, `score_route_a.py`.
- Development-inclusive bootstraps: `analysis/geo_effect_decomposition/co_devincl_full_refit.py` (Colombia), `analysis/v18_bootstrap_b1000/sl_devinclusive_B1000.py` (Sri Lanka).
- 90th-percentile matched ablation (this session): `analysis/matched_ablation_90pct_v1/{colombia,srilanka}_matched_ablation_90pct_v1.py` (committed on branch `add-90th-matched-ablation`, `c32884c`).

## Frozen predictions / data
- Frozen matched pairs: `ALT_STATS/frozen/{srilanka,colombia}_matched_pairs.csv` (+ `FROZEN_INPUTS.sha256`).
- Raw/derived analysis data under `~/data_quarantine/` (read-only, chmod 444 + SHA256; **not committed**, per quarantine discipline).

## Archival DOI
- None assigned. `.zenodo.json` / `CITATION.cff` not yet created (§9.6). DOI = **TBD**.

## Status
Inventory complete. Manuscript source identified. Proceeding to §5.1 (Colombia climate-spec resolution).
