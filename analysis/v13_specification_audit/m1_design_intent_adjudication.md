# M1 design-intent adjudication (Phase 4) — PIVOTAL

## Finding: **INTENDED-STRUCTURED**

The Sri Lanka `M1` structure (recent-case lags + seasonal harmonics + RDHS fixed effects) was the **intended** design; the manuscript methods prose ("M1 = recent incidence lags only, no seasonal or geographic terms") is the error. Evidence is convergent across the required signals and is **independent of the frozen code's runtime behaviour**.

## Convergent evidence

| # | Signal | Source | What it shows |
|---|---|---|---|
| 1 (plan) | Dated design-lock spec | `docs/hybrid_model_extension_spec.md` L17 | **"M1 — recent-cases AR baseline: the existing committed model (incidence lags t, t−1, t−2, t−4 + harmonics + RDHS FE)…"** — M1 is *explicitly specified as structured*, in a pre-computation document. |
| 1 (plan) | Colombia ladder spec | `docs/colombia_model_ladder_spec.md` L35 | **"M1 — recent-surveillance baseline: cases_lag0,1,2,4"** — Colombia M1 is *explicitly cases-only*. The two countries' baselines are **deliberately different by design**, each documented in its own dated spec. |
| 4 (ladder coherence) | SL spec | `hybrid_model_extension_spec.md` L18–19 | M4 = "M1's lagged dengue features + climate cross-basis" (i.e. AR+climate, no harmonics/RDHS); M5 = "M4 plus harmonics and RDHS FE." The ladder is internally coherent as an intended design: M1 = structured surveillance benchmark, M4 = "cases+climate vs structured surveillance," M5 = "climate added to structured surveillance." The spec states "the contrast that matters is M4 vs M1." |
| 2–3 (mechanism) | code vs specs | `_run_rolling_recal.py`, `_run_hybrid_model_extension.py` | SL M1 receives `['sin1','cos1','sin2','cos2']+rd_cols` as structural features **by design** (matching the spec), not via an accidental shared-object leak; Colombia M1 is built cases-only per its own spec. Not a copy-paste leak. |
| 3 (reproduction) | Phase 3 | validated | Reconstructed M1/M4/M5 reproduce the committed frozen predictions to max|Δ| ≤ 1.1e-16 over all 3,926 aligned test rows (row-identity verified). Confirms code faithfulness (necessary, not sufficient — used only to confirm we audited the same model the spec describes). |

## Reconciling the conflicting signal (item 5, prose)
The manuscript methods prose said "M1 = recent incidence lags only." This **conflicts** with the design-lock spec (item 1). The dated pre-computation spec is the authoritative statement of design *intent*; the methods prose is a later, incomplete/incorrect *description*. The prose is therefore the error, not the code. (This is the one signal pointing the other way; it is a description, not a design artifact, and is outweighed by the explicit spec.)

## Why NOT UNINTENDED-BUG
A bug would require the structure to have entered SL M1 *against* the documented design. The opposite is true: the dated spec *explicitly prescribes* "harmonics + RDHS FE" for SL M1. There is no design document defining SL M1 as cases-only. Colombia's cases-only M1 is a separate, deliberately different specification.

## Author confirmation (still recommended)
This adjudication rests on the authors' own dated design-lock spec, which is strong. A one-line confirmation from Khadka/Thapa/Shiwakoti — *"Was Sri Lanka M1 specified as cases-only or as cases + seasonality + RDHS?"* — would finalize it beyond doubt. The documentary evidence already answers it (structured).
