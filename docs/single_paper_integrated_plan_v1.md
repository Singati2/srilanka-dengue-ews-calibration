# Integrated Single-Paper Plan (v1) — Benchmark + MAUP + Spatial-Honest Validation + Geospatial Model & Hybrid

*Author-side planning document. Status: DRAFT for PI + coauthor discussion. No implementation started; nothing here is committed or pushed. Supersedes the "Paper 1 vs Paper 2" split for the purpose of a single comprehensive paper.*

---

## 0. The decision and its honest consequences

**Decision (PI-level):** fold the WP4/WP5 program **and** a geospatially-developed new model + hybrid into **one** paper, rather than freezing v18 and deferring to Paper 2.

**What this changes — say it plainly:**
1. **Paper identity changes.** v18 is a *calibration/decision-curve evaluation under a fixed model ladder with a "no-new-model" rule.* Adding a developed geomatics model + hybrid makes it a **development-and-evaluation** paper. The title, abstract, and contribution claims must be rewritten (see §1).
2. **The "no-new-model" rule is deliberately retired** for the new-model component — and **replaced by a stricter discipline**: pre-specified protocol, leakage-proof *nested* spatial CV, multiplicity control, and mandatory honest-null reporting (§2). Without this substitution the paper is weaker than v18, not stronger.
3. **Timeline extends and review reopens.** The current v18's science is frozen and administratively-blocked only; this plan reopens the science for ~2–4 months of work (§7) plus a full new review cycle. That is the price of comprehensiveness. It is worth it **only if** the rigor items in §2 are honored.
4. **v18 is not discarded — it becomes the backbone.** The M0–M5 ladder + surveillance-benchmark + calibration/DCA result is the paper's *first half* (the "evaluation" contribution). We build the second half (development + spatial validation) on top of it.

**One thing that gets *better*:** doing a real pre-registration for the new-model component converts the audit's standing weakness ("no prospective public registration is claimed") into a strength.

---

## 1. Reframed paper

**Contribution, restated as four linked claims:**
1. **Benchmark (from v18):** recent-case surveillance is a demanding benchmark; climate-only adds little; evaluate by calibration + decision-curve net benefit, not discrimination.
2. **Exposure honesty (WP5/MAUP):** decisions are/are-not robust to how weather is aggregated over an area (area-mean vs population-weighted vs terrain-corrected).
3. **Spatial honesty (WP4):** the out-of-sample conclusion survives *spatially-blocked* validation, not just a temporal split.
4. **Development (new):** a geospatially-augmented model, developed under leakage-proof CV, does / does not beat recent surveillance on **calibrated decision value** — reported either way.

**Candidate titles (pick at PI level):**
- **A.** "Calibrated, decision-curve, and spatially-honest evaluation of climate- and geospatial-informed dengue alerting, with a surveillance-benchmarked hybrid model: evidence from Sri Lanka and Colombia."
- **B.** "Does geospatial information improve dengue alert decisions beyond recent surveillance? A spatially-validated development-and-evaluation study in Sri Lanka and Colombia."
- **C.** "From benchmark to model: surveillance-anchored development and spatially-blocked validation of a geospatial dengue alerting hybrid."

*Recommendation:* **B** — it keeps the honest question framing (which survives a null), signals development + validation, and does not overpromise outbreak "early warning."

**Structure (IMRaD, two-half spine):**
- Methods: settings → outcome/labels → **exposure builds (A/B/C)** → M0–M5 benchmark ladder → **spatial-honest CV design** → **geospatial feature screen + new-model development protocol** → **hybrid** → calibration/DCA endpoints → bootstrap.
- Results: (i) benchmark [v18], (ii) MAUP sensitivity, (iii) spatial-CV survival, (iv) developed model + hybrid performance.
- Heavy SI (the current v18 SI + new S13–S18).

---

## 2. Non-negotiable rigor (this is what makes the new-model paper survive review)

These five items directly answer the panel's kill-shots. Skipping any one hands a reviewer the paper.

**R1 — Power the development on Colombia, not Sri Lanka.**
Sri Lanka has **26 RDHS units** — you cannot develop/validate a multi-factor model or run a ~20-covariate F8 regression there (more covariates than units). **Colombia (~1,000 municipalities) LEADS** all new-model development, the F8 miscalibration panel, and the powered spatial-block CV. **Sri Lanka is confirmatory/sensitivity only** (buffered LOOCV as a companion, transparently underpowered). This single decision defuses the "hopeless at n=26 / multiplicity" objection.

**R2 — Nested, leakage-proof spatial CV.**
Feature selection, hyperparameter tuning, and threshold choice happen in the **inner** folds; performance is scored on **outer** spatial-block folds the selection never saw. No factor is chosen and evaluated on the same data. Temporal honesty (lags from the past only) preserved inside every spatial fold → **spatio-temporal nested CV**. This is the difference between a defensible development and optimistic garbage.

