# Residual spatial-autocorrelation diagnostic (reviewer M10)

Moran's I on per-unit mean residuals (outcome - prediction), row-standardized weights,
9999-permutation test, seed 20260612. Reproduce: `python3 moran_residuals.py`.

## Adjacency provenance (verified)
- **Sri Lanka (26 RDHS):** built from public HDX COD-AB Sri Lanka ADM2 districts (the source the
  manuscript cites); Ampara district split into Ampara (LK52A) + Kalmunai (LK52K) using the
  committed 26-RDHS build report's neighbour lists. **VERIFIED against the committed graph:**
  26 nodes, 60 edges, degree min/med/max 2/4/9, Kalmunai degree 2, and the report's named edges
  (Ampara-Matale, Ampara-Hambantota, Jaffna-Mullaitivu) all reproduced; the geometric queen graph
  independently recovered whole-Ampara's 6 neighbours including the flagged long borders.
- **Colombia (31 test departments):** built from public GADM v4.1 GID_1 departments (the source
  the manuscript cites; department_id parsed from the GADM GIDs carried in the frozen data). No
  committed department graph exists to cross-verify; mapping is inherent in the data's GIDs.

## Results
| Setting | Model | Moran's I | E[I] | perm p |
|---|---|---|---|---|
| Sri Lanka (n=26) | M5 full, recal | -0.125 | -0.040 | 0.33 |
| Sri Lanka (n=26) | M5 no-climate, recal | -0.065 | -0.040 | 0.63 |
| Colombia (n=31) | M5 full, recal | +0.203 | -0.033 | 0.095 |
| Colombia (n=31) | M5 no-climate, recal | +0.223 | -0.033 | 0.063 |

## Interpretation
No significant residual spatial autocorrelation in Sri Lanka. Colombia shows borderline positive
autocorrelation (not significant at 0.05, but p approx 0.06-0.10), a mild caution for the
department-level cluster-bootstrap exchangeability assumption in the load-bearing setting.
