"""Freeze the M6-core artifact (instruction_m6.md §6 / §24 item 1).

Hashes the notebooks, inputs, outputs and figures that produced the reported M6
result, so no future run can silently overwrite it. Notebook hashes are taken
from the committed blobs at FREEZE_COMMIT, not the working tree, because the
committed state is what produced the record.

Emits analysis/geomatics_integration_v1/M6_CORE_FROZEN_MANIFEST.yaml.
"""
import hashlib
import json
import subprocess
from pathlib import Path

import pandas as pd

REPO = Path("/Users/mpcr/aj/Dengue/srilanka-dengue-ews-calibration")
QUAR = REPO / "data_quarantine" / "m6_geomatics"
FIGS = REPO / "Manuscript_Figures" / "m6"
OUT = REPO / "analysis" / "geomatics_integration_v1"
FREEZE_COMMIT = "ff6287d0e336ab4e3a3d178593d3bb28e3f33a21"

NOTEBOOKS = [
    "00_setup_and_geometry", "01_terrain_batchA", "02_dynamic_modis",
    "03_batchB_statics", "04_feature_assembly", "05_label_and_row_mask",
    "06_fit_m6", "07_evaluation", "08_figures",
]


def sha16(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def git_blob_sha16(commit, relpath):
    """Hash the committed blob, not the working tree."""
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{commit}:{relpath}"],
        capture_output=True, check=True).stdout
    return hashlib.sha256(blob).hexdigest()[:16]


def worktree_differs(relpath):
    r = subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", "HEAD", "--", relpath])
    return r.returncode != 0


nb06 = json.loads((QUAR / "nb06_provenance.json").read_text())
nb07 = json.loads((QUAR / "nb07_provenance.json").read_text())
nb08 = json.loads((QUAR / "nb08_provenance.json").read_text())

# test row-key identity: hash the sorted (unit, week) keys of the frozen panel
mp = pd.read_csv(REPO / "ALT_STATS" / "frozen" / "srilanka_matched_pairs.csv",
                 parse_dates=["predictor_week"])
keys = (mp[["spatial_unit_id", "predictor_week"]]
        .sort_values(["spatial_unit_id", "predictor_week"])
        .astype(str).agg("|".join, axis=1))
rowkey_hash = hashlib.sha256("\n".join(keys).encode()).hexdigest()[:16]

# how much of the test set rests on a test-informed (clamped) threshold
thr = pd.read_csv(QUAR / "m6_label_thresholds_srilanka_v1.csv")
mp2 = mp.rename(columns={"spatial_unit_id": "geometry_id"})
mp2["target_year"] = (mp2.predictor_week + pd.Timedelta(days=28)).dt.year
j = mp2.merge(thr[["geometry_id", "year", "source"]],
              left_on=["geometry_id", "target_year"], right_on=["geometry_id", "year"], how="left")
clamped = j.source.str.startswith("clamped")

L = []
a = L.append
a("# M6-core frozen manifest")
a("# instruction_m6.md §6 — freeze the present result so it cannot drift.")
a("# NO FUTURE RESULT MAY OVERWRITE THIS VERSION. A re-fit goes to a new version tag.")
a("")
a("model_label: M6-core (A/B/C)")
a(f"freeze_commit: {FREEZE_COMMIT}")
a("country: sri_lanka")
a("label_source: recovered")
a("quotable: true")
a("feature_manifest: analysis/geomatics_integration_v1/M6_CORE_FEATURE_MANIFEST.yaml")
a("")
a("notebooks:  # sha256[:16] of the committed blob at freeze_commit")
for n in NOTEBOOKS:
    rel = f"notebooks/{n}.ipynb"
    flag = "  # worktree differs (re-execution noise only)" if worktree_differs(rel) else ""
    a(f"  {n}: {git_blob_sha16(FREEZE_COMMIT, rel)}{flag}")
