# Reference resolution report — v3

## Root cause of the 17-page `Dengue.pdf` with an empty References section
The three PDFs differ (SHA256 prefixes): `Final Version.pdf` = `e20f0daca0980881`; `~/Downloads/Dengue.pdf` = `ec81e3e665be5f4b`; v2 compiled = `be05e5f7c465b5bc`. **`Dengue.pdf` (17 pp) ends with a bare `References` heading and no entries.** The v2/v3 LaTeX source, by contrast, compiles to a populated bibliography. Therefore `Dengue.pdf` was produced by a build in which **BibTeX did not run or `references.bib` was not present** (the typical cause: only the `.tex` was uploaded to Overleaf, or the compiler did not run BibTeX). It is **not** a source defect.

A genuine source-level hazard did exist: `build.sh` (v1/v2) contained `bibtex … || true`, which suppresses BibTeX failures. v3 removes this.

## v3 resolution
- Bibliography bundled as `references_v3.bib`; manuscript uses `\bibliography{references_v3}` and `\bibliographystyle{unsrtnat}` (numeric, order-of-appearance, locally available; no downloaded style).
- **Fail-fast `build.sh`**: `set -euo pipefail`, `-halt-on-error`, no `|| true`; guards exit non-zero on undefined citations/references or BibTeX errors.

## Verification (v3 build)
| Check | Result |
|---|---|
| `\bibitem` entries in `.bbl` | 35 |
| Undefined citations | 0 |
| Undefined references | 0 |
| `[?]` / `[? ?]` in PDF | 0 |
| References section populated | yes (ends with Cameron, Gelbach & Miller 2008 + DOI) |
| Every cited key in `references_v3.bib` | yes (0 undefined) |
| Duplicate bib keys | none |
| Uncited bib entries | none (unsrtnat prints only cited; all 35 are cited) |
| BibTeX `.blg` errors | 0 |

## Citation corrections carried from the v1 reference audit (already in the bib)
- `Baharom2022`, `HussainAlkhateeb2021`, `VanCalster2023` author lists corrected; OpenDengue cited (V1.3 note); Sri Lanka census year 2025 (district-totals release describing the 2024 census); added DOI-verified DCA/calibration/bootstrap/PR-AUC/EWARS/STROBE references. See `docs/reference_audit_v1.md`.

**Hard-stop satisfied:** v3 contains zero `[?]` citations and a fully populated, numbered References section.
