# Specification — Canonical R `dlnm` Install & Run (design-lock)
*Plan to install **real R `dlnm`** (Gasparrini) and run the canonical DLNM climate comparator on the identical committed evaluation rows. **No install performed; no models run; no data modified.** Documentation only. The earlier apt attempt failed on the sudo password (passwordless root not available) — so the install must be run by the user. The Python cross-basis result stands as the documented fallback until R `dlnm` actually loads.*

**Date:** 2026-06-14 · **Status:** specification only.

## 0. Verified environment facts (read-only this session)
- **OS:** Ubuntu 22.04.5 LTS (jammy). **Network:** CRAN (cloud.r-project.org:443) reachable.
- **apt R:** `r-base` / `r-base-core` candidate **4.1.2-1ubuntu2** (universe); `r-cran-mgcv` **1.8-39**; **`r-cran-dlnm` NOT in apt**.
- **Current CRAN `dlnm`:** **2.4.10** (2025-04-17), **Depends: R (≥ 4.4)**, Imports: stats/graphics/grDevices/utils/splines/nlme/mgcv/tsModel → **will not install on R 4.1.2**.
- **Archived `dlnm` (R-4.1-compatible):** e.g. `dlnm_2.4.7.tar.gz` (2021-10-07) and nearby — predate the R≥4.4 requirement; pure-R (no compilation).
- **R/Rscript:** not installed. **sudo:** requires a password Claude does not have → **user must run the sudo steps**.

## 1. Install route decision
- **Route A — PREFERRED:** add CRAN's jammy-cran40 repo → install **current R (≥ 4.4, currently 4.5.x)** → `install.packages("dlnm")` = **dlnm 2.4.10** (truly current canonical). Best for reviewers (matches the live package).
- **Route B — FALLBACK:** apt **R 4.1.2** + `r-cran-mgcv` → install **archived dlnm 2.4.7** (R-4.1-compatible) from source into a user library. Genuinely canonical `dlnm` (same `crossbasis()`/`crosspred()` API), just an older pinned version; document it.

Decision rule: **attempt Route A first**; if the CRAN-repo setup is undesired or fails, use Route B. Either way, **do not claim "canonical R dlnm" until `library(dlnm)` loads and `packageVersion("dlnm")` is recorded.**

## 2. Exact commands
### Route A (preferred) — user runs the `sudo` lines (e.g., `! sudo …`)
```bash
sudo apt-get install -y --no-install-recommends software-properties-common dirmngr wget
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc \
  | sudo tee /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc >/dev/null
sudo add-apt-repository -y "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/"
sudo apt-get update
sudo apt-get install -y r-base r-base-dev
# then (NO sudo needed; Claude can run):
Rscript -e 'install.packages(c("tsModel","dlnm"), repos="https://cloud.r-project.org")'
Rscript -e 'library(dlnm); cat("R", as.character(getRversion()), "| dlnm", as.character(packageVersion("dlnm")), "\n")'
```
- **sudo needed:** yes (repo add + R install). **Expected R:** ≥ 4.4 (≈ 4.5.x). **Expected dlnm:** 2.4.10. **mgcv:** current from CRAN.

### Route B (fallback) — user runs the `sudo` line
```bash
sudo apt-get install -y r-base-core r-cran-mgcv          # R 4.1.2 + mgcv 1.8-39
# then (NO sudo; Claude can run; user library):
mkdir -p ~/Rlibs
Rscript -e '.libPaths("~/Rlibs"); install.packages("tsModel", repos="https://cloud.r-project.org")'
Rscript -e '.libPaths("~/Rlibs"); install.packages("https://cran.r-project.org/src/contrib/Archive/dlnm/dlnm_2.4.7.tar.gz", repos=NULL, type="source")'
Rscript -e '.libPaths("~/Rlibs"); library(dlnm); cat("R", as.character(getRversion()), "| dlnm", as.character(packageVersion("dlnm")), "\n")'
```
- **sudo needed:** yes (apt R only). **Expected R:** 4.1.2. **Expected dlnm:** 2.4.7 (pinned; if a newer archived version still supports R<4.4, may use it — record whichever loads). **dlnm is pure R** → no `r-base-dev`/compiler required for Route B.

## 3. Per-route comparison
| | Route A (preferred) | Route B (fallback) |
|---|---|---|
| sudo | yes (repo+R) | yes (R only) |
| Expected R | ≥4.4 (≈4.5.x) | 4.1.2 |
| Expected dlnm | **2.4.10 (current)** | 2.4.7 (2021, archived) |
| Reproducibility | matches live CRAN; record sessionInfo | fully reproducible if version pinned; record sessionInfo |
| Risks | bigger system change; repo-key/add-apt-repository can be fiddly | older dlnm; must confirm 2.4.7 builds & loads on R 4.1.2 (expected fine, pure-R) |
| Reviewer optics | best ("current canonical dlnm") | acceptable ("canonical dlnm, version pinned") |

