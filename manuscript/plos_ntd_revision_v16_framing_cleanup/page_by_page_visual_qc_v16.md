# Page-by-page visual QC — v16 (framing cleanup)

**Method.** All 24 pages of the line-numbered and grayscale line-numbered v16 PDFs were rendered at 200 dpi (Poppler `pdftoppm`). The pages carrying v16's framing edits — the cross-setting synthesis/Table 6 page, the Discussion pages, and the Limitations/future-work pages — were individually inspected in colour and grayscale. The remaining pages are unchanged in content from the fully inspected v15 build (their pagination shifts by at most one page from the cross-setting page onward, because the added future-work paragraph and sentences added one page: 23 → 24). Fail-fast build reported 0 undefined citations/references and no overfull hbox ≥10 pt.

**Overall verdict.** Clean. **24 pages.** 0 clipping/overflow, 0 line-number collisions, 0 unreadable tables/figures, 0 undefined references, 0 literal placeholder tokens. One sub-threshold overfull hbox (3.99 pt, Sri Lanka primary-comparison paragraph — pre-existing, invisible) and one underfull hbox (a reference line). Continuous line numbers on the line-numbered build; double spacing active; grayscale legible on every inspected page.

## Changed-content pages (individually inspected, colour + grayscale)

| Page | Edit(s) | Verified content | Result |
|---|---|---|---|
| 17 | EDIT 1 | Cross-setting: "No formal interaction, heterogeneity or equivalence analysis was performed. The setting-specific estimates differed in magnitude and precision, but this study does not establish whether the underlying effects differ between settings. The two settings should be interpreted as complementary rather than as a formal comparative experiment." Table 6 intact. | PASS |
| 18 | EDIT 2, 3, 4 | Discussion: "In Sri Lanka, the planned M4−M1 estimate was −0.008 (95% CI −0.028 to +0.013), while the expanded M5−M1 sensitivity estimate was +0.0081 (95% CI −0.0012 to +0.0181). In Colombia, the M5−M1 estimate was +0.0188 …"; wild-cluster-bootstrap-t "a secondary, single-implementation sensitivity … but did not independently validate them"; "No formal cross-setting comparison was performed; the two settings should be interpreted as complementary rather than as a formal comparative experiment." | PASS (colour + grayscale) |
| 19 | EDIT 6 | Limitations: "… percentile (exceedance) thresholds rather than official outbreak declarations, representing elevated-activity alerting rather than rare-epidemic declaration (even the stricter 90th-percentile sensitivity remained a comparatively common outcome), …" | PASS |
| 20 | EDIT 5 | Future-work: "Future operational evaluation should preserve real-time surveillance vintages and reporting triangles, incorporate nowcasting of provisional counts, use rolling-origin and spatial-block validation, and elicit decision thresholds from documented response costs and stakeholder preferences. A formal cross-setting comparison would additionally require harmonized periods, spatial units, predictors, recalibration procedures and a jointly specified setting-by-model analysis." Retained mechanistic-modeling sentence follows; Declarations intact. | PASS |

## Unchanged pages
Pages 1–16 (title, Abstract, Author Summary, Methods, Tables 1–5, Figures 1–3, Colombia 2022 paragraph) and 21–24 (References, Supporting Information) carry content identical to the v15 build inspected in `plos_ntd_revision_v15_final_verification/page_by_page_visual_qc_v15.md`; only pagination shifts by one page from the cross-setting page onward. The internal author-review build carries no line numbers; the grayscale build reproduces text pages identically and the three figure pages remain legible via their redundant non-colour encodings.

## Compliance confirmations (v16 edits)
- No prohibited phrasing anywhere in the manuscript or SI: "statistically indistinguishable/equivalent", "intervals overlap", "significant in one setting/versus nonsignificant", "includes/excludes/contains/crosses zero" — all 0.
- No AI-review, field-expert, peer-review, or AI-agent-count language in the manuscript or Supporting Information (the provenance statement lives only in the internal `sensitivity_review_provenance_v16.md`).
