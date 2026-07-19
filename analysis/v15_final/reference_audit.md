# Reference audit — offline, formatting/consistency only

**File audited:** `manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_C2_final.tex`
**Date:** 2026-07-10
**Scope:** OFFLINE checks only. No web access, no DOI resolution, no verification against external bibliographic sources. Anything that would require the internet or a database is marked **NEEDS-EXTERNAL-CHECK**. No references were added, removed, corrected, or renumbered. The manuscript was not edited.

Bibliography style: hand-written `\begin{thebibliography}` (no `.bib`/BibTeX at build time; a `references_v10.bib` is mentioned in a comment as the source but is not used by the build). Citations use `natbib` `[numbers,sort&compress]`; all in-text references are `\cite{...}` (no `\citep`/`\citet` used).

## Headline counts

| Metric | Value |
|---|---|
| Bibitem entries | 45 |
| Distinct cited keys | 45 |
| Total in-text citation key-instances (with multiplicity) | 54 |
| `\cite{}` commands | 31 |
| Cited keys with NO bibitem (orphan cites) | 0 |
| Bibitem entries never cited | 0 |
| Duplicate bibitem keys | 0 |
| Duplicate entries (same reference twice under different keys) | 0 detected |

The cited-key set and the bibitem-key set are **identical** (perfect 1:1 mapping). No orphan citations, no uncited entries, no duplicate keys.

## (a) Cited keys with no bibitem entry
None.

## (b) Bibitem entries never cited
None. Every one of the 45 entries is cited at least once.

## (c) Duplicate keys / duplicate entries
- No duplicate `\bibitem` keys.
- No two entries appear to describe the same work.
- Keys legitimately cited more than once (not a defect; single entry, multiple in-text uses): `Beal2025` (×2), `EWARScsd` (×2), `Gasparrini2011` (×2), `HussainAlkhateeb2021` (×2), `Murphy1985` (×2), `Tozan2023` (×2), `VanCalster2019` (×2), `Vickers2006` (×2), `Vickers2016` (×2).

## (d) Internal formatting inconsistencies

1. **Author-list truncation style is inconsistent.** The reference-block comment states the convention "first six authors then et al." Most journal entries follow it, but three entries truncate after a SINGLE author with "et al.":
   - `Sangkaew2026` — "Sangkaew S, et al."
   - `ValleDelCauca2024` — "Grubaugh ND, et al."
   - `Campbell2026` — "Campbell AM, et al."
   These list one author + "et al." rather than up to six. Internally inconsistent with the rest of the bibliography and the stated convention. (Whether more authors exist = NEEDS-EXTERNAL-CHECK.)

2. **Missing terminal period.** `Leung2022` is the only journal entry whose DOI line has no trailing period (`...journal.pntd.0010631` with no `.`). All other DOI-bearing entries end with a period.

3. **Key-year vs entry-year mismatches** (cosmetic; keys do not render, but internally inconsistent):
   - `Leung2022` — key says 2022; entry is published **2023** (PLoS Negl Trop Dis. 2023;17(2)).
   - `OpenDengue2024` — key says 2024; entry says "figshare; **2025**."

4. **Journal-name capitalization: "PLoS" vs "PLOS".** Older-style "PLoS" (e.g., `Mordecai2017`, `Huber2018`, `HussainAlkhateeb2021`, `Leung2022`, `Benedum2020`, `ColonGonzalez2021`, `SaitoRehmsmeier2015`) coexists with all-caps "PLOS" (`Sangkaew2026` = PLOS Digit Health; `Campbell2026` = PLOS Glob Public Health). This may reflect the publisher's own rebrand (newer PLOS journals use all-caps), so it is possibly correct-as-printed — NEEDS-EXTERNAL-CHECK — but is an internal capitalization inconsistency on its face.

5. **Date granularity for gray-literature entries.** `PAHO2023` gives a full date ("14 December 2023") whereas every other entry gives year only (optionally with volume/issue). Minor style variance for a situation report.

