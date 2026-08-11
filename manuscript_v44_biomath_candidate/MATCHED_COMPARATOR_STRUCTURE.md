# MATCHED_COMPARATOR_STRUCTURE

Evidence that the matched climate ablation compares two models differing **only by the climate feature block**, so that $\mathcal I^{S}\subseteq\mathcal I^{SC}$ is a legitimate nested-information contrast. All facts are transcribed from the canonical v44 manuscript (`manuscript_v44/revised_manuscript.tex`, SHA256 `08fad12b…`); no analysis was run.

## The matched pair
- **Full model:** M5.
- **Matched comparator:** M5$_{\text{no-climate}}$ = M5 with **only** the climate feature block removed (canonical: "retains the same case-history, seasonal, and geographic terms, preprocessing, model family, and rows as M5").
- **Contrast:** $\Delta$NB(M5$-$M5$_{\text{no-climate}}$), and analogously $\Delta$NLL/$\Delta$Brier/$\Delta$AUC — the metric-specific increments $\Delta V_{C,k}$.

## Feature-block decomposition (canonical S9 Table; Colombia design-matrix widths)
| Model | Feature blocks | # features |
|---|---|---|
| M1 | recent-case lags | 4 |
| M4 | cases + climate lags | 22 (cases + 18 climate) |
| **M5$_{\text{no-climate}}$ (matched)** | cases + season + 32 dept FE | **40** |
| **M5 (full)** | cases + climate + season + 32 dept FE | **58** |

**58 − 40 = 18 climate columns** — the matched pair differs by exactly the climate block. This is the arithmetic backing the nesting claim.

## Shared vs differing components
| Component | Shared across the matched pair? | Evidence |
|---|---|---|
| Row universe ($\mathcal R$) | **Yes** | CO 13,361 muni-weeks / SL 3,926 RDHS-weeks; "identical rows"; keys verified identical (S18: 0 duplicate keys, 0 missing probabilities) |
| Case-history block | Yes | retained in both |
| Seasonal block | Yes | retained in both |
| Geographic block (32 dept FE, CO; RDHS FE, SL) | Yes | retained in both |
| Climate block | **No — this is the only difference (18 cols, CO)** | S9; the estimand |
| Estimator family ($\mathcal A$) | Yes | penalized (L2) logistic, Python |
| Preprocessing / missingness | Yes | same pipeline (Version-6) |
| Calibration machinery ($\mathcal C$) | Yes (per setting) | SL rolling-52 intercept-only; CO Platt on validation |
| Evaluation / bootstrap machinery | Yes | SL RDHS(26); CO municipality(475) conditional, department(31) dev-inclusive |
| **Tuning rule ($\Lambda$)** | **Partial** | "both models independently fit under the same development protocol (so the selected penalty may differ)" |

## Regeneration fidelity
Matched no-climate predictions were regenerated through the verbatim Version-6 pipeline: Colombia regenerated M5 matched the frozen file to $1.1\times10^{-16}$; Sri Lanka M1/M4/M5 reproduced to $<10^{-6}$ (S18). The reconstructed Colombia matched point was $+0.00783$ vs frozen $+0.00786$ (S17).

## Three separate concepts (do not conflate)
- **`FEATURE_SET_NESTING` = PASS.** $\mathcal I^S\subseteq\mathcal I^{SC}$: M5$_{\text{no-climate}}$ is M5 minus exactly the 18-column climate block (S9: 58 vs 40). The information sets are strictly nested.
- **`DEVELOPMENT_PROTOCOL_MATCHING` = PASS.** The pair shares row universe, preprocessing, estimator family (L2 penalized logistic), tuning **algorithm/rule**, calibration algorithm, evaluation machinery, and bootstrap structure (see the shared/differing table above; canonical Methods "same procedure"/"identical rows, model family, tuning, recalibration").
- **`FITTED_PARAMETER_IDENTITY` = NOT REQUIRED.** The two models are independently refitted and tuned under the same rule, so the selected L2 penalty $C$ may differ; identical fitted parameters are not required and not claimed. The single-penalty refit (+0.0087 → +0.0099, canonical line 171; provenance in `SINGLE_PENALTY_0099_PROVENANCE.md`) shows the increment is not an artifact of differential regularization.

**Approved wording (used in the candidate):** *the matched pair used the same development protocol and identical non-climate structure, while each model was independently refitted and tuned under the same rule; the full model additionally included the climate block.* **Do not** write "the fitted models were identical except for climate."

## Verdict on the nested-information interpretation
- **Information-set nesting $\mathcal I^{S}\subseteq\mathcal I^{SC}$: PASS.** The comparator is M5 minus exactly the 18-column climate block; all other feature blocks, rows, estimator, preprocessing, calibration, and evaluation machinery are shared.
- **Bit-identical fitting machinery: PARTIAL.** The L2 penalty $C$ is selected independently per model, so the two fits are not identical maps of the shared features. The manuscript addresses this directly: refitting both matched models **under a single identical penalty** left the Sri Lanka increment essentially unchanged (+0.0087 → +0.0099), so the increment is not an artifact of differential regularization.

**`MATCHED_INFORMATION_SET_IDENTITY = PASS (with a documented PARTIAL on penalty-selection identity, shown not to drive the result).`**

## Contrast with the non-nested M4−M1
M1 = 4 features (recent-case lags only, in Colombia); M4 = 22 (cases + 18 climate, no season/FE). So M4 and M1 differ by climate **and** by the absence of the seasonal/geographic structure — they are **non-nested**, and $\Delta$NB(M4−M1) does **not** isolate the climate block. This is why the matched ablation (M5 vs M5$_{\text{no-climate}}$), not M4−M1, is the climate-specific estimand. In Colombia the matched increment (+0.0078) is ~42% of the compound M5−M1 (+0.0188), quantifying how much of the compound was seasonal/geographic rather than climate.