**R3 — Pre-specify everything before touching test performance.**
Lock, in a dated `analysis_plan_v2.md` (+ **OSF pre-registration**): the full candidate factor list and transforms; the model class(es); the selection rule (stability selection with a fixed threshold); the primary estimand; p\*; the endpoints; the multiplicity plan. "Include-then-prune on the same data" (as the current plan says) is a garden-of-forking-paths — replace it with **pre-registered stability selection**, where pruning is a rule, not a look.

**R4 — Multiplicity control with one confirmatory contrast.**
Exactly **one** primary confirmatory contrast: *does the hybrid improve ΔNB at p\* over M1 under outer-fold spatial CV, CI excluding 0, in Colombia?* Everything else (per-variable MAUP, factor importances, F8 covariates, SL companion, thresholds/horizons) is **exploratory**, reported with FDR control and labeled as such. Report all factors tried, not just survivors.

**R5 — Honest-null, and it's now genuinely honest.**
Because the paper is reframed as development-*and*-evaluation, a null ("geospatial augmentation does not beat recent surveillance on decision value") is a *headline-consistent, publishable* result — not something you're pre-committed to bury. This removes the panel's "publication-bias trap" objection **only under the reframe**; keep the v18 no-new-model framing and the trap returns.

---

## 3. Phase 0 — data staging (the critical-path blocker)

Nothing in WP4/WP5 is built; every input is outside the checkout. This is the schedule driver, not an afterthought.

| Input | Source | Needed for | Notes |
|---|---|---|---|
| Build-A exposure (area-weighted) | in quarantine | benchmark, contrasts | exists, re-verify checksum |
| WorldPop rasters (SL + Colombia) | quarantine / WorldPop | Build B weights | equal-area reproject |
| DEM (Copernicus GLO-30) | Copernicus | Build C, TWI/HAND | both countries |
| Colombia municipality boundaries + OpenDengue | HDX / OpenDengue V1.3 | all Colombia work | version+access date (fixes audit gap) |
| GHSL, ESA WorldCover, MODIS NDVI/LST, VIIRS, JRC GSW, Meta RWI | Google Earth Engine | F8 panel, factors | GEE avoids bulk download |
| Saved per-obs predictions | quarantine | reuse where possible | move out of quarantine into a deposit |

**Rule:** everything reprojected to an equal-area CRS before weighting; every derived table checksummed + FREEZE_LOG'd; **CSVs/rasters never committed** (code + reports only).

---

## 4. Integrated workstream sequence

**WS-A — Exposure builds (WP5).** Build B (population-weighted) → Build C (terrain-corrected temperature). Append the 3 free weekly variables (DTR, VPD/abs-humidity, SPI/SPEI) as candidate features (now *allowed* — they feed the new model under R2/R3). Row-aligned, checksummed.

