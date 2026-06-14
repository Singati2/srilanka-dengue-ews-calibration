# Specification — Novel Contribution: Targeted Value of Climate Information for Dengue EWS (design-lock)
*Pre-computation design lock for a **novel, 2026-aligned** contribution: a regime-conditional, spatially-explicit, decision-analytic estimate of the **incremental value of climate information** over a surveillance-only dengue early-warning baseline. **No models run; no metrics computed; no data modified.** Documentation only. Reuses the committed, frozen, date-aligned pipeline; adds conditional net-benefit estimation, a spatial (BYM2) value surface, and population-weighted exposure.*

**Date:** 2026-06-14 · **Status:** specification only — locks the estimand, regimes, models, and pre-committed interpretation before any computation. Honesty constraint: this is a **framework + map** contribution, **not** a claim that climate beats surveillance on average.

## 1. The novelty (and why it is novel)
The dengue-EWS field evaluates climate-vs-surveillance primarily on **average discrimination** (AUC/RMSE/CRPS). The verified 2026 literature (see `docs/literature_landscape_repositioning_v1.md`) shows:
- climate's discrimination edge is **regime-dependent** (Beal et al., *GeoHealth* 2025, DOI 10.1029/2024GH001325 — skillful at long lead / low incidence / weak autocorrelation);
- **spatial representativeness** of climate inputs drives predictive utility, distinct from marginal association (Khamthong & Phramrung, *PLoS NTD* 2026, DOI 10.1371/journal.pntd.0014270);
- decision-curve / net-benefit is standard in clinical prediction (Gulati et al., *Circ. CQO* 2022, DOI 10.1161/CIRCOUTCOMES.121.008487; Benitez-Aurioles et al., *Diagn. Progn. Res.* 2026, DOI 10.1186/s41512-026-00224-z) but **essentially absent in dengue EWS**.

**To our knowledge, and consistent with that verified landscape, no dengue-EWS study has estimated the *conditional, spatially-explicit, net-benefit* value of climate information** — i.e., *when and where* adding climate to surveillance is operationally worth it. That is the novel contribution. (Novelty is asserted relative to the reviewed verified literature, not as an absolute "first.")

## 2. Primary estimand
**Conditional incremental net benefit of climate information:**
> ΔNB_climate(p\*, z) = NB(surveillance + climate model | p\*) − NB(surveillance-only baseline | p\*), estimated **conditional on regime z**, with RDHS-cluster bootstrap 95% CIs.

- "surveillance-only baseline" = **M1** (recent-cases AR), the committed baseline.
- "surveillance + climate" = the **hybrid** model (M5 = AR + DLNM-style climate cross-basis + season + RDHS FE), the committed near-miss.
- ΔNB_climate > 0 with CI excluding 0 in regime z ⇒ climate information adds operational value **in that regime**.

