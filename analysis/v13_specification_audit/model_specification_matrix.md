# Model specification matrix (Phase 2) — from CODE + dated specs, not manuscript prose

| Model | Sri Lanka (spec `hybrid_model_extension_spec.md` + code) | Colombia (spec `colombia_model_ladder_spec.md` + code) |
|---|---|---|
| M1 | recent-case lags (t,1,2,4) **+ seasonal harmonics + RDHS FE** (fit_score, C=1e6) | recent-case lags (0,1,2,4) **only** (cases-only) |
| M2 | climate-only | climate-only |
| M3 | climate + season + RDHS FE | climate + season + dept FE |
| M4 (primary) | M1's **case lags** + DLNM climate cross-basis (temp/precip/RH, lags 0-8, cr df=3) — **no** season/RDHS | cases + linear climate lags — no season/dept |
| M5 | M4 + season + RDHS FE (= cases+climate+season+RDHS) | cases + climate + season + dept FE |
| M5_no-climate (matched) | cases + season + RDHS (independently fit, same procedure) | cases + season + dept (independently fit) |

- Outcome: 75th-pctile h=4 elevated-activity label. Train SL 2018-2022 / test 2023-2025; CO train 2006-2017 / val 2018-19 / test 2020-2022.
- **Key asymmetry:** SL M1 carries season+RDHS (structured); CO M1 is cases-only. Deliberate, per each country's dated spec. ⇒ M1-level cross-country comparisons non-comparable; matched estimand (M5−M5_no-climate) is comparable.
- Reproduction: reconstructed SL M1/M4/M5 match frozen predictions to ≤1.1e-16 (3,926 rows, identity-verified).
