# Page-by-page visual QC — v15 (final verification)

**Method.** All 23 pages of each of the three final v15 PDFs — internal author-review (line numbers off), line-numbered review (line numbers on), and grayscale line-numbered review — were rendered at **200 dpi** (Poppler `pdftoppm`). Every page of the grayscale PDF was individually opened and inspected (not only figure pages), each against a fixed checklist: body-text readability, line-number visibility, table rules/shading, captions/footnotes, mathematical symbols, hyperlink/gray text, references, Supporting-Information list, internal review notice, and margin clipping. The fail-fast build reported 0 undefined citations/references and no overfull hbox ≥10 pt.

**Overall verdict.** Clean. **23 pages.** Every grayscale page is fully legible. Tables use booktabs rules with no cell shading, so they reproduce exactly in grayscale; the three figures carry redundant non-colour encodings (distinct point markers and solid/dashed line styles in Fig 2; filled circular markers and a crosshatch bar pattern in Fig 3; outlines and text labels in the Fig 1 flow diagram), so all remain legible without colour. Continuous line numbers are visible on every grayscale page; double spacing is active; no margin clipping on any page. One sub-threshold typographic overfull hbox (3.99 pt, Sri Lanka primary-comparison paragraph) and one underfull hbox (a reference line) are present but invisible and below the build's 10 pt fail threshold.

**Note on the v14 QC file (§4).** `page_by_page_visual_qc_v14.md` was opened and checked directly: 36 lines, 3,913 bytes, 0 non-printable/control characters, 25 well-formed table rows, complete sentences. It is **not** corrupted; the malformed-looking text seen in a workflow log was terminal line-wrapping only. No malformed text was carried into v15.

## Per-page grayscale inspection (one row per page)

| Page | Content | Body text | Line numbers | Tables/rules | Captions/footnotes | Math symbols | Refs / gray text | Margin clipping | Grayscale result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Title, authors, internal-review notice | crisp | visible (1–11) | n/a | n/a | n/a | n/a | none | PASS — notice legible |
| 2 | Abstract | crisp | visible | n/a | n/a | p*, ΔNB, CI render | n/a | none | PASS |
| 3 | Author Summary + Introduction | crisp | visible | n/a | n/a | n/a | citation superscripts legible | none | PASS |
| 4 | Introduction / Methods 2.1 | crisp | visible | n/a | n/a | n/a | citations legible | none | PASS |
| 5 | Methods 2.2–2.3 (OpenDengue provenance) | crisp | visible | n/a | n/a | n/a | n/a | none | PASS — new wording legible |
| 6 | Methods 2.4–2.6 | crisp | visible | n/a | n/a | population formula renders | monospace feature names legible | none | PASS |
| 7 | Methods 2.6–2.7 | crisp | visible | n/a | n/a | n/a | monospace pkg names legible | none | PASS |
| 8 | Methods 2.8 (DCA equation)–2.9 | crisp | visible | n/a | n/a | NB equation renders clearly | n/a | none | PASS |
| 9 | Methods 2.9 tail (seed/estimand) | crisp | visible | n/a | n/a | ΔNB renders | n/a | none | PASS |
| 10 | Figure 1 (pipeline) + cohort | crisp | visible | n/a | caption legible | n/a | n/a | none | PASS — boxes/arrows/labels legible |
| 11 | Table 1 + Table 2 + Figure 2 (DCA) | crisp | visible | rules crisp, no shading | legends/caption legible | p* renders | n/a | none | PASS — 6 series distinguishable by marker+line style |
| 12 | Table 3 (recalibration) + 3.4 hybrid | crisp | visible | rules crisp | caption legible | signed ΔAUC/ΔNB render | n/a | none | PASS |
| 13 | Table 4 + hybrid/wild-bootstrap text | crisp | visible | rules crisp | caption legible | ΔNB renders | n/a | none | PASS |
| 14 | Colombia + Table 5 | crisp | visible | rules crisp | caption (ladder/M4 pointer) legible | n/a | n/a | none | PASS |
| 15 | Figure 3 (Colombia AUC + NB) + 3.6 Horizon | crisp | visible | n/a | caption legible | n/a | n/a | none | PASS — markers + crosshatch legible; value labels readable |
| 16 | 3.7 Threshold + Colombia 2022 paragraph | crisp | visible | n/a | n/a | p* renders | n/a | none | PASS |
| 17 | Cross-setting synthesis + Table 6 | crisp | visible | rules crisp | descriptive title legible | ΔNB(M5−M1) renders | n/a | none | PASS |
| 18 | Discussion (estimate-only Sri Lanka wording) | crisp | visible | n/a | n/a | CIs render | n/a | none | PASS |
| 19 | Discussion / Limitations | crisp | visible | n/a | n/a | n/a | n/a | none | PASS |
| 20 | Declarations + Data availability + AI-use | crisp | visible | n/a | n/a | n/a | n/a | none | PASS — pending-confirmation items expected |
| 21 | References [1]–[16] | crisp | visible | n/a | n/a | n/a | DOIs/links black, legible | none | PASS |
| 22 | References [17]–[35] | crisp | visible | n/a | n/a | n/a | OpenDengue [22] clean, no internal filename | none | PASS |
| 23 | Supporting information S1–S12 | crisp | visible | n/a | n/a | n/a | n/a | none | PASS — list complete |

**Cross-checks.** The internal author-review PDF was confirmed to carry no line numbers (title page and a sampled interior page), with content identical to the line-numbered build; the line-numbered PDF carries continuous line numbers throughout. Grayscale differs from colour only on the three figure pages (10, 11, 15); all other pages are black text on white and are identical between colour and grayscale.
