# Feasibility Memo — OpenDengue External-Replication Arm (scoping only)
*Assess whether a small OpenDengue external **replication** arm is feasible to strengthen the Sri Lanka paper. **Feasibility/scoping only — no data downloaded, no models built, no external metrics computed, no labels, no climate linkage, no data modified.** Per-country specifics flagged "verify in catalog" are not yet confirmed and must be checked before any run. No external-validation claim is made.*

**Date:** 2026-06-14 · **Status:** feasibility memo only.

## 1. Purpose
Determine whether a **small, clean external replication** of the *decision-evaluation framework* (not Sri Lanka coefficients) is feasible using **OpenDengue** — to convert a single-country pilot into a transportability check and address the field's most-cited gap (external validation uncommon: Leung 2023; Hussain-Alkhateeb 2021).

## 2. External-validation target (replication, not transfer)
**Not** transfer of Sri Lanka model coefficients. Instead, **re-fit and re-evaluate the same framework locally in each external setting:**
- recent-cases AR baseline (M1-analog),
- climate-only model (DLNM/logistic),
- hybrid surveillance + climate (M5-analog),
- calibration + recalibration,
- decision-curve **net benefit**,
- **ΔNB of adding climate beyond the surveillance baseline**.
Question: *does the pattern replicate* — "recent cases hard to beat operationally; calibration drift correctable; targeted climate value at most regime/threshold-dependent"?

## 3. Verified OpenDengue facts (anchor)
- OpenDengue (Clarke et al., *Scientific Data* 2024, DOI 10.1038/s41597-024-03120-7): **56M+ cases, 102 countries, 1924–2023**; **>95% weekly or monthly**; **subnational for 40 countries**; v1.3 (2025) through 2023. Public, standardized. **No Sri Lanka subnational** (why we built from WER).
- Climate inputs (ERA5-Land/CHIRPS) are **global** → climate linkage is technically possible for any country **with admin boundaries** (COD-AB/GADM) — a per-country effort, not free.

## 4. Candidate-setting criteria
A usable external setting needs: (a) ≥ ~5 years of dengue counts; (b) **weekly** preferred (monthly only if scoped); (c) **subnational** units if possible; (d) **stable unit definitions** over the window; (e) enough events for a 75th-pct outbreak label and ≥ ~10 spatial clusters for cluster bootstrap; (f) a fair temporal train/test split; (g) feasible ERA5/CHIRPS linkage (boundaries available); (h) no gross reporting discontinuity (e.g., COVID-era gaps) that makes validation unfair.

## 5. Minimum feasibility table
*Surveillance characteristics below are reasoned from **verified** forecasting/EWS papers (Schlesinger 2024 Colombia; Colón-González 2021 Vietnam; Wu 2025 PNAS multi-country); exact OpenDengue temporal/spatial coverage and unit counts per country are **"verify in catalog"** before any run.*

| Country/region | Temporal res. | Spatial res. | Years (approx) | Units (approx) | ~Obs | Event/label feasibility | Climate-linkage feasibility | Likely design | Keep/Drop | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| **Brazil** | weekly (verify) | municipal/state | long, multi-decade | 27 states / many munis | very large | high (large counts) | high (GADM boundaries) | temporal split, state-level | **KEEP (primary candidate)** | Best-documented weekly subnational; used in Wu 2025, Sebastianelli 2024 |
| **Colombia** | weekly (verify) | municipal | 2007–2023 (verify) | dozens of municipalities | large | high | high (COD-AB exists) | temporal split, municipal | **KEEP (primary candidate)** | EWARS-csd weekly municipal precedent (Schlesinger 2024) |
| **Vietnam** | weekly/monthly (verify) | province | 2002–2020+ (verify) | ~63 provinces | large | high | high | temporal split, province | **KEEP (secondary)** | Province weekly 2002–2020 (Colón-González 2021) |
| **Mexico** | weekly (verify) | state/district | multi-year | 32 states | large | high | high | temporal split, state | KEEP (secondary) | EWARS operational (Mexico) precedent |
| **Thailand / Malaysia** | weekly/monthly (verify) | province/state | multi-year | provinces/states | moderate–large | moderate–high | high | temporal split | Conditional | Used in Wu 2025; confirm subnational+weekly in OpenDengue |
| **Peru / Puerto Rico** | weekly (verify) | region/island | multi-year | few–dozens | small–moderate | moderate (cluster count low) | high | temporal split | Conditional/Drop | Few spatial clusters → cluster-bootstrap power risk |
| Most other OpenDengue countries | often national/monthly | national | varies | 1 | small | low (no subnational/weekly) | n/a | — | **DROP** | Not subnational/weekly → fails criteria |

