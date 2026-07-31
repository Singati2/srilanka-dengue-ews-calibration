# Page-by-page audit — v5 (source: `Dengue (3).pdf`, content-identical to v4; v5 = 21 pp)

Source identification: `~/Downloads/Dengue (3).pdf` (sha256 `32cbb363…`) is a recompile, byte-different (pdfTeX timestamp) but **text-identical** to `manuscript/plos_ntd_revision_v4_full_audit/dengue_ews_plos_ntd_v4.tex` (`94860499…`) with line numbers removed. v5 was created from that source. All numeric corrections transcribed from frozen reports (`numeric_fidelity_check_v5.md`); no recomputation.

Rendered every page at 150–200 dpi (Poppler `pdftoppm`) before and after; grayscale generated. Findings:

| Page/region | v5 status / correction | Spec item |
|---|---|---|
| 1 — title page | Sentence-case title; short title added ("Climate-informed dengue warning beyond surveillance"); authors/affiliations/corresponding email; dedicated title page (`\newpage`); single discreet internal-review box (title page only); light running header; no ORCIDs/second-author email in PDF | §14, §15 |
| 2 — Abstract | "not significant" removed; estimate-and-uncertainty wording; ΔAUC separated from ΔNB CI; horizon flatness scoped to Colombia + Sri Lanka clause; heterogeneity-not-tested retained; no overlap-equals-similarity; **293 words** | §2, §5 |
| 2 — Author Summary | "requires local interpretation" wording; elevated dengue activity / alert week / locally defined threshold; no "outbreak" except official-declaration contrast; **200 words** | §6 |
| 3 — Introduction | benchmark framing; no CI-overlap-as-test; "potentially setting-dependent" hedged (Introduction only) | §3 |
| 4–8 — Methods | "Python DLNM-style cross-basis approximation" (consistency); Colombia Platt-on-validation distinguished from SL rolling recalibration; "confirmatory" removed → "benchmark comparisons"; 26-RDHS coarse-CI caveat added; B=1000/0-failures surfaced; unretained SL targeted-value seed disclosed; OpenDengue coverage level-explicit; SIVIGILA/INS comma-splice fixed | §3, §9, stat-01 |
| 8 — DCA threshold interpretation | **corrected**: each false alert weighted ≈0.429 TP-equivalents; one TP offsets ≈2.33 false alerts; "mathematical implication, not an empirically chosen tolerance"; the 0.43-false-per-true error removed; display equation unnumbered (no lineno collision) | §4 |
| 9 — Table 1 (10-col) | fits within margins; abbreviations defined; "Hybrid models M4--M5 reported separately" now honored (M4 in Table 4) | ic-02 |
| 10 — Figure 1 | pipeline arrows do not cross text (v4 fix holds) | — |
| 10 — line numbers | continuous, in margin, no collision with table/figure | §15 |
| 11 — Table 2 / Figure 2 | Alert-none column normalized to 0.000 (consistent 3-decimal); Figure 2 = representative thresholds (not a continuous curve); 0.34 explained; no "full grid in SI" claim | §13 |
| 11–12 — §3.4 contrasts | Python-DLNM≈R-DLNM, R-DLNM−M1, M5−M1 each with explicit subtraction orientation | §11 |
| 13 — Table 4 | **M4 row added** (AUC 0.764; NB 0.193/0.128/0.087, frozen); renamed "Sri Lanka climate-only, distributed-lag, and hybrid model comparison"; M4−M1 contrast (ΔAUC +0.013 [−0.020,0.046]; ΔNB −0.008 [−0.028,0.013]) added to text | §11 |
| 13 — Table 5 (Colombia) | M0–M5 on common-complete n=13,361; per-model mean-pred/obs omission noted | §9, §10 |
| 14 — Figure 3 | **Panel B zero-based** (alert-none=0 baseline; alert-all 0.107 dashed; exact 3-decimal labels); M0 present in both panels; grayscale hatching | §12 |
| 15 — §3.7 sensitivity | neutral language: "excludes zero", "not the registered primary contrast", "borderline" removed; p*=0.40 reported descriptively; Colombia 75/80/90th "attenuated from +0.0188 to +0.0092"; all CIs retained | §7 |
| 15–16 — cross-setting | Table 6 caption editorial "must not be compared for overlap" replaced with publication prose; estimates+CIs retained | §8 |
| 16–18 — Discussion | benchmark/heterogeneity framing; no significance dichotomization; limitations intact | §2, §3 |
| 18 — Declarations | neutral "Pending author confirmation"; truthful AI-use disclosure retained | §19 |
| 19–20 — References | Vancouver inline (surname+initials, first-six-et-al, NLM abbreviations, doi:); EWARS-csd corrected (Schlesinger M et al.); OpenDengue editorial note removed | §16 |
| 21 — Supporting information | only existing draft files (S1–S6) captioned; S7–S10 explicitly noted as planned/not-provided | §18 |
| whole doc | American English; consistent notation (M5$-$M1, ΔNB, ΔAUC, p*=0.30, h=4, 95% CI); under-/over-predicted consistent; no broken Unicode/soft hyphens; line numbers + double spacing | §21, §15 |

**Layout:** 2 overfull boxes, both < 10 pt (Figure 1 tikz frame and one SI line); 0 overfull ≥ 10 pt; 0 underfull. No clipped text, no line-number collisions, no orphan words, no truncated axes (Figure 3 corrected), no figure/table overflow, no `[?]`, no distracting per-page internal-review footer (moved to title page).
