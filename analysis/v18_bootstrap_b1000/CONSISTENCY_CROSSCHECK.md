# CONSISTENCY_CROSSCHECK — v18 (B=1000 symmetric-null)

Manuscript `paper1_plos_gph_v18_b1000_final.tex` (40 pp, exit 0, 0 undefined, 0 errors, 0 broken refs).

| Element | Value | Present & consistent |
|---|---|---|
| SL recal matched, conditional | +0.0157 [+0.0066, +0.0257] | abstract, results, table ✓ |
| SL recal matched, **development-inclusive (B=1000)** | **[−0.0002, +0.0302]** (includes 0) | abstract, results, cross-tier, caveat, table (6 loci) ✓ |
| SL raw matched, development-inclusive (B=1000) | [−0.0079, +0.0245] (includes 0) | results, table (2 loci) ✓ |
| Colombia matched, development-inclusive | [−0.0001, +0.0244] (includes 0) | abstract, results, cross-tier, caveat, discussion ✓ |
| Headline | "no exclusion robust across both raw evaluation and model refitting in either setting" | abstract, cross-tier ✓ |

Checks (grep):
- **Stale B=300 interval [+0.0015 to +0.0284]: 0.** Stale raw [−0.0074 to +0.0223]: 0. Any "B=300": 0.
- **"survives model-development" as a positive claim: 0** — the only two `surviv…model-development` hits are the negated correct forms ("did not survive", "does not survive").
- No Sri Lanka "excludes zero" development-inclusive statement survives; every dev-inclusive locus now says includes zero.
- B=1000 stated at the loci reporting the interval (7 mentions).
- Estimand hierarchy intact (M5−M1 "not specification-matched" ×4; post-hoc labels; M4−M1 non-nested). Abstract 422 words (≤500).
- C2 SI disclosure sentence present (S14 Text).

**PASS.**
