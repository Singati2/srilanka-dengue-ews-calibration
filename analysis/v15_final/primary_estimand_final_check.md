# Phase 4 — Primary estimand audit: **PASS**

Checked against §C/§D of the consolidated prompt on `paper1_plos_gph_C2_final.tex`.

| Requirement | Status | Evidence |
|---|---|---|
| M5 − M5_no-climate is the ONLY matched estimand, labeled post hoc/exploratory | PASS | §D.1 methods block inserted ("Estimand hierarchy…"): "reported as a post hoc, exploratory analysis rather than a prespecified confirmatory estimand." Analysis-status table now lists "Sri Lanka M5−M5_no-climate (matched) — Post hoc specification diagnostic." |
| M4 − M1 retained but demoted, non-nested, "does not isolate climate" (never "confounded") | PASS | Present at abstract, L349, L381, and §D.1. No occurrence of "structurally confounded" (grep = 0). |
| M5 − M1 explicitly NOT matched, with the penalization/standardization reason | PASS | Fixed at 4 SL loci (results L255/L263, recal L349/L357, discussion L383, L393) + §D.1. Reason stated: frozen M1 fit near-unpenalized C=1e6, AR-only standardization vs M5 whole-design/C-selected. |
| §D.3 reconciliation present where +0.0081 and +0.0087 co-occur | PASS | Results paragraph: "The frozen-pipeline contrast M5−M1 (+0.0081) and the specification-matched contrast M5−M5_no-climate (+0.0087) differ by ≈0.0006 because …". |
| Independent-refit evidence for M5_no-climate; +0.0006 gap explained | PASS | fit_eval('matched') is a from-scratch LogisticRegression().fit; gap explained by penalty/standardization (matched_pair_confirmation.md, v14 closeout). |
| "Prespecified/design-locked" NOT applied to the matched estimand | PASS | §D.1 closing sentence restricts prespecification to "the original model ladder and the structured Sri Lanka M1 specification, not to the revision-stage matched estimand." Grep for prespecif/design-lock near no-climate = 0 positive claims. |
| No residual M1-level cross-country comparison as if identical | PASS | Cross-setting synthesis confined to M5−M5_no-climate; explicit non-comparability disclosure retained. |
| No "same/similar/comparable magnitude" wording | PASS | grep = 0; replaced with "consistently-signed … of uncertain, setting-varying magnitude." |

**Verdict: estimand audit PASS — no STOP condition.**