## 4. Run spec (after a route succeeds and `dlnm` loads)
- **Record:** `sessionInfo()`, R version, exact `dlnm`/`mgcv`/`tsModel` versions → into the output meta and the report (no canonical claim without this).
- **Input files (read-only):** v2 date-aligned table `…dengue_climate_population_linked_2018_2025_v2_date_aligned.csv` (sha256 `3a197d61…`); committed primary predictions `…/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv` (sha256 `07f5916a…`) for M1/M2/M3; Python-DLNM predictions `…/dlnm_comparator_v1/dlnm_comparator_predictions_v1.csv`; hybrid `…/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv` for M5.
- **Identical-row requirement (stop-gate):** export the exact train/test design (geometry_id, week_start, split, y, the lagged climate matrices `t2m_mean_c__L0..L8`, `precip_sum_mm__L0..L8`, `rh_mean_percent__L0..L8`) from the committed pipeline to a quarantined CSV; R reads **that**. The R test predictions must align 1:1 (same 3,926 rows, same labels) to the committed M1/M2/M3/Python-DLNM rows; **stop if mismatch.**
- **Canonical model (`dlnm::crossbasis`):** for each climate variable, `cb <- crossbasis(Q, lag=c(0,8), argvar=list(fun="ns", df=3), arglag=list(fun="ns", df=3))` where `Q` = the n×9 matrix of that variable's lags 0–8; value-spline knots from **train only**. Fit `glm(y ~ cb_temp + cb_precip + cb_rh, family=binomial)` on **train**; predict on **test**. (This is canonical frequentist DLNM — the same cross-basis construction as Gasparrini's tutorials; mgcv penalized `gam` is an optional sensitivity, reported separately.)
- **Comparison set on identical rows:** R-DLNM-climate vs **M1** (recent-cases AR), **M2**, **M3**, **Python-DLNM** (approximation), and **M5** (hybrid) for context.
- **Metrics (test):** AUC, PR-AUC, Brier, calibration-in-the-large, calibration slope, NB@p\*=0.30, threshold-band NB (0.20–0.40); **ΔAUC and ΔNB vs M1**, and **R-DLNM vs Python-DLNM agreement** (max|Δ prob|, ΔAUC).
- **RDHS-cluster bootstrap** (seed 20260612, B=1000) for ΔAUC/ΔNB(R-DLNM − M1) and (R-DLNM − Python-DLNM).

## 5. Strict interpretation rules (pre-committed)
- **Primary purpose:** establish the *canonical* climate comparator and check it agrees with the Python approximation — **not** to find a win.
- If **R-DLNM ≈ Python-DLNM** (small ΔAUC, CI on ΔNB includes 0): the Python approximation is validated; the "not canonical dlnm" objection is removed; prior conclusions stand.
- If **R-DLNM materially differs** from Python: report the difference honestly; the canonical R result supersedes the approximation for the manuscript.
- **R-DLNM still vs M1:** expected to remain below M1 operationally (per Beal 2025 / Sesay 2026); report as-is. **No model-winning claim** unless ΔNB(R-DLNM − M1) CI excludes 0 positively and is band-robust.
- Record dlnm/R versions; **"canonical R dlnm" stated only after `library(dlnm)` loads successfully.**

## 6. Outputs & governance
- Quarantined only: `~/data_quarantine/model_pilots/dlnm_R_canonical_v1/` → `dlnm_R_metrics_v1.csv`, `dlnm_R_dca_v1.csv`, `dlnm_R_predictions_v1.csv`, `dlnm_R_ci_v1.csv`, `dlnm_R_sessioninfo.txt`, `dlnm_R_canonical.meta.md`, `_run_dlnm_R.R`, `_export_design_for_R.py`. Read-only + SHA256.
- Safe repo report later: `docs/canonical_R_dlnm_report.md`. **No data files committed.** No prior outputs overwritten (new directory). Frozen tables untouched.

## 7. Confirmation
- **No install performed; no analysis run; no data modified.** Only this markdown spec was created. Nothing committed.
- The earlier apt attempt installed **nothing** (failed on sudo password). Rscript remains absent.

## Next step (gated)
1. **You** run the Route A (or B) `sudo` lines via `! …`. 2. Claude installs `dlnm` (user lib, no sudo), confirms it loads, records versions. 3. Claude exports the identical-row design, runs `_run_dlnm_R.R`, writes quarantined outputs + safe report. Nothing runs until R `dlnm` loads and you approve the run.