## 6. Recommended external arm
- **If catalog confirms clean weekly subnational data:** a **one-country replication (Brazil OR Colombia)** is the right first move — both have the strongest documented weekly subnational surveillance and existing climate-EWS precedent.
- **Two-country only if both are clean and easy** (Brazil + Colombia). 
- **No external arm** if catalog inspection shows only annual/national/unstable units for the candidates (do not force it).
- Do **not** attempt many countries — scope creep; one clean replication answers the transportability question.

## 7. Analysis design (if feasible) — pre-specified
- **Label:** local RDHS-analog **75th-percentile** outbreak threshold, **train-period only** (same rule as Sri Lanka).
- **Horizon:** **h=4 weeks** if weekly; nearest compatible (e.g., 1 month) if monthly — scoped explicitly.
- **Split:** temporal train/test within the country's coverage (e.g., earlier years train, later years test).
- **Models:** recent-cases AR baseline; climate-only (canonical R `dlnm` if installed, else documented approximation); hybrid surveillance+climate.
- **Metrics:** AUC, PR-AUC, Brier, calibration-in-the-large, slope, recalibration; **net benefit / decision curve**; **ΔNB(hybrid − surveillance)** with **bootstrap clustered by spatial unit** (seed 20260612).
- **Outputs quarantined; safe markdown report only.** Same governance as all prior steps.

## 8. Stop rules
Stop (and report "not feasible") if, for every candidate: only **annual** data; **inconsistent/unstable spatial units**; **< 3 usable years**; **too few events** for a 75th-pct label or **< ~10 spatial clusters**; **ambiguous climate linkage** (no usable boundaries); or **no fair train/test split** (e.g., dominant COVID-era discontinuity).

## 9. Interpretation rules
- **Allowed:** "external **replication** of the evaluation framework"; "pattern **replicated / not replicated** in country X."
- **Forbidden:** "Sri Lanka model globally validated"; "global external validation"; "deployment-ready"; any claim of transferring SL coefficients.

## 10. Recommendation
- **External validation is STRONGLY RECOMMENDED** (the single highest-leverage upgrade — turns the pilot into a transportability study, directly addressing the field's #1 gap) — **but NOT strictly required before first submission.** The paper is publishable single-country as a methods/decision-evaluation/data-resource study, with the external arm as the headline strengthener or a fast-follow.
- **Feasibility now:** *likely yes for 1 clean country (Brazil or Colombia)*, **pending catalog verification** of weekly subnational coverage and a clean train/test window — plus the real (non-trivial) effort of per-country boundary sourcing and ERA5/CHIRPS linkage.
- **Suggested sequence:** (1) catalog-inspection only (confirm Brazil/Colombia weekly subnational, years, units, COVID gaps) → (2) if clean, gated single-country replication run → (3) safe markdown report. Each step approval-gated.

## 11. Confirmation
- **No OpenDengue data downloaded; no models built; no external metrics; no labels; no climate linkage; no data modified.**
- Per-country specifics are reasoned from verified literature + the verified OpenDengue descriptor; **exact coverage flagged "verify in catalog."** No external-validation claim made.
- **Only this markdown memo was created.** Nothing committed.