a("")
a("rows:")
a(f"  train: {nb06['split']['train']}")
a(f"  val: {nb06['split']['val']}")
a(f"  test: {nb06['split']['test']}")
a("  test_panel: 26 RDHS x 151 weeks, 2023-01-02 to 2025-11-17")
a(f"  test_rowkey_sha256_16: {rowkey_hash}")
a("  identical_to_frozen_comparator_rows: true")
a("")
a("model:")
a(f"  estimator: {nb06['model']['class']}")
a(f"  penalty: {nb06['model']['penalty']}")
a(f"  C_selected: {nb06['model']['C_selected']}")
a(f"  C_grid: {nb06['model']['C_grid']}")
a("  C_selected_on: validation log loss (val carved from train tail, 2022-01-01 onward)")
a(f"  n_features: {nb06['features']['n']}")
a("  feature_selection: none")
a(f"  standardized_on: {nb06['features']['standardized_on']}")
a(f"  seed: {nb06['seed']}")
a("")
a("calibration:")
a(f"  m6_method: {nb06['recalibration']['method']}")
a(f"  m6_platt_intercept: {nb06['recalibration']['intercept']}")
a(f"  m6_platt_slope: {nb06['recalibration']['slope']}")
a("  comparator_method: past-only rolling-52-week recalibration")
a("  primary_comparison: raw predictions")
a("  primary_comparison_reason: >-")
a("    M6 and the comparators use different recalibration schemes; raw keeps all three on")
a("    equal footing. Per instruction_m6.md §10 the raw contrast is the primary fair")
a("    standalone comparison and calibrated differences must not be read as pure")
a("    model-information differences.")
a("")
a("uncertainty:")
a(f"  scheme: {nb07['uncertainty']['scheme']}")
a(f"  B: {nb07['uncertainty']['B']}")
a(f"  seed: {nb07['uncertainty']['seed']}")
a(f"  failures: {nb07['uncertainty']['failures']}")
a(f"  pstar: {nb07['pstar']}")
a("")
a("modis_gap_rule:")
a("  gap: 2025-07-04 to 2025-11-17 (both MODIS products, source-side catalogue gap)")
a("  rule: forward-fill last valid composite; stale_flag set; rows NOT dropped")
a("  reason_not_dropped: >-")
a("    dropping breaks identical-rows comparability with the frozen comparators")
a("    (M6.md §11 STOP condition).")
for s in nb07["stale_sensitivity"]:
    a(f"  sensitivity_{s['subset'].replace(' ', '_')}: {{n: {s['n']}, AUC: {round(s['AUC'], 4)}, NB: {round(s['NB'], 4)}}}")
a("")
a("inputs:")
a(f"  features_weekly: {sha16(QUAR / 'm6_features_weekly_srilanka_v1.csv')}")
a(f"  rowset: {sha16(QUAR / 'm6_rowset_srilanka_v1.csv')}")
a(f"  label_thresholds: {sha16(QUAR / 'm6_label_thresholds_srilanka_v1.csv')}")
a(f"  implied_thresholds: {sha16(QUAR / 'm6_implied_thresholds_srilanka_v1.csv')}")
a(f"  worldpop_r2025a: {sha16(QUAR / 'm6_worldpop_r2025a_by_district_year.csv')}")
a(f"  comparator_panel: {sha16(REPO / 'ALT_STATS' / 'frozen' / 'srilanka_matched_pairs.csv')}")
a("  comparator_panel_path: ALT_STATS/frozen/srilanka_matched_pairs.csv")
a(f"  comparators_available: {nb07['comparators']['available']}")
a(f"  comparators_absent: {nb07['comparators']['absent']}")
a("")
a("outputs:")
for f in ["m6_predictions_srilanka_v1.csv", "m6_coefficients_srilanka_v1.csv",
          "m6_metrics_srilanka_v1.csv", "m6_bootstrap_ci_srilanka_v1.csv",
          "m6_dca_srilanka_v1.csv"]:
    a(f"  {f}: {sha16(QUAR / f)}")
a("")
a("figures:")
for f in sorted(FIGS.iterdir()):
    a(f"  {f.name}: {sha16(f)}")
