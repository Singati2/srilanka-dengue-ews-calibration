# Path B — Reproduction Check (Gate A)
Original pipeline rerun (exact script logic, same input sha256 `bfb2a536…`, seed 20260612, B=1000).
- Frozen target: ΔNB(M5−M1)@0.30 = +0.018775; bootstrap 95% CI [+0.0117, +0.0260]; ΔAUC +0.04029.
- Reproduced: ΔNB(M5−M1) = **+0.01878** (|Δ|=5e-6 ≤ 0.001 tolerance) → **GATE A PASS**; CI **[+0.0117, +0.0260]**; ΔAUC +0.0403; 0 bootstrap failures; test prevalence 0.3753; row counts train 53,711/val 12,713/test 13,361 (guarded).
- Interpretation of the matched contrast is therefore authorized.
