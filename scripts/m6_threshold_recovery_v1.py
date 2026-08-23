"""Port of the M6 label-threshold recovery (instruction_m6.md §25 fix attempt).

STATUS: PARTIAL. Read this before using it.

The threshold table `m6_label_thresholds_srilanka_v1.csv` defines the M6 target but was
produced by ad-hoc session code that was never committed. This script reconstructs that
procedure from the method recorded in docs/study_decision_log.md (2026-08-07 b) and checks
it against the frozen table.

Result of that check:

  * The FEASIBLE-INTERVAL SOLVER reproduces exactly.  26/26 districts get a non-empty
    interval, and for all 5 clamped districts K equals the interval's lower bound to
    within 1e-12.  The clamped district-years -- the 19.2% of test rows that are
    test-informed -- are therefore fully reproducible.

  * The EMPIRICAL q75 HALF DOES NOT reproduce.  K is an exact observed train ratio in
    21/21 districts, at quantile level 0.733-0.765, so the method is confirmed to be
    "empirical ~75th percentile of train cases/WorldPop".  But no combination of
    {year basis} x {6 train row-set definitions} x {5 interpolation modes} reproduces
    more than 10 of the 21 values.  K sits at a VARYING rank (187-195 of 255) where a
    fixed quantile rule on this series would give a fixed rank -- consistent with the
    original code having used a train row set that differs from any recoverable here by
    a few rows.

Per instruction_m6.md §25 this is reported BLOCKED rather than resolved by further search.
Searching definitions until one matches is the failure mode that instruction warns against.

This script therefore VERIFIES and does NOT emit a thresholds table. The frozen CSV
remains the single source of the target. Nothing here may overwrite it.
"""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path("/Users/mpcr/aj/Dengue/srilanka-dengue-ews-calibration")
QUAR = REPO / "data_quarantine" / "m6_geomatics"
FROZEN_THRESHOLDS_SHA16 = "9746e68bcf89d4a3"
HORIZON_DAYS = 28


def load():
    rowset = pd.read_csv(QUAR / "m6_rowset_srilanka_v1.csv", parse_dates=["week_start"])
    wp = (pd.read_csv(QUAR / "m6_worldpop_r2025a_by_district_year.csv")
          .rename(columns={"Unnamed: 0": "geometry_id"})
          .melt("geometry_id", var_name="year", value_name="wp"))
    wp["year"] = wp.year.astype(int)
    frozen = pd.read_csv(QUAR / "m6_label_thresholds_srilanka_v1.csv")
    pairs = (pd.read_csv(REPO / "ALT_STATS" / "frozen" / "srilanka_matched_pairs.csv",
                         parse_dates=["predictor_week"])
             .rename(columns={"spatial_unit_id": "geometry_id",
                              "predictor_week": "week_start"}))
    return rowset, wp, frozen, pairs


def build_ratios(rowset, wp):
    """cases 4 weeks ahead, divided by the target year's population.

    The threshold is a fixed INCIDENCE, so in count space it scales with population:
    thr_count(d, y) = K(d) * WP(d, y). K is that incidence.
    """
    d = rowset.copy()
    d["target_year"] = (d.week_start + pd.Timedelta(days=HORIZON_DAYS)).dt.year
    d = d.merge(wp, left_on=["geometry_id", "target_year"],
                right_on=["geometry_id", "year"], how="left")
    d["ratio"] = d.cases_future / d.wp
    return d


def feasible_intervals(ratios, pairs):
    """Solve the frozen TEST outcomes for each district's admissible K.

    label = 1 iff cases_future > K * WP, so per test row:
        outcome == 1  =>  K <  cases/WP
        outcome == 0  =>  K >= cases/WP
    giving K in [max over 0-rows, min over 1-rows).

    This is the step that uses test labels, and is the whole of
    instruction_m6.md §3's concern.
    """
    te = ratios.merge(pairs[["geometry_id", "week_start", "outcome"]],
                      on=["geometry_id", "week_start"], how="inner").dropna(subset=["ratio"])
    lo = te[te.outcome == 0].groupby("geometry_id").ratio.max()
    hi = te[te.outcome == 1].groupby("geometry_id").ratio.min()
    return pd.DataFrame({"lo": lo, "hi": hi}).dropna()


def empirical_q75(ratios, interpolation="higher"):
    """Best-known reconstruction of the train-only quantile. NOT exact -- see module docstring."""
    tr = ratios[(ratios.split == "train") & ratios.ratio.notna()]
    return tr.groupby("geometry_id").ratio.quantile(0.75, interpolation=interpolation)


def main():
    rowset, wp, frozen, pairs = load()

    have = hashlib.sha256((QUAR / "m6_label_thresholds_srilanka_v1.csv").read_bytes()).hexdigest()[:16]
    assert have == FROZEN_THRESHOLDS_SHA16, f"frozen thresholds changed: {have}"

    ratios = build_ratios(rowset, wp)
    iv = feasible_intervals(ratios, pairs)
    K = frozen.groupby("geometry_id").agg(K=("K", "first"), source=("source", "first"))
    K = K.join(iv)

    # ---- CHECK 1: every district admits a non-empty interval -------------------
    nonempty = int((K.lo < K.hi).sum())
    print(f"[1] non-empty feasible interval: {nonempty}/{len(K)} districts")
    assert nonempty == len(K), "a district has no admissible K -- the label rule is wrong"

    # ---- CHECK 2: every frozen K lies inside its own interval ------------------
    inside = ((K.K >= K.lo) & (K.K < K.hi))
    print(f"[2] frozen K inside its interval: {int(inside.sum())}/{len(K)} districts")
    assert inside.all(), "a frozen K is outside the interval its own labels imply"

    # ---- CHECK 3: clamped districts sit exactly on the lower bound -------------
    cl = K[K.source.str.startswith("clamped")]
    exact = int(np.isclose(cl.K, cl.lo, rtol=1e-12).sum())
    print(f"[3] clamped K == interval lower bound: {exact}/{len(cl)} districts  "
          f"({sorted(cl.index)})")
    assert exact == len(cl), "the clamp rule does not reproduce"

    # ---- CHECK 4: the empirical half, reported honestly ------------------------
    emp = K[K.source == "empirical q75"]
    q = empirical_q75(ratios).reindex(emp.index)
    match = int(np.isclose(q, emp.K, rtol=1e-9).sum())
    print(f"[4] empirical q75 reproduced: {match}/{len(emp)} districts  "
          f"-- BLOCKED, see module docstring")

    # characterisation: K is an observed train value, at a varying rank
    tr = ratios[(ratios.split == "train") & ratios.ratio.notna()]
    levels, is_obs = [], 0
    for gid, k in emp.K.items():
        v = np.sort(tr[tr.geometry_id == gid].ratio.values)
        if np.any(np.isclose(v, k, rtol=1e-12)):
            is_obs += 1
        levels.append(float((v < k).mean()))
    print(f"    K is an exact observed train ratio in {is_obs}/{len(emp)} districts")
    print(f"    at quantile level {min(levels):.3f}-{max(levels):.3f} (median {np.median(levels):.3f})")

    print("\nSTATUS: interval solver + clamp rule RECOVERED; empirical q75 BLOCKED.")
    print("The frozen thresholds CSV remains the sole source of the target; "
          "this script writes nothing.")


if __name__ == "__main__":
    main()
