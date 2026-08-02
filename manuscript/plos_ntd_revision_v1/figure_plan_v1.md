# Figure plan v1 — ≤5 primary figures (frozen tables only)

Editable source: all figures are native TikZ/pgfplots inside `dengue_ews_plos_ntd_v1.tex` (no raster/screenshot plots). Coordinates transcribed from frozen `docs/*_report.md`.

| # | Figure | Source data (frozen) | Status |
|---|---|---|---|
| 1 | Study-design & surveillance-benchmark evaluation flowchart (colorblind-safe, category fills) | n/a (schematic) | **Done** (recolored Okabe–Ito, grayscale-legible) |
| 2 | Sri Lanka decision-curve / primary comparison (NB vs threshold) | `pilot_h4_75pct_calibration_dca_report.md`, `decision_threshold_dnb_robustness_report.md` | **Done** (pgfplots) |
| 3 | Sri Lanka calibration/recalibration summary (CITL before/after) | `rolling_recalibration_extension_report.md` | **Planned for SI or main** — Table 3 present; bar figure optional (move large grid to SI) |
| 4 | Colombia M0–M5 primary results with ΔNB | `colombia_model_ladder_report.md` | **Done** (AUC bars; NB in Table) |
| 5 | Cross-setting & horizon synthesis | `targeted_value_*`, `label_horizon_robustness_report.md`, `colombia_horizon_sensitivity_report.md` | **Planned** — currently a cross-setting **table** (Table) + horizon prose; convert to a 1–2 panel figure if desired |

## To Supporting Information
- Large Sri Lanka sensitivity grid (S1–S3 linkage/lag/anomaly), targeted-value regime table, Colombia outbreak-threshold (75/80/90) and horizon grids, technical provenance diagrams.

## Notes
- Original PDF Figure 3 (calibration bars) and Figure 6 (cross-country box) were consolidated: cross-country is now a quantitative table (per fidelity-audit recommendation); calibration bars optional.
- No figure introduces a number absent from a frozen report.
