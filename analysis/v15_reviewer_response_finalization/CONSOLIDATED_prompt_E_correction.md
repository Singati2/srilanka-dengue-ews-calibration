# Task 6 — Correction to §E of `claude_prompt_dengue_finalize_CONSOLIDATED.md`

The consolidated prompt file lives in `~/Downloads/` (not in the repo), so it is corrected here (and the Downloads copy is patched in place).

## INCORRECT §E line (must not ship)
> **SL matched, past-only rolling recalibration:** ≈ +0.015, 95% CI [+0.006, +0.025] (excludes zero) — inference is recalibration-dependent.

That +0.015 [+0.006, +0.025] is **recal(M5) − recal(M1)**, the *unmatched* frozen contrast — not the matched estimand.

## CORRECTED §E lines
> - **SL matched, raw @ p*=0.30:** ΔNB(M5 − M5_no-climate) = **+0.0087**, 95% CI **[−0.0015, +0.0188]** (includes zero).
> - **SL matched, past-only rolling-52 recalibration:** recal(M5) − recal(M5_no-climate) = **+0.0157**, 95% CI **[+0.0066, +0.0257]** (excludes zero) — computed by applying the identical past-only recalibration to the independently refit no-climate comparator; inference is recalibration-dependent.
> - **SL frozen M5 − M1, recalibrated (operational sensitivity, NOT matched):** +0.0154, 95% CI [+0.0064, +0.0255] — report only as a frozen-pipeline sensitivity; never as "the matched increment" and never in a cross-country magnitude comparison.

Also correct any §C/§E prose that reads "+0.015 matched" or "the matched increment … +0.015" → "+0.0157 recalibrated matched (M5 − M5_no-climate)".
