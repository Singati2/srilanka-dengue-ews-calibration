# SOURCE_MANUSCRIPT_RESOLUTION

*Written for the v44 biomath gap-analysis / decision-theoretic reframe task. Read-only investigation; no source modified.*

## 1. Canonical manuscript path
`manuscript_v44/revised_manuscript.tex`

## 2. Branch
`agent/v44-round4-geomatics-execution` (the most recently advanced v44 branch; commit dated 2026-08-07).

## 3. Commit SHA
`4b3287ccf11538cf5e54ce3b81dd4c9fbd2fafb6` — *"v44 R4 Phase A: branch reconciliation + submission-readiness semantics + shallow-PASS downgrades"* (2026-08-07).

## 4. Manuscript SHA256
- `manuscript_v44/revised_manuscript.tex` → `08fad12b9188b98faa7566d21769ac71fc3356248afeff91868cebfb07e46915` (632 lines)
- (git blob id `cb53a6efa806d734a771e14ccc1e975b1da001c1`)

Companion / historical, hashed for preservation:
- `manuscript_v43/revised_manuscript.tex` → `60fa9b3632ad5c0db3bad45810147477cdbacaeb927be1af14d332c787651f42` (632 lines; blob `d2f29739…`)
- `manuscript/dengue_ews_manuscript.tex` → `a521e8506bb5f81857f8ae0b979af9df4c527bc990a3d62548f7b11d0a59eadf` (1220 lines; blob `049e19be…`)

## 5. Why it is canonical
Three coexisting manuscript files exist on this branch. Their contents disambiguate which is current:

| File | Lines | Title | Matched ablation? | Proper scores (NLL)? | Dev-inclusive uncertainty? |
|---|---|---|---|---|---|
| `manuscript_v44/revised_manuscript.tex` | 632 | "Exploratory matched-comparator evaluation of climate information for short-lead dengue elevated-activity forecasting" | **yes** | **yes** | **yes** |
| `manuscript_v43/revised_manuscript.tex` | 632 | (same body) | yes | yes | (gated, *not* computed) |
| `manuscript/dengue_ews_manuscript.tex` | 1220 | "Benchmarking Climate-Informed Dengue Early Warning Against Recent Surveillance…" | no | no | no |

- `manuscript_v44/README.txt` states verbatim: *"manuscript_v44 — DRAFT. Copy of manuscript_v43 with ONE change: the Methods proper-score 'gated and not computed' clause corrected to reflect that development-inclusive proper-score intervals were computed (analysis/devincl_proper_scores_v1). v43 is preserved as historical evidence. Geomatics (M6/WP4/WP5) integration + experimental reframe are PENDING — not final."*
- `manuscript_v43/README.txt` states it is the *"CURRENT, v40, 2026-07-23"* Overleaf bundle, title *"Matched-comparator evaluation of climate information in short-lead dengue elevated-activity forecasting."* v43/v44 carry the current deflationary matched-comparator science.
- `manuscript/dengue_ews_manuscript.tex` (1220 lines) is the older *"Benchmarking…"* lineage. It is byte-identical across `main`, `manuscript-v43-repair`, and all `agent/v44-*` branches (blob `049e19be`), contains **zero** occurrences of matched-ablation, proper-score/NLL, information-set, or development-inclusive content, and is superseded by the v43/v44 matched-comparator draft. It is retained as the archival top-level manuscript plus its `plos_ntd_revision_v1…v18/` history (which is where the earlier v16/v17 exact-wording lineage lives — the same v17 mistakenly treated as current in the prior session).

The exact v43→v44 change is a single Methods sentence (verified by `diff`): v43 says development-inclusive proper-score intervals were *"gated and not computed"*; v44 says they *were* subsequently computed (`analysis/devincl_proper_scores_v1`) and reports them. All numbers are otherwise identical. **v44 is the current draft; v43 is its immediate predecessor preserved as evidence.**

## 6. Relationship to v43
v44 = v43 + one corrected Methods clause (proper-score dev-inclusive intervals now computed and reported). Numerically identical otherwise. v43 preserved unchanged as historical evidence.

## 7. Relationship to v44 (internal metadata note)
The file's own header comment reads *"Version 25 (submission closeout). PLOS Global Public Health candidate."* The directory/README versioning ("v43"/"v44") is the repository's manuscript-lineage counter; the in-file "Version 25/V27" strings are an internal editing counter. These are **not** contradictory — they count different things — but the directory/README lineage (v44) is the authoritative external label. Target venue per header: **PLOS Global Public Health**.

## 8. Relationship to the separate M6 branch
The executed geomatics work (M6 geomatics-only model, WP4 spatial-CV scaffolding, WP5 Build-B weight field) lives on `m6-geomatics-notebooks` (commit `ff6287d`, 2026-08-07) and follow-up instructions on `agent/instruction-m6-next-actions` (`8de3018`). These are **not** merged into the canonical manuscript.

## 9. Are M6/WP4/WP5 actually integrated? — NO
Direct token scan of `manuscript_v44/revised_manuscript.tex`:
- `M6` = 0 · `WP4` = 0 · `WP5` = 0 · `geomatic` = 1 (author affiliation only: "Geomatics Engineering") · `SPI`/`MODIS`/`remotely sensed` = 0.

The canonical manuscript contains **no geomatics results**. M6/WP4/WP5 are a separate, pending workstream. Per the task firewall (§23) their numbers must **not** be imported into the biomath candidate.

## 10. Unresolved lineage ambiguity
- **Three coexisting lineages** remain in the tree (project memory: PLOS NTD v8/v9, PLOS GPH v14, v43/v44), plus 14 agent branches. The v44 matched-comparator draft is unambiguously the newest *scientific* line, but the repository has not been pruned to a single canonical file, and `main` still ships the older 1220-line `manuscript/dengue_ews_manuscript.tex` + the outdated README (which still describes "WP1 planning"). This is repository hygiene, not a scientific ambiguity, but it means "canonical" here is asserted from **content + READMEs + recency**, not from a single-source-of-truth tag.
- A Jul-17 PDF (`~/Downloads/Dengue_Project-8.pdf`, title "Does climate information add decision value…? A matched climate ablation study") is a compiled artifact of this same matched-ablation lineage with a different working title; it is consistent with v43/v44 and not a separate result set.

**Resolution: proceed on `manuscript_v44/revised_manuscript.tex` @ `4b3287c`. Not BLOCKED.**
