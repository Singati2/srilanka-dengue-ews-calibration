# Paper Strategy Reframe Memo — honest operational dengue EWS framing (planning only — NO models)
*Reframes the Sri Lanka + Colombia dengue project around the **honest horizon-sensitivity result**: the climate–surveillance hybrid beats recent-case surveillance at every tested horizon, but the incremental value is **modest, robust, and roughly flat (not lead-time-increasing) across h=1–12 weeks**, and climate-only models are weak throughout. **Planning/interpretation only: no models run, no labels/data modified, nothing committed.** All result numbers quoted from committed reports.*

**Date:** 2026-06-18 · **Status:** strategy memo (planning) · **Base commit:** 2c7c095.

## A. Proposed title options
1. *"Climate adds modest but consistent value beyond recent-case surveillance for dengue early warning: a decision-curve evaluation in Sri Lanka and Colombia."* (recommended — descriptive, honest, decision-analytic)
2. *"Benchmarking matters: recent-case surveillance is hard to beat, and climate's contribution to dengue early warning is incremental and hybrid-only."*
3. *"How much does climate add? A surveillance-benchmarked, calibration- and net-benefit–based evaluation of dengue early-warning models across two countries."*
4. *(conservative methods framing)* *"A pre-specified decision-curve framework for evaluating climate-informed dengue early-warning systems, with external framework replication."*
- **Avoid:** any title implying climate "predicts dengue", "outperforms surveillance", "improves with lead time", or "validated/deployment-ready".

## B. New central thesis (one paragraph)
> Climate-informed dengue early-warning systems are usually benchmarked against weak baselines and judged by discrimination (AUC) alone. Under a pre-specified, calibration-aware, **decision-curve** evaluation that benchmarks against a recent-case surveillance baseline, we show across two settings (Sri Lanka primary; Colombia external framework replication) that **recent-case surveillance is hard to beat, climate-only models add little operational value, and climate's contribution is realized only as a modest, statistically robust increment when combined with surveillance in a hybrid**. In Colombia this hybrid increment is confirmed by municipality-cluster bootstrap at the primary h=4 horizon (M5 vs M1: ΔNB@0.30 +0.018 [0.012, 0.026]) and is **stable but does not grow across 1–12-week horizons**. The contribution is therefore methodological and operational — a reproducible, surveillance-benchmarked, net-benefit framework and an honest quantification of when (and how little) climate adds — rather than a claim of climate-driven predictive superiority.

## C. Claims we can make safely
- Recent-case surveillance is a **hard-to-beat operational benchmark**; climate EWS must be benchmarked against it, not against null/climatology baselines.
- **Climate-only models are weak** in both settings (≈ treat-all/treat-none at operational thresholds).
- A **hybrid surveillance+climate model adds a modest, statistically robust net-benefit increment** over surveillance (Colombia h=4; confirmed by cluster bootstrap), and this increment is **consistent across 1–12-week horizons**.
- **Calibration and net benefit are essential** — AUC gains alone can mislead about operational value.
- **External framework replication is feasible** with open data (OpenDengue + CHIRPS + ERA5-Land), with documented data-alignment and crosswalk methodology (a reusable resource).
- The cross-setting pattern is **complementary, not contradictory** (Sri Lanka regime-/threshold-limited; Colombia confirmed-but-modest).

## D. Claims we must avoid
- Climate value **increases at longer lead times** (h=1–12) — **not supported**.
- Climate-only outperforms surveillance · climate "predicts" dengue · causal climate effect.
- Global validation · deployment readiness · cost-effectiveness.
- That the hybrid increment is large or practice-changing (it is small: ΔNB ≈ +0.018 at p\*=0.30).
- That Colombia "confirms" a universal climate benefit (it is one external replication; Sri Lanka shows it is not guaranteed).

## E–F. Minimum additional experiments (with full specification)

### E1. Operational alert-threshold / decision-curve robustness (p\* = 0.10–0.50) — **MUST DO (before submission)**
- **Question:** is the hybrid's net-benefit advantage over surveillance robust across the operationally plausible decision-threshold range, or only at p\*=0.30?
- **Data needed:** existing committed h=4 + horizon predictions (already computed; `…dca_…csv` covers p=0.05–0.50). **No new fitting** — analysis/figure of existing outputs + cluster-bootstrap ΔNB at a grid of thresholds.
- **Model comparison:** M5 vs M1 (and M4 vs M1) ΔNB across p\*=0.10,0.15,…,0.50, with GID_2 cluster-bootstrap CIs.
- **Primary metric:** ΔNB(M5−M1) with 95% CI at each threshold.
- **Stop/fail:** if predictions/DCA outputs are missing or row sets mismatch.
- **If positive:** ΔNB>0 (CI excl 0) across most thresholds → the operational conclusion is threshold-robust.
- **If null:** ΔNB advantage confined to a narrow threshold band → report as threshold-sensitive; soften operational claim.

