# Project Overview

## Title
Calibration and decision-curve evaluation of climate-driven dengue early-warning models in Sri Lanka.

## Question
When two existing climate-driven dengue early-warning systems have comparable discrimination (AUC), do they lead to **different public-health alert decisions** under calibration and decision-curve / net-benefit analysis?

## Approach (existing models only — no new model)
1. **Mathematical model:** a published climate-forced dengue R0 / Ross–Macdonald / SEIR-SI model.
2. **Statistical model:** a published DLNM / INLA / Bayesian early-warning model.
3. **Contribution:** external validation, **calibration**, **recalibration**, **decision-curve / net-benefit** evaluation of outbreak alerts, and spatial decision-support. Methodological novelty is explicitly **not** claimed; prior work (e.g., Tozan 2023 net-benefit/cost-loss for VBD EWS) is cited — see `osf_prereg_skeleton.md`.

## Pilot
Sri Lanka. Outcome unit: **26 RDHS divisions**, **epidemiological week**, 2018–2025.

## Status at repository creation
- Outcome dataset built, QC-validated, and **frozen** locally (held outside git).
- Manual QC: 33 sampled issues, **0 mismatches**; current-week field clean (0 invalid values).
- OpenDengue evaluated → **quarantined negative** (no Sri Lanka district/RDHS-weekly data).
- Next phase: **Geomatics WP1** (RDHS boundary crosswalk + population denominators).

## Pipeline (scripts/)
- `wer_bulk_harvest.py` → harvest + download + manifest (checksums).
- `wer_bulk_extract_dengue_v2.py` → Table-1 RDHS × dengue current-week extraction (hardened).
- `wer_qc_report_v2.py` → structural + current-week + cumulative QC.

## Document map
- `study_decision_log.md` — **running log of new directions, approaches & decisions** (start here for "what's new / what did we decide").
- `maup_sensitivity_and_spatial_cv_plan.md` — scope-locked plan for WP5 (MAUP / 3 exposure builds) + WP4 (two-country spatial CV). Source of truth.
- `wp4_wp5_implementation_plan.html` — browser-friendly rendering of that plan (open locally; Markdown wins if they disagree).
- `data_access_plan.md` — data sourcing, eligibility, decision rules, freeze rules.
- `geomatics_scope_of_work.md` — geospatial work-stream (exposure, adjacency, decision-flip mapping).
- `dengue_geospatial_risk_factors_review.html` — literature review of geomatics dengue risk factors (59 sources).
- `osf_prereg_skeleton.md` — preregistration skeleton + verified prior-work positioning.
- `probast_tripod_scoring_instrument.md` — risk-of-bias / reporting QC instrument.

## Forbidden-file guard (run before EVERY commit)
```bash
git add -A
git status --porcelain | awk '{print $2}' > /tmp/staged.txt
# must return NOTHING:
grep -E '\.(pdf|zip|tar|gz|xz|h5|nc|tif|tiff)$|frozen.*\.csv$|data_quarantine/|raw_bulk/|email|credential|secret' /tmp/staged.txt \
  && echo "FORBIDDEN FILE STAGED — ABORT" || echo "guard passed"
```
Only commit when the guard prints `guard passed`.

## Hard rules
- Never commit raw PDFs, the frozen CSV, climate rasters, credentials, or private correspondence.
- `dengue_cumulative` is QC-only, never an analysis field.
- No outcome↔exposure linkage or modeling until WP1 + final preregistration are complete.
