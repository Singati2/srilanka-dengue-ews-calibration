# S10 Text — Reproducibility artifact inventory and checksums (transcribed; no recomputation)
Selected frozen-artifact identifiers (from committed reports). Full inventory pending author finalization.

- Committed Sri Lanka primary predictions: `predictions_h4_75pct_v1.csv` / `07f5916a…` (referenced in hybrid report).
- Canonical R dlnm sessionInfo: `~/data_quarantine/.../R_sessionInfo_v1.txt` sha256 `e5f28716…` (R 4.6.0; dlnm 2.4.10; mgcv 1.9.4; tsModel 0.6-2).
- Colombia OpenDengue extract: `Temporal_extract_V1_3.zip` sha256 `7f5df21…` (version V1.3 verified locally).
- Colombia committed h=4 metrics `…model_metrics_h4_75pct_v1.csv` `c2dd62f0…`; bootstrap `319b35459…`.
- Software: R 4.6.0 / dlnm 2.4.10 / mgcv 1.9.4 / tsModel 0.6-2 verified; Python modeling-stack versions NOT preserved.

## Secondary-sensitivity artifacts (added in v12, retained in v13; transcribed from audited v2 outputs, no recomputation)
- Colombia 2022-only sensitivity: input `colombia_model_predictions_h4_75pct_v1.csv` sha256 `a938a138…` (recalibrated/post-Platt columns); B=1000, seed 20260630, municipality (GID_2) resampling, 0 failures. Outputs: `colombia_2022_only_v2` report; `colombia_2022_only_results.csv`, `colombia_2022_only_contrasts.csv` (v1 run retained unchanged).
- Sri Lanka wild-cluster-bootstrap-t: input `hybrid_model_predictions_v1.csv` sha256 `0f505fed…`; B=9999, seed 20260631, RDHS (26) clusters, Webb six-point weights. Environment: Python 3.10.12; `wildboottest` 0.3.2 wheel sha256 `886762642098358ddeb190656fc05c17e26d5c024ccff9f8863627ce3392902f`; statsmodels 0.14.6, numpy 1.26.4, pandas 2.1.3, scipy 1.11.4, numba 0.58.1 (full pip freeze, 490 packages, preserved in the sensitivity workspace). Single-implementation; statistics/CR-SE independently reproduced with statsmodels; full-precision bounds in `S11_srilanka_wild_cluster_bootstrap_t_results.csv`.

This is a partial inventory transcribed from frozen reports and audited secondary-sensitivity outputs; the complete checksum manifest is an author-finalization item.
