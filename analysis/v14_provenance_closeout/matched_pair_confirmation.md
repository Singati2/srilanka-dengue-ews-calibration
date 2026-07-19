# Task 2 — Matched no-climate model independently refit? **VALID**

Source: `analysis/v12_referee_response/run/sl_matched_and_recal.py` (the validated reconstruction; reproduces frozen M1/M4/M5 to ≤1.1e-16, gate enforced at L102–103: exits without reporting if any Δ ≥ 1e-6).

| # | Check | Evidence (quoted) | Result |
|---|---|---|---|
| 1 | Fit from scratch, not coefficient-zeroing | `pmatch,_ = fit_eval('matched')` (L112); `fit_eval` calls `LogisticRegression(penalty='l2',C=bestC,…).fit(Xtr,ytr)` (L80). A new estimator is `.fit()`; no climate coefficient of M5 is zeroed. | PASS |
| 2 | Same training rows as M5 | Both `fit_eval('M5')` and `fit_eval('matched')` build `Xtr` from the same `tr` frame and label `ytr` (L69,79–80). | PASS |
| 3 | Same penalty-tuning protocol | Both run the identical rolling-origin C-grid AUC selection in `fit_eval` (L70–78). Selected C may differ between the two independent fits, so non-climate coefficients can shift across the pair — this is a **predictive incremental-value** contrast, not a coefficient-level decomposition. | PASS (with stated caveat) |
| 4 | Same test set | Both predict on `Xte`/`te` (`design(te,kind)`, L69,82); NB evaluated on the same `yte`. | PASS |
| 5 | Differs only by the climate block | `design('M5')=[AR, cb, season, RD]` (L61) vs `design('matched')=[AR, season, RD]` (L59). The sole difference is `cb = climate_block` = DLNM cross-basis over temp/precip/humidity, lags 0–8, `cr(df=3)` (L51–55). Exact columns removed = that cross-basis block. | PASS |

## The +0.0006 gap is explained
ΔNB(M5 − M5_no-climate) = +0.0087 vs ΔNB(M5 − M1_frozen) = +0.0081. `M5_no-climate` (`fit_eval('matched')`, whole-design standardization, C-selected) is a **different fit** from the frozen `M1` (`fit_score_M1`, C=1e6 near-unpenalized, AR-only standardization; L84–89). Same structural columns (AR+season+RDHS), different penalty/standardization ⇒ different predictions ⇒ the 0.0006 difference. This is exactly the signature of an **independent refit**, not of M1 relabeled or coefficients zeroed. 

**Matched estimand: VALID.** (Caveat carried forward: it is post-hoc — constructed at revision, not in the frozen pipeline.)
