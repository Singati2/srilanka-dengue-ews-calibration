# PLOS Global Public Health — Submission-Compliance Checklist

**Manuscript:** `manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_C2_final.tex`
**Checked:** 2026-07-10
**Sourcing note:** The only saved PLOS requirements file in the repo is `docs/plos_ntd_submission_requirements_audit_v1.md`, which audits **PLOS NTD** (a sibling journal), not PLOS Global Public Health (GPH). PLOS-wide policies (data availability, code sharing, funding, competing interests, authorship/CRediT, AI disclosure, ORCID, Vancouver references, line numbering/spacing, figure/table placement, Supporting-Information naming) are quoted verbatim from official PLOS pages in that audit and apply across PLOS journals; these are treated as sourced. GPH-specific items that differ from NTD (abstract structure, Author Summary, title constraints) are **not** sourced here and are marked External-confirmation-needed. No requirement below is invented.

---

## RESOLVED

- **Title & short title.** Full title present (line 52); running short title present (line 54).
- **Author affiliations.** Three authors with superscripted institutional affiliations (lines 56–61).
- **Corresponding-author info.** Corresponding author flagged (`$\ast$`, line 56) with email `ganshiwakoti@gmail.com` (line 62). (ORCID still needed — see Author-action.)
- **Line numbering / spacing / single column.** `\doublespacing` (line 38), `\linenumbers` continuous (line 45), single-column article class — matches PLOS §7.
- **Reference format.** Numbered Vancouver, ordered by first appearance, first-six-authors-then-et-al, NLM-style journal abbreviations, DOIs appended (`thebibliography`, lines 428–521) — matches PLOS §6. (Final .bst production is a post-acceptance formatting step.)
- **Reporting-guideline mention.** STROBE + TRIPOD+AI + PROBAST cited in Methods (line 98); S1 (STROBE), S2 (TRIPOD+AI), S3 (PROBAST) checklists planned (lines 531–533).
- **AI/LLM disclosure.** Dedicated statement naming tool (Anthropic Claude via Claude Code), use, and author validation (line 417) — matches PLOS §14.
- **Figure files.** Nine figures as external files `Fig1.pdf`–`Fig9.pdf` via `\includegraphics`, each caption in-text immediately after first citation — matches PLOS §8 (main-file figures acceptable at initial submission).
- **Table placement.** All tables embedded in-text after first citation, none in separate files — matches PLOS §8.
- **Supporting-Information captions.** All S1–S14 captions present, listed after References, each with an "S#" name — matches PLOS §9 (lines 528–544).

---

## AUTHOR-ACTION-REQUIRED

1. **[BLOCKING] Data Availability Statement** — placeholder only: "Repository and archival details … pending author confirmation" (line 412). PLOS §10 requires a complete DAS in every submission.
2. **[BLOCKING] Code availability** — placeholder within the DAS (line 412); no repository, persistent identifier, or open license stated. PLOS §11 requires author-generated code shared under a persistent-ID repository + open license, with access stated in the DAS.
3. **[BLOCKING] Ethics statement** — placeholder: "A formal institutional determination is pending author/institutional confirmation" (line 411). Provide IRB determination or an explicit not-applicable justification for de-identified aggregate surveillance data.
4. **[BLOCKING] Funding statement** — "Pending author confirmation" (line 413). PLOS §13c requires a Funding Statement (use the standard "no specific funding" wording if unfunded).
5. **[BLOCKING] Competing interests** — "Pending author confirmation" (line 414). PLOS §13d requires a declaration (standard "no competing interests" statement if none).
6. **[BLOCKING] Author contributions (CRediT)** — "Pending author confirmation" (line 415). PLOS §13b requires CRediT roles per author.
7. **[BLOCKING] OpenDengue v1.3 version-specific record identifier + acquisition date** — explicitly unavailable: "A version-specific record identifier for version 1.3 and the acquisition date are pending author confirmation" (lines 104, 412). The cited Figshare DOI (`10.6084/m9.figshare.24259573`, ref OpenDengue2024) is the general record, not the pinned version. Recover and record both.
8. **[BLOCKING] Pinned/reproducible Python environment for primary models** — "versions of the Python modeling stack were not preserved in the reproducibility record" (lines 115, 535). The primary M0–M5 penalized-logistic models are Python; reconstruct and pin (e.g., lockfile / environment.yml) so the primary results are reproducible.
9. **Abstract length** — the abstract is ~500 words (lines 72–76), far above the typical PLOS ~250–300-word limit. Shorten substantially. (Exact GPH limit is External-confirmation-needed, but current length exceeds any PLOS limit.)
10. **Acknowledgments** — placeholder "Pending author confirmation" (line 416); complete or remove before submission.
11. **Corresponding-author ORCID** — not present in the manuscript; PLOS §13e requires the corresponding author's ORCID entered in the submission system. (Author ORCIDs also flagged outstanding in `docs/zenodo_release_plan_v1.md`.)
12. **Supporting-Information in-text citations** — S2, S3, S4, S7, S8, S10, S13, S14 (and S1) have captions but are not cited by their S-number in the body (only generic "Supporting Information"). PLOS §9 expects each SI item cited in text; add explicit S# call-outs or reconcile.
13. **Archive frozen predictions + input checksums to a tamper-evident repository (Zenodo/OSF)** — recommended. A plan exists (`docs/zenodo_release_plan_v1.md`) but **no record, tag, or DOI has been created**. Depositing the frozen M1/M4/M5 predictions plus `source_checksums_v1.txt` (referenced as S10 Text) under a DOI + open license both hardens dataset/model provenance and simultaneously satisfies the Data Availability (#1) and Code Availability (#2) requirements.

---

## EXTERNAL-CONFIRMATION-NEEDED

- **Abstract: structured vs unstructured + word limit for PLOS GPH.** Manuscript uses an unstructured abstract per its own preamble claim (lines 4–9). The only sourced audit (PLOS NTD) requires a *structured* abstract (Background / Methodology-Principal Findings / Conclusions-Significance, 250–300 words). GPH policy not sourced here — confirm on the GPH author guidelines before finalizing.
- **Author Summary requirement for PLOS GPH.** Manuscript omits an Author Summary (preamble claims GPH does not require one). PLOS NTD *requires* a 150–200-word first-person Author Summary. Confirm whether GPH requires one.
- **Title format/length constraints for GPH.** No title-length or format rule is sourced. Confirm against GPH guidelines.
- **TRIPOD as a required reporting guideline.** The sourced audit marks TRIPOD "UNVERIFIED" for PLOS (STROBE is the confirmed observational guideline). Manuscript cites TRIPOD+AI and plans an S2 checklist; confirm TRIPOD applicability/acceptance for the prediction-model component via EQUATOR/GPH.
- **Figure production specs at revision.** NTD figure guidance (separate TIFF/EPS, 300–600 ppi, ≤10 MB) applies at acceptance/revision; confirm GPH figure-file specs at that stage (not blocking at initial format-free submission).
- **Section-order / heading conventions for GPH.** Manuscript uses "Materials and methods" and a combined-order layout; confirm against the GPH template (initial submission is format-free per PLOS-wide policy, so not blocking).

---

*Counts — Resolved: 10 · Author-action-required: 13 · External-confirmation-needed: 6.*