### E2. Longer-horizon feasibility (h = 16/20/24 weeks) — **OPTIONAL (not required before first draft)**
- **Question:** does the climate-dominant / climate-leading-indicator regime reported elsewhere at 3–6-month leads (≈12–26 weeks; Beal 2025, GeoHealth) emerge **beyond** our current 12-week ceiling?
- **Data needed:** **new label construction** for h=16/20/24 (current labels stop at h=12) using the *same* train-only 75th-pct rule; existing features (lag warm-up is on the predictor side, unaffected). Check labelable/common-complete n per horizon (will shrink; many municipalities may lack a t+h outcome).
- **Model comparison:** same M0–M5 ladder; M5 vs M1 ΔAUC/ΔNB.
- **Primary metric:** ΔNB(M5−M1) and absolute NB vs treat-all/none.
- **Stop/fail:** stop if common-complete test n collapses (e.g., <~3,000) or test one-class; or if NB for all models is indistinguishable from treat-none (floor).
- **If positive:** ΔNB(M5−M1) grows at 16–24 weeks → evidence for a longer-lead climate regime (would be a genuine new finding).
- **If null (expected, given NB already ≈0 at h=12):** outbreaks are not anticipable at these leads with these features → report honestly; reinforces that the operational window is short and surveillance-dominated.

### E3. Outbreak-threshold sensitivity (75th vs 80th vs 90th percentile) — **MUST DO (before submission)**
- **Question:** does the hybrid increment survive a **rarer, more epidemic-like** outbreak definition (higher percentile), or is it an artifact of the high-base-rate 75th-pct label (~25–40% prevalence)?
- **Data needed:** 90th-pct per-unit threshold **already computed** (`…thresholds…csv` has thr90); 80th-pct needs a small train-only recompute (no new data). Re-derive labels at 80/90; rebuild common-complete; refit ladder at h=4 primary.
- **Model comparison:** M5 vs M1 (and M2/M3 vs M1) at each label.
- **Primary metric:** ΔNB(M5−M1)@p\* with cluster-bootstrap CI; also report event prevalence and PR-AUC (rarer events).
- **Stop/fail:** stop if event prevalence at 90th-pct is too low for stable evaluation (e.g., <~3–5% with too few events) — then report 80th-pct only.
- **If positive:** ΔNB advantage persists at 80/90th-pct → robust to outbreak definition; strengthens the claim.
- **If null:** advantage vanishes for rarer outbreaks → climate's increment is specific to "above-typical" weeks, not true epidemics — an important honest qualifier.

### E4. Geographic transportability — leave-one-department-out (LODO) — **OPTIONAL (not required before first draft)**
- **Question:** does the hybrid's incremental value **transport across space** (train on 32 departments, test on the held-out one), or is it driven by a few departments?
- **Data needed:** existing Colombia h=4 common-complete table; LODO splits over the 33 departments (train-only thresholds re-fit per fold to avoid leakage; or use the committed temporal-train thresholds with spatial holdout documented).
- **Model comparison:** M5 vs M1 per held-out department; pooled ΔNB distribution across departments.
- **Primary metric:** distribution of ΔNB(M5−M1) across held-out departments; fraction of departments with ΔNB>0; pooled estimate.
- **Stop/fail:** stop if many departments have too few test events for a stable per-fold estimate (report only departments above a pre-set event floor).
- **If positive:** ΔNB>0 in a clear majority of departments → spatial transportability supported.
- **If null:** ΔNB driven by a minority of departments → report heterogeneity; temper the "general" claim and add a regime/heterogeneity analysis.