6. **Key-naming convention is mixed** (cosmetic only): author+year keys (`Mordecai2017`) coexist with descriptive keys (`EWARScsd`, `CHIRPS`, `HDXCODABSriLanka`). Additionally `ValleDelCauca2024` names a place while its entry's first author is Grubaugh and its title concerns Colombia broadly — the key does not obviously match the author or title. No functional impact.

7. **Issue-number presence varies** (standard-Vancouver-acceptable, noted for completeness): some entries carry `volume(issue):pages` (e.g., `Vickers2006` 26(6):565--574) while others use `volume:articlenumber` with no issue (e.g., `VanCalster2019` 17:230; `Funk2015` 2:150066). Consistent with journals that use article numbers; not flagged as an error.

**Not problems:** every entry has a year; page/volume formatting within journal articles is otherwise consistent; the `doi:\,` prefix is uniform; en-dash page ranges (`--`) are uniform.

## (e) Claim–reference plausibility (offline, surface-level only)

Every `\cite` was checked for whether the entry's title/venue is a *plausible* support for the sentence. All 31 citation sites are plausibly consistent with their cited entries; none look mismatched. Whether each reference *actually substantiates* the specific numeric or factual claim is **NEEDS-EXTERNAL-CHECK** (cannot be verified offline). Notes on the few that are worth a human second look:

- `Sangkaew2026` supports "calibration and decision-curve analysis ... recently been applied to dengue prognosis." The entry is *individual-level clinical* prognosis in children (febrile phase), not population/surveillance alerting. Topically adjacent and plausible, but confirm it actually reports calibration/DCA — NEEDS-EXTERNAL-CHECK.
- `VanCalster2019` (co-cited with `Vickers2016`) supports "summarize net benefit across the evaluated decision-curve grid rather than relying on a single threshold." `VanCalster2019` is a calibration paper; the net-benefit-grid point is carried mainly by `Vickers2016`. Loose but defensible pairing.
- `EWARScsd` is cited for detailed operational claims (DLNM of temperature and rainfall in a Bayesian INLA framework, validation by sensitivity/predictive value in Colombian municipalities). Title/venue are consistent; the specific methodological detail is NEEDS-EXTERNAL-CHECK.
- `ValleDelCauca2024` supports "DENV-3 lineage introductions in Colombia" under 2023–2024 El Niño. Entry title ("Dengue outbreak caused by multiple virus serotypes and lineages, Colombia, 2023–2024") is consistent; the DENV-3/El Niño specifics are NEEDS-EXTERNAL-CHECK.
- All dataset/software citations (`OpenDengue2024`, `CHIRPS`, `Funk2015`, `MunozSabater2021`, `ERA5LandCDS`, `Tatem2017`, `WorldPop2025`, `SriLankaCensus2025`, `HDXCODABSriLanka`, `SriLankaWER`, `RCoreTeam2026`, `Gasparrini2011`) are used as provenance for the data/tools they name; surface match is fine.

## NEEDS-EXTERNAL-CHECK (summary)

The following cannot be resolved offline and require external confirmation:

1. Every DOI's resolution and correctness (all `doi:` lines).
2. Correct publication year for `Leung2022` (entry prints 2023; key says 2022) — which is right.
3. `OpenDengue2024` figshare year/version (entry says 2025; text refers to Temporal extract v1.3 and a version-specific record identifier "not available").
4. Full author lists behind the single-author-plus-"et al." entries (`Sangkaew2026`, `ValleDelCauca2024`, `Campbell2026`) — and whether "et al." is being used correctly.
5. Whether "PLoS" vs "PLOS" capitalization matches each journal's official name at time of publication.
6. Volume/issue/page-number correctness for all entries.
7. Whether each cited reference actually substantiates the specific claim/number attributed to it (esp. `Sangkaew2026`, `EWARScsd`, `ValleDelCauca2024`, `PAHO2023` "4.2 million cases / surpassing 2019", `Beal2025` "3–6-month leads in Colombian cities", `Campbell2026` "greatest value-added at 4–6-month leads").
8. Existence/consistency of the referenced `references_v10.bib` (mentioned in a source comment, not part of the offline build).