a("")
a("headline_result:  # do not restate these numbers from any other artifact")
a("  M6:         {AUC: 0.601, CI: [0.568, 0.638], PR_AUC: 0.442, Brier: 0.223, NB_at_0.30: 0.058, NB_CI: [0.033, 0.085]}")
a("  M5_full:    {AUC: 0.771, CI: [0.741, 0.804], PR_AUC: 0.667, Brier: 0.180, NB_at_0.30: 0.145, NB_CI: [0.106, 0.184]}")
a("  M5_noclim:  {AUC: 0.751, CI: [0.721, 0.782], PR_AUC: 0.652, Brier: 0.191, NB_at_0.30: 0.135, NB_CI: [0.100, 0.176]}")
for v in nb07["verdicts"]:
    a(f"  {v['contrast']}: {{dAUC: '{v['dAUC']}', dNB: '{v['dNB']}'}}")
a("  test_prevalence: 0.3365")
a("  test_events: 1321")
a("")
a("# ---------------------------------------------------------------------------")
a("# PROVENANCE GAPS found while freezing. Both are open items, not PASS.")
a("# ---------------------------------------------------------------------------")
a("provenance_gaps:")
a("  threshold_generator_not_committed:")
a("    severity: blocking_for_reproducibility")
a("    status: BLOCKED  # port attempted 2026-08-07; only half recovers")
a("    detail: >-")
a("      m6_label_thresholds_srilanka_v1.csv defines the model target, but no committed")
a("      code produces it. Notebook 06 only consumes it via THRESHOLDS_CSV; notebook 05")
a("      stopped before constructing a label. The WorldPop year-ratio recovery was run as")
a("      ad-hoc session code and was never written to scripts/ or a notebook. This trips")
a("      instruction_m6.md §25's stop condition on establishing which artifact produced a")
a("      manuscript number, for the target itself.")
a("    port_attempt: scripts/m6_threshold_recovery_v1.py")
a("    recovered: >-")
a("      The feasible-interval solver and the clamp rule reproduce EXACTLY: 26/26 districts")
a("      admit a non-empty interval, all 26 frozen K values lie inside their own interval,")
a("      and all 5 clamped districts sit on the lower bound to within 1e-12.")
a("    not_recovered: >-")
a("      The empirical q75 half does not reproduce: best 10 of 21 districts across")
a("      {2 year bases} x {6 train row-sets} x {5 interpolation modes}. K is an exact")
a("      observed train ratio in 21/21 districts at quantile level 0.733-0.765, so the")
a("      method is confirmed, but K sits at a VARYING rank (187-195 of 255) where a fixed")
a("      quantile rule would give a fixed rank -- the original train row set differed from")
a("      any recoverable here by a few rows. Search halted per §25 rather than continuing")
a("      until a definition matched.")
a("    consequence: >-")
a("      The 19.2% of test rows that are test-informed ARE reproducible; the 80.8% that are")
a("      train-only are NOT. Route A (the original threshold artifact) is now the only")
a("      clean resolution.")
a("  nb05_provenance_stale:")
a("    severity: documentation")
a("    detail: >-")
a("      nb05_provenance.json still records status 'STOPPED at M6.md §11 — thresholds not")
a("      reproducible; label NOT constructed', which predates the recovery. Its rowset")
a("      output hash is still correct and is what notebook 06 consumed.")
a("")
a("target_provenance:  # instruction_m6.md §3 — quantified, see M6_TARGET_PROVENANCE.md")
a(f"  threshold_district_years_total: {len(thr)}")
a(f"  threshold_district_years_clamped: {int(thr.source.str.startswith('clamped').sum())}")
a(f"  districts_with_any_clamp: {int(thr[thr.source.str.startswith('clamped')].geometry_id.nunique())}")
a(f"  districts_clamped: {sorted(thr[thr.source.str.startswith('clamped')].rdhs_name.unique())}")
a(f"  test_rows_on_clamped_threshold: {int(clamped.sum())}")
a(f"  test_rows_on_clamped_threshold_frac: {round(float(clamped.mean()), 4)}")
a(f"  test_events_on_clamped_threshold: {int(j[clamped].outcome.sum())}")
a("  status: EXPLORATORY_RECONSTRUCTED_TARGET  # pending Route A/B recovery")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "M6_CORE_FROZEN_MANIFEST.yaml").write_text("\n".join(L) + "\n")
print("wrote", OUT / "M6_CORE_FROZEN_MANIFEST.yaml")
print(f"test rows on clamped thresholds: {int(clamped.sum())} ({clamped.mean():.2%})")