### E5. Climate lag-window / feature-richness sensitivity (longer lags, rolling summaries, DLNM-style) — **STRONG REVIEWER-DEFENSE (if time; pre-specify before running)**
- **Question:** is climate-only weakness an artifact of **under-modeling** climate (simple lags 0–8) rather than a true absence of signal? (Pre-empts the obvious reviewer objection, esp. since the Sri Lanka arm used a DLNM cross-basis.)
- **Data needed:** existing climate grid; **new feature assembly** for richer climate (lags 0–16, rolling means/sums over 4/8/12 weeks, optionally a DLNM-style cross-basis as in Sri Lanka). No new raw downloads.
- **Model comparison:** M2/M3 (rich climate) vs M2/M3 (current); M5 (rich) vs M5 (current) and vs M1.
- **Primary metric:** ΔAUC/ΔNB of richer-climate vs current-climate models; whether climate-only AUC materially exceeds ~0.56.
- **Stop/fail:** stop if richer features induce overfitting unhandled by the validation-tuned C (document).
- **If positive:** richer climate materially improves climate-only/hybrid → the weak-climate finding was partly feature-poverty; revise accordingly (still likely surveillance-dominant, but fairer to climate).
- **If null:** richer climate does **not** rescue climate-only → strengthens the core claim that climate is weak *as a standalone signal* and only useful as a hybrid increment, even when generously modeled.

## G. Experiment priority (tiered)
1. **Must do before submission:**
   - **E1** — operational alert-threshold / ΔNB robustness across p\*=0.10–0.50 (core to the decision-analytic claim; uses existing DCA outputs).
   - **E3** — outbreak-threshold sensitivity (75th vs 80th/90th percentile; is the increment real for rarer, more epidemic-like outbreaks?).
2. **Strong reviewer-defense if time:**
   - **E5** — climate feature-richness / longer lag summaries / DLNM-style or rolling climate robustness. **Must be pre-specified before running** (lock the feature families and grid in a committed spec first) to **avoid post-hoc feature hunting**; otherwise it becomes a fishing expedition that weakens, not strengthens, the paper.
3. **Optional / not required before the first manuscript draft:**
   - **E4** — leave-one-department-out transportability (strengthens generalizability, but the paper stands without it for a first draft).
   - **E2** — longer horizons h=16/20/24 (tests the long-lead regime; expected null given the NB floor at h=12; needs new labels).
- **Rationale:** E1 and E3 close the two attacks that would most directly undermine the core "modest, robust increment" claim (threshold cherry-picking and label cherry-picking) and are cheap. E5 pre-empts the "climate is merely under-modeled" objection but adds real scope and must be disciplined (pre-specified). E4/E2 are genuine strengtheners but not gating for a first submission.

### G.1 Immediate next practical step (sequence)
1. **E1 first** — decision-threshold robustness, reusing the **existing committed DCA outputs** (h=4 `…dca_…csv`; horizon `…dca_v1.csv`) plus a cluster-bootstrap ΔNB across thresholds. Lowest cost, highest necessity.
2. **Then E3** — outbreak-threshold sensitivity (thr90 already computed; thr80 a small train-only recompute).
3. **E5 only if** the team decides the reviewer defense is worth the additional scope — and only after a **committed pre-specification** of the climate feature families.
4. E4 and E2 remain deferred/optional. Each experiment stays a separately gated spec → run → report cycle.

## H. Recommended target framing & venue
- **Frame as a methods / public-health modeling paper**, not a high-impact epidemiology discovery. The result is a careful, partly-negative, decision-analytic finding plus a reusable framework and an open-data replication resource — high methodological value, low "novel discovery" value.
- **Realistic target venues (mid-tier, methods/global-health):** *PLOS Neglected Tropical Diseases*, *PLOS Global Public Health*, *BMC Medicine / BMC Infectious Diseases*, *Lancet Regional Health – Americas/Southeast Asia*, or an epidemiology-methods venue (TRIPOD-aligned). Avoid pitching to *Nature/Lancet* main or as a climate-EWS breakthrough — the honest finding will not support that framing and would draw rejection for over-claiming.
- **Positioning:** the selling points are (1) the **surveillance-benchmarked, calibration + net-benefit framework**; (2) the **honest "how much does climate actually add" answer** (a needed corrective to an over-optimistic literature); (3) the **open-data external-replication pipeline + data-alignment lessons** (WER ISO-week alignment, GID_2 crosswalk). TRIPOD-AI / PROBAST adherence and pre-registration are strengths to foreground.

## I–K. Confirmations
- **No models run; no predictions; no metrics computed; no labels/thresholds recomputed; no data or quarantine outputs modified; no Sri Lanka data changed.**
- **Planning/strategy memo only.** Experiment specs above are proposals — each would be a separately gated spec→run→report cycle.
- **Nothing committed** — this markdown is proposed for commit pending your approval.
