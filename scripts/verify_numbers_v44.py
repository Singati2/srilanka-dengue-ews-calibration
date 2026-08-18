#!/usr/bin/env python3
"""Cross-check the v44 biomath candidate's numeric claims against analysis outputs.

WHY THIS EXISTS
---------------
`BIOMATH_NUMERIC_CROSSWALK.md` verifies the candidate against the PREVIOUS .tex
("preserved by construction" via byte-for-byte copy). That proves the candidate did not
corrupt v44; it cannot detect an error inherited FROM v44, because it never re-opens the
analysis outputs. Its own legend concedes this: SOURCE_ONLY = "artifact cited but not
independently re-opened here."

This script closes that loop: manuscript claims are literal dicts below (transcribed from
`revised_manuscript_biomath.tex`), outputs are read from disk, and the two are compared at
the precision the manuscript uses.

The outputs are the source of truth. Never edit an output to match the text.

Usage:  python3 scripts/verify_numbers_v44.py
Exit:   0 = all checks pass; 1 = at least one mismatch stands.
"""
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Source-of-truth hierarchy (established before any comparison)
# ---------------------------------------------------------------------------
# AUTHORITATIVE (frozen, checksum-locked, cited in the manuscript):
#   ALT_STATS/results/route_a_primary.csv      proper scores + discrimination, B=5000/10000
#   ALT_STATS/results/calibration_metrics.csv  CITL / slope / ICI / meanp / prev
#   analysis/v18_bootstrap_b1000/SL_devinclusive_B1000.json     SL dev-inclusive, B=1000
#   analysis/geo_effect_decomposition/co_devincl_full_refit_results.json  CO dev-incl, B=1000
#   analysis/path_b_matched_fixed_effects_original_pipeline/run/*.json    CO NB levels/robustness
# SUPERSEDED (kept for provenance, must NOT be used):
#   analysis/v17_devinclusive_finalization/SL_devinclusive_results.json   B=300 pilot
# NOT ON THIS MACHINE (cannot be checked here; flagged as UNTRACEABLE-LOCALLY):
#   90th-percentile matched ablation outputs (analysis/matched_ablation_90pct_v1/ holds
#     only .py, no results)
#   development-inclusive proper-score outputs (analysis/devincl_proper_scores_v1/ holds
#     only .py, no results)
#   S1/S3 ladder tables for M0-M4 (frozen figures "not on this machine" per
#     FINAL_CANONICAL_DECISION.md line 6)

SUPERSEDED = {
    "analysis/v17_devinclusive_finalization/SL_devinclusive_results.json": "B=300 pilot; use v18 B=1000",
}

# ---------------------------------------------------------------------------
# What the manuscript claims  (location, label) -> claimed value
# Transcribed from manuscript_v44_biomath_candidate/revised_manuscript_biomath.tex
# Adding a number to the manuscript means adding it here.
# ---------------------------------------------------------------------------
CLAIMS = {
    # --- S19 Table (line 741-750), recalibrated state -----------------------
    ("S19 Table, SriLanka full climate, NLL", "nll"): 0.5406,
    ("S19 Table, SriLanka full climate, Brier", "brier"): 0.1787,
    ("S19 Table, SriLanka full climate, ICI", "ici"): 0.027,
    ("S19 Table, SriLanka full climate, AUC", "auc"): 0.751,
    ("S19 Table, SriLanka matched no-climate, NLL", "nll"): 0.5613,
    ("S19 Table, SriLanka matched no-climate, Brier", "brier"): 0.1865,
    ("S19 Table, SriLanka matched no-climate, ICI", "ici"): 0.045,
    ("S19 Table, SriLanka matched no-climate, AUC", "auc"): 0.724,
    ("S19 Table, Colombia full climate, NLL", "nll"): 0.6162,
    ("S19 Table, Colombia full climate, Brier", "brier"): 0.2127,
    ("S19 Table, Colombia full climate, ICI", "ici"): 0.109,
    ("S19 Table, Colombia full climate, AUC", "auc"): 0.7255,
    ("S19 Table, Colombia matched no-climate, NLL", "nll"): 0.6251,
    ("S19 Table, Colombia matched no-climate, Brier", "brier"): 0.2169,
    ("S19 Table, Colombia matched no-climate, ICI", "ici"): 0.113,
    ("S19 Table, Colombia matched no-climate, AUC", "auc"): 0.7134,
}

