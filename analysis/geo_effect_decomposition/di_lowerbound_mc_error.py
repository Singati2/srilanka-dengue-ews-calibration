#!/usr/bin/env python3
"""
Monte-Carlo error of the Colombia development-inclusive lower bound (reviewer D1).

Reads the committed B=1000 full-refit replicate distribution
(co_devincl_full_refit_distribution.csv), reproduces the headline 95% interval as a gate,
then estimates the Monte-Carlo standard error of the 2.5th-percentile endpoint by resampling
the replicate distribution (bootstrap-of-the-bootstrap). No refit, no training data required.
Env: numpy 1.26.4, pandas 2.1.3. Seed 20260612.
"""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260612
x = pd.read_csv(os.path.join(HERE, "co_devincl_full_refit_distribution.csv"))["matched"].values
lo, hi = np.percentile(x, 2.5), np.percentile(x, 97.5)
print(f"replicates: {len(x)}")
print(f"95% interval: [{lo:+.5f}, {hi:+.5f}]  width {hi-lo:.4f}")
assert abs(lo - 0.00075) < 3e-4 and abs(hi - 0.02089) < 3e-4, "GATE FAIL: interval != committed [0.00075, 0.02089]"
print("GATE: reproduces committed [+0.00075, +0.02089]  OK")
rng = np.random.default_rng(SEED); B2 = 5000
los = np.array([np.percentile(rng.choice(x, size=len(x), replace=True), 2.5) for _ in range(B2)])
se = los.std(ddof=1)
print(f"Monte-Carlo SE of 2.5th-pct lower bound (B2={B2}): {se:.5f}")
print(f"lower bound {lo:+.5f} = {lo/se:.2f} MC-SE above zero; frac(resampled lower bound <= 0) = {(los<=0).mean():.4f}")