## 3. Conditioning regimes (z) — pre-specified
1. **Lead time:** h ∈ {1, 2, 4, 8, 12} (committed label/horizon grid).
2. **Local autocorrelation regime:** per-RDHS strength of recent-case predictability (e.g., training lag-1 autocorrelation of incidence), split at the training median into "strong-AR" vs "weak-AR" RDHS — *defined on training only*. (Direct test of Beal's "climate helps when AR is weak.")
3. **Incidence regime:** weeks below vs above the RDHS training median incidence ("low" vs "high") — *training-defined thresholds*. (Tests Beal's "climate helps when incidence is low.")
4. **Space:** per-RDHS, smoothed with a **BYM2 spatial model** over the committed 26-RDHS adjacency graph (`rdhs_26_v1` adjacency) → a **value-of-climate surface** (map).

## 4. Spatial / statistical modeling (the math/stat upgrade)
- **Per-RDHS ΔNB** estimated, then **spatially smoothed via a BYM2 (Besag–York–Mollié 2) model** on the committed adjacency (structured + unstructured random effects) to produce stable per-division value estimates and a map. *This finally uses the BYM2 adjacency graph built early in the project.* (Implementation: Python; if R/INLA is later approved, an INLA fit mirrors the EWARS-csd stack — gated, not required.)
- **Conditional ΔNB** estimated by stratified decision-curve analysis and, as a model-based complement, a **varying-coefficient / interaction specification** (ΔNB or the underlying alert prediction as a function of regime covariates), train-only fitting.
- **Continuous net benefit** (area under the decision curve across the p\*=0.20–0.40 band; Benitez-Aurioles 2026) reported per regime, so conclusions are not threshold-pinned.
- **Value-of-information framing:** report the conditional ΔNB as the expected operational gain from acquiring/using climate inputs, per regime — the deployable "targeting rule."

## 5. Geomatics axis (the geomatics engineer's headline deliverable)
- Rebuild the RDHS climate exposure under **population-weighted** aggregation (and an elevation-corrected variant if feasible) vs the committed **area-weighted (`all_touched`)** exposure, using the already-quarantined ERA5-Land/CHIRPS rasters + WorldPop denominators.
- Re-estimate the value-of-climate surface under each exposure construction → a **MAUP / spatial-representativeness sensitivity** directly testing Khamthong & Phramrung 2026: *does better spatial representativeness change where/whether climate is worth it?*
- This is a genuine methodological result, not housekeeping.

## 6. Evaluation cell & discipline (reuse committed frame)
- Same date-aligned v2 table (`3a197d61…`), 75th-pct label, h=4 primary (others as the lead-time regime), train 2018–2022 / test 2023–2025, same modelable rows.
- **Leakage/repro:** all thresholds, regime splits, knots, scaling, exposure weights, BYM2 hyperpriors learned/fixed on **train only**; predictions on identical test rows; deterministic seeds (20260612); RDHS-cluster bootstrap (B=1000) for all ΔNB CIs.
- Exact-row stop-gate vs committed predictions, as in prior steps.

## 7. Strict, pre-committed interpretation (outcome-robust — novelty either way)
- **If ΔNB_climate > 0 (CI excludes 0) in identifiable regimes** (e.g., weak-AR / low-incidence / long-lead / specific RDHS): the contribution is a **deployable targeting rule + value map** — "climate is worth adding specifically when/where …" (positive novel finding).
- **If ΔNB_climate does not exclude 0 in any regime**: the contribution is a **decision-analytic cautionary result** — "climate's regime-dependent *discrimination* gains (Beal 2025) do not convert to *operational decision value* even conditionally, including under population-weighted exposure" (still novel, still publishable, still honest).
- **Either way:** no claim that climate beats surveillance on average; no deployment-readiness claim; the framework + map is the contribution. **No headline finalized without team review.**

## 8. Honest constraints / what this is NOT
- It is **not** external validation (single country); an OpenDengue multi-country transportability arm is a separate, later step.
- The climate model remains a **Python DLNM-style cross-basis approximation**, not canonical R `dlnm`/INLA (stated throughout); an EWARS-style INLA comparator is a separate gated upgrade.
- No serotype/immunity or mobility data (named field gaps); out of current scope.
- Novelty is asserted **relative to the verified reviewed literature**, with a hedge ("to our knowledge"), not as an absolute first.

## 9. Outputs (LATER, not now) — quarantined only
Future directory: `~/data_quarantine/model_pilots/value_of_climate_v1/`
- `conditional_dnb_v1.csv`, `value_of_climate_surface_v1.csv` (per-RDHS BYM2 estimates), `exposure_sensitivity_v1.csv` (area- vs population-weighted), `vci_diagnostics_v1.csv`, `value_of_climate.meta.md`.
CSVs read-only + SHA256; **none committed**. Future safe report: `docs/targeted_value_of_climate_report.md`. Map figure(s) built by the team from the quarantined surface CSV. Prior outputs not overwritten.

## 10. Confirmation
- **No models run; no metrics computed; no labels created; no data modified.**
- **Only this markdown spec was created.** Nothing committed. Preregistration unchanged.

## Next step (separate, approval-gated)
On approval, execute in gated stages: (1) conditional ΔNB by lead/AR/incidence regime on committed predictions; (2) per-RDHS BYM2 value surface on the committed adjacency; (3) population-weighted exposure rebuild + sensitivity (geomatics); (4) quarantined outputs + safe report + team-built map. Each stage reports honestly under §7. Nothing runs until directed.
