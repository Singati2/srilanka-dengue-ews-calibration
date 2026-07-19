# Task 1 — Provenance of the design-lock spec

## Endpoints (commands run, outputs pasted)

**Spec side — introduction of `docs/hybrid_model_extension_spec.md` and its L17:**
```
$ git log --diff-filter=A --format='%H | an=%an ae=%ae | ad=%ad | cd=%cd' --date=iso -- docs/hybrid_model_extension_spec.md
1d8e268 | an=Ganesh Shiwakoti ae=ganshiwakoti@gmail.com | ad=2026-06-14 13:24:14 -0400 | cd=2026-06-14 13:24:14 -0400
$ git log -L 17,17:docs/hybrid_model_extension_spec.md            # single entry ⇒ L17 never edited since introduction
1d8e268 ... 17) - **M1 — recent-cases AR baseline:** ... (incidence lags t, t−1, t−2, t−4 + harmonics + RDHS FE) ...
$ git blame -L 17,17 --date=iso -- docs/hybrid_model_extension_spec.md
1d8e268 (Ganesh Shiwakoti 2026-06-14 13:24:14 -0400 17) - **M1 — recent-cases AR baseline:** ... + harmonics + RDHS FE ...
```
L17 was introduced fully formed by `1d8e268` on **2026-06-14 13:24:14** and has never been edited (the `-L` line history has exactly one entry).

Colombia spec L35 (cases-only M1) introduced by `37221a63`, 2026-06-18 14:59:04 — a separate, later, deliberately different baseline.

**Results side — the frozen SL predictions are NOT in git.** `git ls-files data_quarantine/…hybrid_model_extension_v1/` → 0 tracked files. The artifacts live outside the repo tree in `/home/mpcrlab/data_quarantine/…` and were never committed (the spec's own report states they are "quarantined and git-ignored"). Git can therefore only order the spec against the **results-report** commit, which IS in git:
```
$ git show -s --format='%H | ad=%ad | cd=%cd' 02f986e
02f986e | ad=2026-06-14 14:33:47 -0400 | cd=2026-06-14 14:33:47 -0400   (adds docs/hybrid_model_extension_report.md)
```

## 1b. DAG ancestry (survives date rewriting)
```
$ git merge-base --is-ancestor 1d8e268 02f986e ; echo $?   -> 0   (spec precedes results-report in the DAG)
$ git rev-list --count 1d8e268..02f986e                    -> 1
$ git merge-base --is-ancestor 1d8e268 HEAD ; echo $?       -> 0
$ git branch --contains 1d8e268                            -> * main
```
Spec `1d8e268` is a DAG ancestor of the results-report commit and of HEAD, on `main`. Ordering holds structurally, independent of dates.

## 1c. History-rewrite fingerprint (trust check)
- This is the **original working repo** (`.git` present; `git reflog` returns 87 entries spanning 2026-06-11 → 2026-07-07 with coherent checkout/commit/reset operations) — not a fresh clone, so reflog is informative.
- ad vs cd divergence: **1 of 83 commits** has `ad != cd`. No mass committer-date reset. The three commits around the spec all have `ad == cd`:
  `00111b2 13:14:43`, `1d8e268 13:24:14` (spec), `02f986e 14:33:47` (report).
- No mass-cd collision: the largest committer-date cluster is 3 commits — normal small batching, not a `filter-branch` fingerprint.
- Root-import check: `git log --oneline --reverse | head` shows an ordinary init (`Initial commit` → `Initialize … repository` → merge), not a single bulk import of docs+results. `docs/` and the results were NOT added in one squashed commit.

⇒ History was **not** rewritten in a way that could reorder or back-date the spec.

## 1d. External corroboration (independent of git)
Filesystem mtimes form a coherent, monotonic sequence that matches the commit order and is not settable by any git operation:
```
2026-06-14 13:15:29  docs/hybrid_model_extension_spec.md          (written; committed 13:24)
2026-06-14 13:31:11  …/_run_hybrid_model_extension.py             (the run script)
2026-06-14 13:32:22  …/hybrid_model_predictions_v1.csv            (frozen predictions GENERATED)
2026-06-14 13:34:14  docs/hybrid_model_extension_report.md        (written; committed 14:33)
```
The spec was written (13:15) and committed (13:24) **before** the frozen prediction CSV was generated (13:32). The committed report `02f986e` states verbatim: *"Executed per the locked spec (`docs/hybrid_model_extension_spec.md`, commit 1d8e268) … input checksums re-verified; exact row match."* — a contemporaneous, hash-pinned cross-reference that the results were produced **against** the spec, not the spec rationalized against results.

## 1e. Provenance verdict: **PROVENANCE-CONFIRMED**
Spec L17 predates the frozen SL results by (i) DAG ancestry on `main`, (ii) absence of any rewrite fingerprint in the original repo's history and reflog, and (iii) filesystem mtimes and a hash-pinned contemporaneous report that independently corroborate spec-before-results. The design-locked, structured Sri Lanka M1 (and the M4-primary / M5-sensitivity ladder) is defensibly pre-specified for the **spec-defined ladder**.

### Scope limit (harsh-reviewer caveat, carried to the verdict)
CONFIRMED covers the *spec-defined ladder and the structured M1*. It does **not** cover the specific interpretable estimand now featured, **M5 − M5_no-climate**: `M5_no-climate` is absent from the frozen pipeline (frozen columns are only `p_M1, p_M4_hybrid, p_M5_hybrid_season_RDHS`) and the spec designates M5 as "a sensitivity, not the primary" and never names a no-climate matched model. That matched contrast is a **revision-stage, post-hoc analytic decomposition** — valid (Task 2) but not pre-specified. Pre-specified ladder ≠ pre-specified matched estimand.
