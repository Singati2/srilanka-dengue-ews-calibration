# Reference integrity report — v5 (§16)

Rendered as an inline Vancouver `thebibliography` (no Vancouver/PLOS `.bst` is installed in this TeX distribution; the base styles cannot produce surname-first, no-period, first-six-et-al Vancouver output). The bibliography is numbered by order of first citation, generated from `references_v5.bib`, and renders without BibTeX. Build: 35 `\bibitem` entries, 35/35 `\cite` keys resolved, 0 undefined, 0 `[?]`.

## Vancouver formatting applied
- Surname followed by initials (no full first names): e.g., "Mordecai EA, Cohen JM, ...".
- First six authors then "et al." for entries with more than six authors (Mordecai2017, Johansson2019, Lowe2021, EWARScsd, Collins2024TRIPODAI, Wolff2019, Moons2019, MunozSabater2021, Funk2015).
- NLM journal abbreviations (PLoS Negl Trop Dis, Proc Natl Acad Sci U S A, Lancet Planet Health, BMC Med, Eur Heart J, Med Decis Making, Diagn Progn Res, Mon Weather Rev, Am J Trop Med Hyg, Front Public Health, Lancet, Ann Intern Med, Sci Data, Earth Syst Sci Data, Stat Med, J Stat Softw, PLoS One, Rev Econ Stat, Risk Manag Healthc Policy).
- Year;volume(issue):pages format; `doi:` prefix on every entry with a DOI; `[dataset]`/`[Internet]` designations for non-article sources.
- No internal/editorial commentary remains in any entry.

## Defects found and corrected in v5
1. **EWARS-csd author error (corrected).** v4 listed "Hussain-Alkhateeb, Laith and others" as if he were first author. Verified from the publisher page (Front Public Health 2024;12:1323618): the correct author order is **Schlesinger M, Prieto Alvarado FE, Borbón Ramos ME, Sewe MO, Merle CS, Kroeger A, Hussain-Alkhateeb L** (he is the senior/last author). Corrected in both the rendered bibliography and `references_v5.bib`. Cross-confirmed by `canonical_R_dlnm_report.md` line 58 ("Schlesinger 2024").
2. **OpenDengue editorial note removed (hard-stop).** The bibliography entry no longer contains the V1.2-vs-V1.3 commentary. The version/DOI issue is moved to `submission_blockers_v5.md`. The entry cites the record DOI `10.6084/m9.figshare.24259573` and the version (V1.3) used; the version-specific DOI is an author-to-confirm submission blocker (not asserted falsely).
3. **Stale `\bibliography{references_v4}` reference removed** (the v4 source pointed at the v4 bib); replaced by the inline Vancouver list.

## R / software citation (§17)
- `RCoreTeam2026` (R 4.6.0, 2026-04-24) is **verified** against `canonical_R_dlnm_report.md` (with a recorded `sessionInfo` sha256). dlnm 2.4.10, mgcv 1.9.4, tsModel 0.6-2 likewise verified. R is cited only for the `dlnm` comparator.
- No Python software citation exists; the Python stack versions are not preserved. Flagged as a submission blocker, not invented.

## Author-to-confirm (not invented)
WER access URL/date; HDX COD-AB record URL/version/access date; OpenDengue exact V1.3 DOI + download date; a Python software citation. All tracked in `submission_blockers_v5.md`.
