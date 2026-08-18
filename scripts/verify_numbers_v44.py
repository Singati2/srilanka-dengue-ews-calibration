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
    ("S19 Table, Colombia full climate, AUC", "auc"): 0.725,
    ("S19 Table, Colombia matched no-climate, NLL", "nll"): 0.6251,
    ("S19 Table, Colombia matched no-climate, Brier", "brier"): 0.2169,
    ("S19 Table, Colombia matched no-climate, ICI", "ici"): 0.113,
    ("S19 Table, Colombia matched no-climate, AUC", "auc"): 0.713,
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
    "Results Q2-CO line 295 prose, CO M5 AUC": ("A2_dlnm_no_humidity", "M5lin", 0.725),
    "S4-ladder table line 573, CO M5 AUC": ("A2_dlnm_no_humidity", "M5lin", 0.725),
    "Results Q2-CO line 295 prose, CO M1 AUC": ("A2_dlnm_no_humidity", "M1", 0.685),
    "Results Q2-CO line 295 prose, CO M4 AUC": ("A2_dlnm_no_humidity", "M4lin", 0.699),
}

# --- Colombia reporting-delay sensitivity (Results Q6, line 316) ---
CO_DELAY_CLAIMS = {
    "Results Q6 line 316, CO matched @ 3-week delay censor": (
        ["A3_matched_delaycurve", "drop0_1_2", "M5-matched"], 0.0049),
    "Results Q6 line 316, CO matched DLNM cross-basis refit": (
        ["A2_matched_dlnm", "M5dlnm_minus_matched"], 0.0122),
    # Line 318 now states both arms as +0.008; the archive spread (0.00786 frozen,
    # 0.00783 reconstructed, 0.007859) straddles the 0.0078/0.0079 boundary, so the
    # claim is checked at 3 dp -- the precision the pipeline can actually resolve.
    "Results Q6, CO matched IPW-comparator (both arms, 3 dp)": (
        ["A3_matched_delaycurve", "full", "M5-matched"], 0.008),
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


# ---------------------------------------------------------------------------
# WP4 / WP5 (Sri Lanka), ported into v44 Results Q7 on 2026-08-17.
#
# These read the WP4/WP5 quarantine tables. Those are gitignored by study policy
# ("code and reports only"), so on a machine without them this whole section
# reports as SKIPPED rather than failing -- absence is not a mismatch.
#
# Everything below is RECOMPUTED from the source table, never transcribed. Two
# aggregation hazards are handled explicitly:
#   * district-week vs district-mean. The same displacement has two legitimate
#     values (t2m A'->B is 0.205 per district-week but 0.171 as a mean of 26
#     district means). The manuscript quotes district-week throughout except
#     where it names a district, so the checks below use the 10,842-row tables
#     and the 26-row table only for per-district claims.
#   * raw vs recalibrated state. The flip analysis is quoted in the RAW state
#     throughout (recal gives 46-83 where raw gives 35-76), except the exact
#     bound, which the text labels as recalibrated. Both are checked as labelled.
# ---------------------------------------------------------------------------

WP45_QUAR = ("data_quarantine/wp5_exposure", "data_quarantine/wp4_cv")


def _rows(rel):
    with open(REPO / rel) as fh:
        return list(csv.DictReader(fh))


def _mean(xs):
    return sum(xs) / len(xs)


def _absdiff(rows, a, b):
    return [abs(float(r[a]) - float(r[b])) for r in rows]


def _spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk
    rx, ry = rank(xs), rank(ys)
    mx, my = _mean(rx), _mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")


def check_wp45(results):
    """Recompute every WP4/WP5 number quoted in Results Q7. Returns n checked."""
    P = _rows("data_quarantine/wp5_exposure/wp5_precip_exposure_twin_srilanka_v1.csv")
    T = _rows("data_quarantine/wp5_exposure/wp5_temp_exposure_twin_srilanka_v1.csv")
    C = _rows("data_quarantine/wp5_exposure/wp5_buildC_temp_exposure_srilanka_v1.csv")
    X = _rows("data_quarantine/wp5_exposure/wp5_exposure_contrast_srilanka_v1.csv")
    E = _rows("data_quarantine/wp5_exposure/wp5_decision_flip_envelope_srilanka_v1.csv")
    S = _rows("data_quarantine/wp5_exposure/wp5_decision_flip_summary_srilanka_v1.csv")
    F = _rows("data_quarantine/wp5_exposure/wp5_f8_modifier_screen_srilanka_v1.csv")
    M = _rows("data_quarantine/wp5_exposure/wp5_miscalibration_structure_srilanka_v1.csv")
    ST = _rows("data_quarantine/wp5_exposure/wp5_04_station_validation_srilanka.csv")
    PW = _rows("data_quarantine/wp4_cv/wp4_power_cost_srilanka_v1.csv")
    FG = _rows("data_quarantine/wp4_cv/wp4_fold_effect_gap_srilanka_v1.csv")
    FM = _rows("data_quarantine/wp4_cv/wp4_fold_effect_metrics_srilanka_v1.csv")
    MI = _rows("data_quarantine/wp4_cv/wp4_morans_i_srilanka_v1.csv")
    n0 = len(results)

    src_p = "data_quarantine/wp5_exposure/wp5_precip_exposure_twin_srilanka_v1.csv"
    src_t = "data_quarantine/wp5_exposure/wp5_temp_exposure_twin_srilanka_v1.csv"
    src_c = "data_quarantine/wp5_exposure/wp5_buildC_temp_exposure_srilanka_v1.csv"
    src_x = "data_quarantine/wp5_exposure/wp5_exposure_contrast_srilanka_v1.csv"
    src_e = "data_quarantine/wp5_exposure/wp5_decision_flip_envelope_srilanka_v1.csv"
    src_s = "data_quarantine/wp5_exposure/wp5_decision_flip_summary_srilanka_v1.csv"
    src_f = "data_quarantine/wp5_exposure/wp5_f8_modifier_screen_srilanka_v1.csv"
    src_w = "data_quarantine/wp4_cv/"

    # ---- cohort sizes -----------------------------------------------------
    for nm, tbl, src in (("precip", P, src_p), ("temp", T, src_t), ("buildC", C, src_c)):
        check(results, f"Methods/Table wp5-ladder, {nm} table rows", "district-weeks",
              10842, len(tbl), src)
    check(results, "Table wp5-flips, held-out panel rows", "district-weeks", 3926, len(E), src_e)
    check(results, "Results Q7, spatial units", "districts", 26, len(X), src_x)

    # ---- Table wp5-ladder: rainfall --------------------------------------
    base = [float(r["precip_sum_mm_a_frac"]) for r in P]
    mask = _absdiff(P, "precip_sum_mm_a_frac", "precip_sum_mm_a_alltouched")
    a2b = _absdiff(P, "precip_sum_mm_b_pop", "precip_sum_mm_a_frac")
    mean_rain = _mean(base)
    check(results, "Table wp5-ladder, rainfall A->A' (mask)", "mean |d| mm", 0.76, _mean(mask), src_p)
    check(results, "Table wp5-ladder, rainfall A->A' (mask)", "% of mean", 1.8,
          100 * _mean(mask) / mean_rain, src_p)
    check(results, "Table wp5-ladder, rainfall A'->B", "mean |d| mm", 3.40, _mean(a2b), src_p)
    check(results, "Table wp5-ladder, rainfall A'->B", "max |d| mm", 72.6, max(a2b), src_p)
    check(results, "Table wp5-ladder, rainfall A'->B", "% of mean", 7.9,
          100 * _mean(a2b) / mean_rain, src_p)
    check(results, "Results Q7 prose, mean weekly rainfall", "mm", 42.9, mean_rain, src_p)

    order = sorted(range(len(P)), key=lambda i: base[i])
    for lab, frac, claim_mm, claim_pct in (("wettest decile", 0.90, 8.56, 5.4),
                                           ("wettest percentile", 0.99, 12.89, 4.9)):
        cut = order[int(len(P) * frac):]
        check(results, f"Table wp5-ladder, rainfall A'->B, {lab}", "mean |d| mm",
              claim_mm, _mean([a2b[i] for i in cut]), src_p)
        check(results, f"Table wp5-ladder, rainfall A'->B, {lab}", "% of mean",
              claim_pct, 100 * _mean([a2b[i] for i in cut]) / _mean([base[i] for i in cut]), src_p)

    # ---- Table wp5-ladder: temperature and humidity -----------------------
    for var, claim_mean, claim_max in (("t2m_mean_c", 0.205, 1.16),
                                       ("t2m_max_c", 0.387, 2.76),
                                       ("t2m_min_c", 0.316, 2.34),
                                       ("rh_mean_percent", 0.77, 6.29)):
        d = _absdiff(T, f"{var}_b_pop", f"{var}_a_frac")
        check(results, f"Table wp5-ladder, {var} A'->B", "mean |d|", claim_mean, _mean(d), src_t)
        check(results, f"Table wp5-ladder, {var} A'->B", "max |d|", claim_max, max(d), src_t)
    dbc = _absdiff(C, "t2m_mean_c_c_pop", "t2m_mean_c_b_pop")
    check(results, "Table wp5-ladder, t2m_mean_c B->C", "mean |d|", 0.306, _mean(dbc), src_c)
    check(results, "Table wp5-ladder, t2m_mean_c B->C", "max |d|", 1.92, max(dbc), src_c)
    check(results, "Table wp5-ladder, B->C orography component", "mean |d| C", 0.223,
          _mean([abs(float(r["temp_b2c_orography_c"])) for r in X]), src_x)
    check(results, "Table wp5-ladder, B->C sub-grid component", "mean |d| C", 0.169,
          _mean([abs(float(r["temp_b2c_subgrid_c"])) for r in X]), src_x)

    # ---- per-district claims (the 26-row table, correctly) ----------------
    by_name = {r["rdhs_name"]: r for r in X}
    for dist, claim in (("Nuwara Eliya", -1.92), ("Badulla", -1.33), ("Ratnapura", 1.01)):
        check(results, f"Results Q7 prose, {dist} B->C", "signed C", claim,
              float(by_name[dist]["temp_b2c_c"]), src_x)
    for dist, claim in (("Colombo", -7.30), ("Puttalam", 4.37)):
        check(results, f"Results Q7 prose, {dist} rainfall A'->B", "signed mm", claim,
              float(by_name[dist]["precip_a2b_mm"]), src_x)
    signed = [float(r["precip_a2b_mm"]) for r in X]
    check(results, "Results Q7 prose, districts drier under weighting", "count", 17,
          sum(1 for v in signed if v < 0), src_x)
    check(results, "Results Q7 prose, districts wetter under weighting", "count", 9,
          sum(1 for v in signed if v > 0), src_x)
    check(results, "Results Q7 prose, rho(|rain|,|temp|) displacement", "Spearman", 0.24,
          _spearman([abs(float(r["precip_a2b_mm"])) for r in X],
                    [abs(float(r["temp_a2b_c"])) for r in X]), src_x)

    # ---- Table wp5-flips (RAW state, as the text specifies) ---------------
    at30 = [r for r in S if abs(float(r["p_star"]) - 0.30) < 1e-9]
    for rung, lo, hi, plo, phi, dnb in (("A'->B", 35, 76, 0.9, 1.9, 0.0013),
                                        ("A'->C", 64, 104, 1.6, 2.6, 0.0009)):
        v = [r for r in at30 if r["rung"] == rung]
        check(results, f"Table wp5-flips, {rung} flips (low)", "count", lo,
              min(int(r["flips_raw"]) for r in v), src_s)
        check(results, f"Table wp5-flips, {rung} flips (high)", "count", hi,
              max(int(r["flips_raw"]) for r in v), src_s)
        check(results, f"Table wp5-flips, {rung} %% of rows (low)", "pct", plo,
              min(float(r["flip_pct_raw"]) for r in v), src_s)
        check(results, f"Table wp5-flips, {rung} %% of rows (high)", "pct", phi,
              max(float(r["flip_pct_raw"]) for r in v), src_s)
        # quoted as "$\\le$", so the claim is that the bound holds, not that it is tight
        obs = max(abs(float(r["dNB_raw"])) for r in v)
        check(results, f"Table wp5-flips, {rung} |dNB| bound holds", "<= claim", dnb,
              obs if obs > dnb else dnb, src_s)
    check(results, "Results Q7 prose, |dNB| across all rungs/specs/thresholds", "abs", 0.0023,
          max(abs(float(r["dNB_recal"])) for r in S), src_s)

    nE = len(E)
    ceil_n = sum(1 for r in E
                 if (float(r["p_full_raw"]) >= 0.30) != (float(r["p_noclim_raw"]) >= 0.30))
    check(results, "Table wp5-flips, climate block removed (ceiling)", "flips", 441, ceil_n, src_e)
    check(results, "Table wp5-flips, climate block removed (ceiling)", "pct", 11.2,
          100 * ceil_n / nE, src_e)
    bnd = sum(1 for r in E if abs(float(r["p_full_recal"]) - 0.30) <= 0.02)
    check(results, "Table wp5-flips, exact bound |p-p*|<=0.02 (recal)", "rows", 253, bnd, src_e)
    check(results, "Table wp5-flips, exact bound |p-p*|<=0.02 (recal)", "pct", 6.4,
          100 * bnd / nE, src_e)
    braw = sum(1 for r in E if abs(float(r["p_full_raw"]) - 0.30) <= 0.02)
    check(results, "Results Q7 prose, exact bound on the raw scale", "pct", 6.0,
          100 * braw / nE, src_e)
    fl = [r for r in E if r["flip_A_to_B_p30"] in ("True", "1")]
    check(results, "Results Q7 prose, A'->B flips added", "count", 67,
          sum(1 for r in fl if float(r["p_A_to_B"]) >= 0.30), src_e)
    check(results, "Results Q7 prose, A'->B flips removed", "count", 9,
          sum(1 for r in fl if float(r["p_A_to_B"]) < 0.30), src_e)
    ev = []
    for p, claim in (("10", 0.088), ("20", 0.160), ("30", 0.289), ("40", 0.431)):
        f_ = [r for r in E if r[f"flip_A_to_B_p{p}"] in ("True", "1")]
        rate = sum(int(r["outcome"]) for r in f_) / len(f_)
        ev.append(rate)
        check(results, f"Results Q7 prose, flipped-row event rate at p*=0.{p}", "rate",
              claim, rate, src_e)
    both = ev + [sum(int(r["outcome"]) for r in g) / len(g) for p in ("10", "20", "30", "40")
                 for g in ([r for r in E if r[f"flip_A_to_C_p{p}"] in ("True", "1")],) if g]
    ts = [0.10, 0.20, 0.30, 0.40] * 2
    mb, mt = _mean(both), _mean(ts)
    r_ = (sum((a - mb) * (b - mt) for a, b in zip(both, ts))
          / ((sum((a - mb) ** 2 for a in both) * sum((b - mt) ** 2 for b in ts)) ** 0.5))
    check(results, "Results Q7 prose, corr(flipped-row event rate, p*)", "Pearson r", 0.96, r_, src_e)

    # ---- F8 modifier screen -----------------------------------------------
    check(results, "Results Q7 prose, modifier screen tests run", "count", 60, len(F), src_f)
    check(results, "Results Q7 prose, associations surviving FDR", "count", 6,
          sum(1 for r in F if r["survives_fdr"] == "True"), src_f)
    fi = {(r["response"], r["modifier"]): r for r in F}
    for resp, mod, claim_rho in (("cal_intercept", "prev", 0.85),
                                 ("cal_slope", "frac_crops", 0.61),
                                 ("cal_slope", "lc_shannon", 0.59),
                                 ("cal_slope", "pop_density_km2", -0.50),
                                 ("flip_AC_pct", "slope_mean", 0.56),
                                 ("flip_AC_pct", "elev_mean", 0.56),
                                 ("flip_AC_pct", "hand_mean", 0.55),
                                 ("dNB_clim", "pop_density_km2", 0.40)):
        k = (resp, mod)
        assert k in fi, f"screen row missing: {k} -- a silently skipped check is untraceable"
        check(results, f"Results Q7 prose, rho({resp} ~ {mod})", "Spearman",
              claim_rho, float(fi[k]["rho"]), src_f)
    for resp, mod, claim_q in (("cal_slope", "frac_crops", 0.031),
                               ("cal_slope", "lc_shannon", 0.032),
                               ("flip_AC_pct", "slope_mean", 0.035),
                               ("flip_AC_pct", "elev_mean", 0.035),
                               ("flip_AC_pct", "hand_mean", 0.038),
                               ("dNB_clim", "pop_density_km2", 0.15)):
        k = (resp, mod)
        assert k in fi, f"screen row missing: {k} -- a silently skipped check is untraceable"
        check(results, f"Results Q7 prose, q({resp} ~ {mod})", "BH q",
              claim_q, float(fi[k]["q"]), src_f)
    sl = [float(r["cal_slope"]) for r in M]
    src_m = "data_quarantine/wp5_exposure/wp5_miscalibration_structure_srilanka_v1.csv"
    check(results, "Results Q7 prose, calibration slope range (min)", "slope", 0.67, min(sl), src_m)
    check(results, "Results Q7 prose, calibration slope range (max)", "slope", 2.23, max(sl), src_m)
    mn = {r["rdhs_name"]: r for r in M}
    for dist, claim in (("Badulla", 9.9), ("Nuwara Eliya", 9.3), ("Ratnapura", 6.0)):
        check(results, f"Results Q7 prose, {dist} exposure flip rate (A'->C)", "pct",
              claim, float(mn[dist]["flip_AC_pct"]), src_m)
    check(results, "Results Q7 prose, rho(elevation, |B->C| displacement)", "Spearman", 0.74,
          _spearman([float(r["elev_mean"]) for r in M], [float(r["abs_b2c"]) for r in M]), src_m)

    # ---- station validation ----------------------------------------------
    src_st = "data_quarantine/wp5_exposure/wp5_04_station_validation_srilanka.csv"
    ne = next(r for r in ST if r["station"] == "Nuwara Eliya")
    check(results, "Results Q7 prose, Nuwara Eliya station elevation", "m", 1880,
          float(ne["z_stn"]), src_st)
    check(results, "Results Q7 prose, Nuwara Eliya station observed", "C", 16.40,
          float(ne["stn_C"]), src_st)
    check(results, "Results Q7 prose, Nuwara Eliya ERA5", "C", 21.17, float(ne["era5_C"]), src_st)
    check(results, "Results Q7 prose, Nuwara Eliya bias", "C", 4.77, float(ne["bias_C"]), src_st)
    check(results, "Methods sec:methods-wp5, ERA5 orography peak", "m", 1219,
          max(float(r["z_orog"]) for r in ST), src_st)

    # ---- WP4: power table -------------------------------------------------
    pw = {r["buffer"]: r for r in PW}
    for buf, med, worst, uw, deg in (("km_0", 21, 16, 5481, 0), ("km_25", 19, 14, 4959, 0),
                                     ("km_50", 15, 10, 4045, 0), ("km_75", 12, 6, 3132, 0),
                                     ("km_100", 9, 5, 2349, 0), ("km_150", 5, 0, 1435, 12)):
        r = pw[buf]
        check(results, f"Table wp4-power, {buf} median train units", "count", med,
              float(r["train_units_median"]), src_w + "wp4_power_cost_srilanka_v1.csv")
        check(results, f"Table wp4-power, {buf} worst fold", "count", worst,
              float(r["train_units_min"]), src_w + "wp4_power_cost_srilanka_v1.csv")
        check(results, f"Table wp4-power, {buf} median train district-weeks", "count", uw,
              float(r["train_unitweeks_median"]), src_w + "wp4_power_cost_srilanka_v1.csv")
        check(results, f"Table wp4-power, {buf} degenerate folds", "count", deg,
              float(r["degenerate_folds"]), src_w + "wp4_power_cost_srilanka_v1.csv")
    check(results, "Results Q7 prose, retained district-weeks at 0 km", "pct", 84,
          float(pw["km_0"]["retained_pct"]), src_w + "wp4_power_cost_srilanka_v1.csv")
    check(results, "Results Q7 prose, retained district-weeks at 100 km", "pct", 36,
          float(pw["km_100"]["retained_pct"]), src_w + "wp4_power_cost_srilanka_v1.csv")

    # ---- WP4: fold table --------------------------------------------------
    fg = {r["buffer"]: r for r in FG}
    src_fg = src_w + "wp4_fold_effect_gap_srilanka_v1.csv"
    for buf, units, auc, ctrl in (("km_0", 21, 0.565, 0.587), ("km_25", 19, 0.571, 0.590),
                                  ("km_50", 15, 0.558, 0.577), ("km_75", 12, 0.516, 0.578),
                                  ("km_100", 9, 0.502, 0.573)):
        r = fg[buf]
        check(results, f"Table wp4-fold, {buf} train units", "count", units,
              float(r["train_units"]), src_fg)
        check(results, f"Table wp4-fold, {buf} buffered AUC", "AUC", auc,
              float(r["auc_buffered"]), src_fg)
        check(results, f"Table wp4-fold, {buf} matched control", "AUC", ctrl,
              float(r["auc_control_mean"]), src_fg)

    # The "Gap [95% CI]" column is NOT self-consistent in its sourcing. At 0, 75
    # and 100 km it quotes the cluster-bootstrap point estimate; at 25 and 50 km
    # no bootstrap was recorded, so it quotes buffered-minus-control directly.
    # Checked here against the direct gap, which is the quantity the neighbouring
    # two columns imply -- a reader subtracting them gets this, not the bootstrap.
    for buf, gap in (("km_0", -0.022), ("km_25", -0.018), ("km_50", -0.019),
                     ("km_75", -0.061), ("km_100", -0.070)):
        check(results, f"Table wp4-fold, {buf} gap (vs buffered-minus-control)", "dAUC",
              gap, float(fg[buf]["auc_gap"]), src_fg)
    fm = {r["arm"]: r for r in FM}
    src_fm = src_w + "wp4_fold_effect_metrics_srilanka_v1.csv"
    for arm, claim in (("0 temporal (frozen M6)", 0.601),):
        if arm in fm:
            check(results, "Results Q7 prose, temporal-split AUC", "AUC", claim,
                  float(fm[arm]["AUC"]), src_fm)
            check(results, "Results Q7 prose, temporal-split calibration slope", "slope", 0.875,
                  float(fm[arm]["cal_slope"]), src_fm)
    adj = [r for r in MI if r["band_km"] == "adjacent" and r["model"].startswith("M6")]
    if adj:
        check(results, "Results Q7 prose, M6 adjacency Moran's I", "I", 0.001,
              float(adj[0]["I"]), src_w + "wp4_morans_i_srilanka_v1.csv")
        check(results, "Results Q7 prose, M6 adjacency permutation p", "p", 0.99,
              float(adj[0]["p_perm"]), src_w + "wp4_morans_i_srilanka_v1.csv")
    ps = [float(r["p_perm"]) for r in MI]
    check(results, "Results Q7 prose, Moran's I permutation p (min)", "p", 0.53, min(ps),
          src_w + "wp4_morans_i_srilanka_v1.csv")
    check(results, "Results Q7 prose, Moran's I permutation p (max)", "p", 0.99, max(ps),
          src_w + "wp4_morans_i_srilanka_v1.csv")

    return len(results) - n0


def main():
    results = []
    wp45_n, wp45_skipped = 0, False

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
    # ---- WP4/WP5 (Sri Lanka), ported into Results Q7 on 2026-08-17 ----
    if all((REPO / d).is_dir() for d in WP45_QUAR):
        wp45_n = check_wp45(results)
    else:
        wp45_skipped = True

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

    if wp45_skipped:
        print("\n  WP4/WP5 (Results Q7): SKIPPED -- the quarantine tables are gitignored by")
        print("  study policy and are not on this machine. None of its ~130 numbers were checked.")
    else:
        print(f"\n  WP4/WP5 (Results Q7): {wp45_n} numbers recomputed from the quarantine tables.")
        for note in [
            "population-product district-week displacements (Table wp5-product, the "
            "R2025A/GHS-POP columns). The local product table is PER-DISTRICT (t2m 0.0070) "
            "and the manuscript quotes PER-DISTRICT-WEEK (0.0088); the district-week product "
            "table is not on this machine. Checking one against the other would be wrong, not lax.",
            "every cluster-bootstrap interval (wp5-flips CIs, wp4-fold CIs) -- these live in "
            "notebook cell outputs, not in a table this script can read",
            "grid attenuation 65.3%/91.7% and effective cells 21.3/11.8 -> 5.3/3.6 (wp5_02 §3)",
            "transfer-coefficient spread 2.3x and R^2 0.27-0.38 (wp5_05 §6)",
            "station lapse rates 6.40 / 6.31 C/km and the Nuwara Eliya interpolation "
            "19.82 / 21.89 / 19.98 (wp5_04 §10-11)",
            "partial correlations adjusting for alert prevalence (wp5_07 §5a-b)",
            "1,456 model fits, the 8.6e-15 reproduce gate, and the 19.2% exploratory-target "
            "caveat (wp4_02 §2-8)",
        ]:
            print(f"    - not checked: {note}")

    print("\nNOTE ON THE 'SUPERSEDED' DEFECT CLASS: every file in this checkout carries the")
    print("checkout mtime, so mtime cannot establish whether text predates an output. Use git")
    print("commit dates of the output vs the .tex if that class needs auditing.")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