# (setting, state, model) -> row in route_a_primary.csv / calibration_metrics.csv
S19_ROWS = {
    "S19 Table, SriLanka full climate": ("SriLanka", "recal", "full"),
    "S19 Table, SriLanka matched no-climate": ("SriLanka", "recal", "no_climate"),
    "S19 Table, Colombia full climate": ("Colombia", "recal", "full"),
    "S19 Table, Colombia matched no-climate": ("Colombia", "recal", "no_climate"),
}

# --- deltas quoted in prose + S19 delta rows (recomputed, not transcribed) ---
DELTA_CLAIMS = {
    ("S19 Table / Results proper-score, SriLanka", "NLL"): -0.0207,
    ("S19 Table / Results proper-score, SriLanka", "Brier"): -0.0079,
    ("S19 Table / Results proper-score, SriLanka", "AUC"): +0.027,
    ("S19 Table / Results proper-score, Colombia", "NLL"): -0.0089,
    ("S19 Table / Results proper-score, Colombia", "Brier"): -0.0043,
    ("S19 Table / Results proper-score, Colombia", "AUC"): +0.012,
    ("Results proper-score prose (raw state), SriLanka", "NLL_raw"): -0.0256,
    ("Results proper-score prose (raw state), Colombia", "NLL_raw"): -0.0085,
    ("Results proper-score prose (raw state), SriLanka", "Brier_raw"): -0.0107,
    ("Results proper-score prose (raw state), Colombia", "Brier_raw"): -0.0036,
}

# --- Sri Lanka matched ablation, dev-inclusive (Results Q2-SL, Fig caption, headline) ---
SL_DEVINCL_CLAIMS = {
    "Results Q2-SL / headline, SL matched raw, point": (["conditional", "raw_matched"], 0.0087),
    "Results Q2-SL / headline, SL matched recal, point": (["conditional", "recal_matched"], 0.0157),
    "Fig sldca caption, SL matched raw, DI CI lower": (["development_inclusive", "raw_matched", "ci", 0], -0.0079),
    "Fig sldca caption, SL matched raw, DI CI upper": (["development_inclusive", "raw_matched", "ci", 1], 0.0245),
    "Fig sldca caption, SL matched recal, DI CI lower": (["development_inclusive", "recal_matched", "ci", 0], -0.0002),
    "Fig sldca caption, SL matched recal, DI CI upper": (["development_inclusive", "recal_matched", "ci", 1], 0.0302),
}

# --- Colombia matched ablation, dev-inclusive (S17, Results Q2-CO, abstract) ---
CO_DEVINCL_CLAIMS = {
    "S17 / abstract, CO matched, reconstructed point": (["point_estimates", "matched"], 0.0078),
    "S17 / abstract, CO matched, DI CI lower": (["development_inclusive", "matched", "ci", 0], 0.0008),
    "S17 / abstract, CO matched, DI CI upper": (["development_inclusive", "matched", "ci", 1], 0.0209),
    "S17, CO matched, frozen committed point": (["reproduce_gate", "matched_target"], 0.00786),
}

# --- Colombia net-benefit levels and compound contrast (Results Q2-CO, S4) ---
CO_NB_CLAIMS = {
    "Results Q2-CO / S4 Table, CO M1 NB@0.30": (["A3_reporting_delay", "NB_M1_full"], 0.117),
    "Results Q2-CO / S4 Table, CO M5 NB@0.30": (["A3_reporting_delay", "NB_M5"], 0.136),
    "Results Q2-CO line 295, CO compound dNB(M5-M1)": (["A3_reporting_delay", "contrasts", "M5-M1_full"], 0.0188),
}