**WS-B — Spatial-honesty backbone (WP4).** Estimate residual autocorrelation range (variogram/Moran's I) per country → build **Colombia spatial-block folds** (leave-department-out, buffered) and **SL buffered-LOOCV** (companion) → leakage-audit memo (0 within-range train/test pairs). *Do this early — the folds are the substrate for R2.*

**WS-C — Feature screen + geomatics-only model (Colombia-led).** Pre-registered candidate panel (weekly exposure factors + static factors). Stability selection **inside inner folds**. Report factor importance with uncertainty; separate spatial-importance from temporal-importance. Output: the "which factors matter" ranking you want, done leakage-proof.

**WS-D — The hybrid (the new centerpiece).** Recent cases (M1) + the pre-registered selected geospatial features → hybrid. Evaluate on **outer** spatial-CV folds with the same calibration + net-benefit + ΔNB machinery as the M-ladder. **This is the R4 primary contrast.** Then confirm in Sri Lanka as an underpowered sensitivity.

**WS-E — MAUP decision-sensitivity + F8 (Colombia-led).** F7: ladder→calibration→net-benefit across builds A/B/C, per-variable + pooled, decision-flip counts (with CIs — no bare counts). F8: regress per-unit calibration/ΔNB on the static covariate panel (Colombia; SL only if units allow), FDR-controlled, explanatory only.

**WS-F — Integration & operational translation.** Everything in per-100-unit-week decision units; both settings; consistent thresholds. Cross-setting presented descriptively (still no formal heterogeneity test unless a common estimand is defensible).

**WS-G — Reproducibility + admin (parallel track, do now).** These block submission regardless of the science: finalize S1–S3 (STROBE/TRIPOD+AI/PROBAST); **create env/requirements files** and recover/disclose Python versions (audit gap); mint Zenodo DOI + license + public repo URL; OpenDengue version/access date; declarations (ethics/funding/CoI/CRediT/ORCID/approval). Start these *today* — they're the long poles that don't depend on the modeling.

**Dependencies:** WS-A → (WS-C, WS-E). WS-B → (WS-C, WS-D). WS-C → WS-D. WS-G ∥ everything.

---

## 5. Locked endpoints (draft — finalize in analysis_plan_v2)

- **Primary (confirmatory):** ΔNB(hybrid − M1) at p\*=0.30, h=4, under Colombia outer-fold spatial CV; RDHS/municipality-cluster bootstrap CI. Win = CI excludes 0.
- **Co-primary robustness:** does the benchmark ranking (M1 vs climate-only) survive spatial CV vs the temporal split.
- **Secondary/exploratory (FDR-controlled):** MAUP ΔNB across builds A/B/C; per-variable MAUP; factor-importance ranking; F8 spatial structure of miscalibration; SL companion results; threshold/horizon grids.
- **Reported either way:** the honest-null on the hybrid.

---

## 6. Risk register (panel objections → mitigations)

| Risk | Mitigation |
|---|---|
| Underpowered at n=26 (dev + F8) | **R1** Colombia leads; SL confirmatory-only |
| Selection leakage → optimistic hybrid | **R2** nested spatial CV; select inner, score outer |
| Multiplicity / forking paths | **R3+R4** pre-registration; one confirmatory contrast; FDR on the rest |
| Estimand drift / "reopened science" | **R3** lock estimand up front; v18 benchmark preserved verbatim as the anchor |
| Publication-bias trap (geomatics hybrid) | **R5** reframe so a null is headline-consistent and reported |
| MAUP mis-spun as "conservative" | State MAUP direction is indeterminate; report flips with CIs, no directional spin |
| Data-staging slippage | Phase 0 is the critical path; trim order = population-product → optional F8 factors → Build C |
| Long time-to-submission | Run WS-G (admin/repro) in parallel now so only the science gates submission |

---

## 7. Indicative timeline (staff-dependent; calendar, not effort)

- **Weeks 0–3:** Phase 0 staging + `analysis_plan_v2` + OSF pre-registration (blocking) ∥ WS-G admin/repro started.
- **Weeks 2–5:** WS-A exposure builds; WS-B spatial folds + leakage memo.
- **Weeks 4–8:** WS-C feature screen + geomatics model (Colombia); WS-D hybrid + primary contrast.
- **Weeks 7–10:** WS-E MAUP/F8; WS-F integration + SL confirmatory.
- **Weeks 9–12:** write-up (new Methods/Results/SI), internal QC, PI sign-off.
- Then submit. **~3 months** with a dedicated geospatial lead + modeler; longer if staging is slow or GEE work is new.

**Scope dials (trim first if slipping):** population-product sensitivity (C7) → optional F8 factors (VIIRS/TWI/HAND/etc.) → Build C terrain correction → SL buffered-LOOCV. Keep the spine: Colombia spatial CV, one exposure sensitivity (A vs B), the developed hybrid + its honest primary contrast.

---

## 8. What we reuse from v18 (do not rebuild)

M0–M5 ladder + calibration/recalibration + DCA code; the frozen benchmark numbers (SL M4−M1, M5−M1; Colombia full-period); the bootstrap protocol/seed; the WER→ISO alignment; RDHS geometry + queen adjacency; the operational-translation language. The v18 benchmark section moves in essentially intact as Contribution 1.

---

## 9. Immediate next actions

1. **PI ratifies** the reframe (§0/§1) and the R1–R5 rigor spine (§2).
2. **Write `analysis_plan_v2.md` + OSF pre-registration** (locks factors, model class, selection rule, primary contrast) — *before* any modeling.
3. **Kick off Phase 0 staging** and the WS-G admin/repro track *in parallel, now*.
4. ~~Confirm the ambition dial~~ **DECIDED (2026-07-07): selected-feature hybrid (the spine).** The new model = recent cases (M1) + a small, pre-registered set of geospatial features chosen by leakage-proof stability selection. The full ~20-factor panel is a **controlled screen that feeds the hybrid**, not a standalone model. Consequence for `analysis_plan_v2`: pre-register (a) the candidate factor list + transforms, (b) stability-selection rule with a fixed selection threshold and a **pre-specified cap on the number of features entering the hybrid** (keeps EPV honest on Colombia's event count), (c) the single confirmatory contrast ΔNB(hybrid − M1). No standalone geomatics-only model is a headline deliverable (it may appear only as an exploratory SI reference point).

*No code, data, or manuscript was modified in producing this plan. Nothing staged, committed, or pushed.*
