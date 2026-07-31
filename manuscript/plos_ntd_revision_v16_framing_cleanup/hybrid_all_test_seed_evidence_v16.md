# All-test Sri Lanka hybrid bootstrap seed — evidence (v16)

Purpose: independently trace the RDHS-cluster bootstrap seed for the **all-test** Sri Lanka hybrid contrasts ΔNB/ΔAUC(M4−M1) and (M5−M1). This is a separate question from the targeted-value regime seed. Per the audit rules, S6 is **not** used as evidence, and the targeted-value seed is **not** assumed to apply here; the seed is traced from the hybrid workflow's own frozen artifacts. No analysis was recomputed; only scripts/metadata/CSV headers were read.

## Workflow
Sri Lanka hybrid model extension (M4 planned primary; M5 expanded sensitivity), all-test RDHS-cluster bootstrap for ΔAUC and ΔNB of M4 and M5 versus M1.

## Artifacts inspected (frozen, read-only)
- **Exact runner script:** `~/data_quarantine/model_pilots/hybrid_model_extension_v1/_run_hybrid_model_extension.py`
  - Line 13: `SEED=20260612; CGRID=[0.1,1.0,10.0]`
  - Line 129: `rng=np.random.default_rng(SEED); B=1000`
  - Lines 126–143: `# ---- RDHS cluster bootstrap: ΔAUC / ΔNB(M4,M5 vs M1) ----` producing the M4−M1 and M5−M1 contrast CIs.
- **Exact metadata file:** `~/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model.meta.md`
  - Line 7: "RDHS-cluster bootstrap (seed 20260612, B=1000, 0 failures) for ΔAUC/ΔNB vs M1."
- **Exact result file (CI output):** `~/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_ci_v1.csv` (meta-recorded sha256 `e441f059905e7813a97860bae9d5ca921fd1a4a4e09a01979459aa3a066e3e59`). Contents match the manuscript's reported intervals:
  - `M4_hybrid-M1, dNB30, -0.00826, -0.0278, 0.01277` → manuscript M4−M1 −0.008 [−0.028, +0.013].
  - `M5_hybrid_season_RDHS-M1, dNB30, 0.00808, -0.00135, 0.01845` → manuscript M5−M1 +0.0081 [−0.0012, +0.0181].
- **Diagnostics file:** `hybrid_model_diagnostics_v1.csv` — records model/C/feature diagnostics but has **no** seed column (the seed is recorded in the runner script and meta.md, not the diagnostics CSV).

## Parameters
- B = 1000 (runner line 129; meta.md line 7; every row of `hybrid_model_ci_v1.csv` shows B=1000, failures=0).
- Seed = 20260612 (runner line 13; meta.md line 7).
- Source line/key: `_run_hybrid_model_extension.py:13` (`SEED=20260612`) and `:129` (`np.random.default_rng(SEED); B=1000`); `hybrid_model.meta.md:7`.

## Conclusion
The all-test Sri Lanka hybrid-bootstrap seed **is independently verified as 20260612 (B=1000, 0 failures)** from the hybrid runner script and metadata, and the corresponding output CI file reproduces the manuscript's M4−M1 and M5−M1 intervals. This is confirmed independently of the targeted-value run and independently of S6.

Note: both the all-test hybrid run and the targeted-value Stage 1A run used the same numeric seed (20260612), but each was verified from its own artifacts; the equality was observed, not assumed. S6 row 1 has been corrected to cite these direct sources.