# --- Colombia discrimination quoted in prose/table (the disputed one) ---
CO_AUC_CLAIMS = {
    "Results Q2-CO line 295 prose, CO M5 AUC": ("A2_dlnm_no_humidity", "M5lin", 0.726),
    "S4-ladder table line 573, CO M5 AUC": ("A2_dlnm_no_humidity", "M5lin", 0.726),
    "Results Q2-CO line 295 prose, CO M1 AUC": ("A2_dlnm_no_humidity", "M1", 0.685),
    "Results Q2-CO line 295 prose, CO M4 AUC": ("A2_dlnm_no_humidity", "M4lin", 0.699),
}

# --- Colombia reporting-delay sensitivity (Results Q6, line 316) ---
CO_DELAY_CLAIMS = {
    "Results Q6 line 316, CO matched @ 3-week delay censor": (
        ["A3_matched_delaycurve", "drop0_1_2", "M5-matched"], 0.0049),
    "Results Q6 line 316, CO matched DLNM cross-basis refit": (
        ["A2_matched_dlnm", "M5dlnm_minus_matched"], 0.0122),
    "Results Q6, CO matched IPW-comparator (unweighted)": (
        ["A3_matched_delaycurve", "full", "M5-matched"], 0.0078),
}

# ---------------------------------------------------------------------------


def load_csv_rows(path):
    with open(REPO / path) as fh:
        return list(csv.DictReader(fh))


def load_json(path):
    with open(REPO / path) as fh:
        return json.load(fh)


def dig(obj, keys):
    for k in keys:
        obj = obj[k]
    return obj


def decimals(claimed):
    """Number of decimal places the manuscript used -- compare at that precision."""
    s = f"{claimed!r}"
    return len(s.split(".")[1]) if "." in s else 0


def round_half_away(x, d):
    """Round half away from zero -- the convention manuscripts use.

    Python's built-in round() is banker's rounding, which would flag a correctly
    rounded -0.00015 -> -0.0002 as a mismatch. Use Decimal so a true half-way case
    resolves the way the author would have written it.
    """
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def check(results, location, label, claimed, actual, source):
    d = decimals(claimed)
    ok = round_half_away(actual, d) == round_half_away(claimed, d)
    results.append({
        "location": location, "label": label, "claimed": claimed,
        "actual": actual, "rounded": round_half_away(actual, d), "ok": ok, "source": source,
    })
    return ok


def main():
    results = []

    # ---- S19 table levels: route_a_primary.csv + calibration_metrics.csv ----
    calib = load_csv_rows("ALT_STATS/results/calibration_metrics.csv")
    calib_idx = {(r["setting"], r["state"], r["model"]): r for r in calib}
    src_c = "ALT_STATS/results/calibration_metrics.csv"

    for (location, field), claimed in CLAIMS.items():
        base = location.rsplit(",", 1)[0]
        key = S19_ROWS[base]
        check(results, location, field, claimed, float(calib_idx[key][field]), src_c)

    # ---- deltas: recomputed from components, never transcribed ----
    route = load_csv_rows("ALT_STATS/results/route_a_primary.csv")
    route_idx = {(r["setting"], r["prediction_state"], r["metric"]): r for r in route}
    src_r = "ALT_STATS/results/route_a_primary.csv"

    for (location, metric), claimed in DELTA_CLAIMS.items():
        setting = "SriLanka" if "SriLanka" in location else "Colombia"
        state = "raw" if metric.endswith("_raw") else "recal"
        m = metric.replace("_raw", "")
        row = route_idx[(setting, state, m)]
        # recompute the delta from its operands rather than reading paired_difference
        delta = float(row["full_model_estimate"]) - float(row["no_climate_estimate"])
        check(results, location, f"delta {metric}", claimed, delta, src_r + " (recomputed)")

    # ---- Sri Lanka development-inclusive ----
    sl = load_json("analysis/v18_bootstrap_b1000/SL_devinclusive_B1000.json")
    src_sl = "analysis/v18_bootstrap_b1000/SL_devinclusive_B1000.json"
    for location, (keys, claimed) in SL_DEVINCL_CLAIMS.items():
        check(results, location, "/".join(map(str, keys)), claimed, dig(sl, keys), src_sl)

    # ---- Colombia development-inclusive ----
    co = load_json("analysis/geo_effect_decomposition/co_devincl_full_refit_results.json")
    src_co = "analysis/geo_effect_decomposition/co_devincl_full_refit_results.json"
    for location, (keys, claimed) in CO_DEVINCL_CLAIMS.items():
        check(results, location, "/".join(map(str, keys)), claimed, dig(co, keys), src_co)

    # ---- Colombia NB levels / compound / delay ----
    rec = load_json("analysis/path_b_matched_fixed_effects_original_pipeline/run/recompute_three_results.json")
    src_rec = "analysis/path_b_matched_fixed_effects_original_pipeline/run/recompute_three_results.json"
    for location, (keys, claimed) in CO_NB_CLAIMS.items():
        check(results, location, "/".join(map(str, keys)), claimed, dig(rec, keys), src_rec)

    for location, (block, model, claimed) in CO_AUC_CLAIMS.items():
        check(results, location, f"AUC {model}", claimed, rec[block]["AUC"][model], src_rec)

    rob = load_json("analysis/path_b_matched_fixed_effects_original_pipeline/run/matched_robustness_results.json")
    src_rob = "analysis/path_b_matched_fixed_effects_original_pipeline/run/matched_robustness_results.json"
    for location, (keys, claimed) in CO_DELAY_CLAIMS.items():
        check(results, location, "/".join(map(str, keys)), claimed, dig(rob, keys), src_rob)

    # ---- report ----
    fails = [r for r in results if not r["ok"]]
    width = max(len(r["location"]) for r in results)
    print(f"{'LOCATION'.ljust(width)}  {'LABEL':<28} {'CLAIMED':>10} {'OUTPUT':>12} {'AT PREC':>9}  OK")
    print("-" * (width + 68))
    for r in results:
        print(f"{r['location'].ljust(width)}  {r['label']:<28} {r['claimed']:>10} "
              f"{r['actual']:>12.6f} {r['rounded']:>9}  {'OK' if r['ok'] else 'MISMATCH'}")

    print(f"\n{len(results)} checks performed, {len(fails)} mismatches.")
    if fails:
        print("\nMISMATCHES (work top to bottom):")
        for r in fails:
            print(f"  - {r['location']}: manuscript says {r['claimed']}, "
                  f"output gives {r['actual']:.6f} (= {r['rounded']} at the reported precision)")
            print(f"      source: {r['source']}")

    print("\nNOT CHECKED HERE (outputs absent from this machine -- not evidence of correctness):")
    for note in ["90th-percentile matched ablation (+0.0034 SL, +0.0081 CO and their intervals)",
                 "development-inclusive proper-score CIs (SL dNLL -0.0403 to +0.0040; CO -0.0224 to -0.0002)",
                 "S1/S3 ladder tables for M0-M4 (SL M4 AUC 0.764, NB levels, M1 slope 1.246)",
                 "rolling-origin median +0.0052 / 75% of 28 departments",
                 "wild-cluster-t and LODO jackknife intervals (S15/S16)"]:
        print(f"  - {note}")

    print("\nNOTE ON THE 'SUPERSEDED' DEFECT CLASS: every file in this checkout carries the")
    print("checkout mtime, so mtime cannot establish whether text predates an output. Use git")
    print("commit dates of the output vs the .tex if that class needs auditing.")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
