# DCA_DENGUE_NOVELTY_VERIFICATION (Gate B)

Targeted verification of the sentence: *"To our knowledge, this is the first application of decision-curve net benefit to population-level dengue elevated-activity / early-warning forecasting, distinct from individual clinical dengue prognosis."*

## Search method
- **Date:** 2026-08-10.
- **Engine:** web search (US). Sources surfaced: arXiv, medRxiv, PubMed/PMC, ResearchGate, Springer, Frontiers, PLOS, Royal Society, Wikipedia. Scopus/Web of Science were **not** connected (a residual coverage limit — see classification).
- **Queries run (verbatim):**
  1. `"decision curve analysis" OR "net benefit" dengue outbreak forecasting early warning population`
  2. `dengue "decision curve analysis" net benefit prediction model clinical`
  3. `dengue early warning system "net benefit" threshold decision analysis cost-loss alert`
  - (A prior session also ran: `decision curve analysis net benefit dengue outbreak early warning surveillance`.)
- **Inclusion:** any dengue study evaluating population-level forecasts/alerts by decision-curve analysis or Vickers-style net benefit. **Exclusion:** general DCA methodology papers; individual-patient clinical dengue prognosis (explicitly out of scope for the claim); cost-effectiveness/ICER analyses (a different decision framework).

## Relevant papers found
| Title | Year | Population/Individual | Forecast/Diagnosis | Early-warning? | DCA used? | Net benefit (Vickers)? | Threshold utility? | Conflicts with claim? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Signalling disease outbreaks: cost-effectiveness analysis of EWARS for dengue control (Shim et al.) | 2015 | Population | Forecast/response | Yes | No | No | Cost-loss via decision-tree/ICER | **No** | Cost-effectiveness (ICER), not decision-curve net benefit |
| EWARS-csd operational analysis (Schlesinger et al., Front Public Health) | 2024 | Population | Forecast/alarm | Yes | No | No | Alarm sensitivity/specificity/PPV | **No** | DLNM+INLA; no DCA/net benefit |
| Dengue epidemic alert thresholds (medRxiv) | 2024 | Population | Alert detection | Yes | No | No | Endemic-channel thresholds | **No** | Threshold-setting, not DCA |
| Evaluating probabilistic dengue risk forecasts, Brazil prototype EWS (PMC4775211) | 2016 | Population | Forecast | Yes | No | No | Skill/reliability scores | **No** | Probabilistic scoring, not net benefit |
| Probabilistic seasonal dengue forecasting, Vietnam superensembles (Colón-González 2021) | 2021 | Population | Forecast | Yes | No | No | CRPS/skill | **No** | Proper scores, not DCA |
| Sangkaew et al., early individualized dengue risk (PLOS Digit Health) | 2026 | **Individual** | Clinical prognosis | No | **Yes** | Yes | Yes | **No** | The one dengue DCA use — individual clinical prognosis; explicitly excluded by the claim, cited as such |
| General DCA methodology (Vickers 2006/2016/2019; continuous net benefit) | — | — | — | — | Yes | Yes | Yes | **No** | Methods anchors, not dengue applications |

**No population-level dengue early-warning/forecasting study evaluating predictions by decision-curve analysis / Vickers net benefit was identified.** The dengue EWS literature instead uses cost-effectiveness (ICER), endemic-channel alert thresholds, and discrimination/skill/alarm metrics. The sole dengue DCA use is individual clinical prognosis (Sangkaew 2026), which the claim distinguishes.

## Classification: `SUPPORTED_WITH_HEDGE`
No conflicting prior work found, but the search did not include Scopus/Web of Science and cannot be exhaustive. Therefore **do not** assert an absolute "first." Use the softer, defensible wording (per §5 of the task):

> "To our knowledge, we did not identify a prior population-level dengue early-warning forecasting study that evaluated predictions using decision-curve net benefit, in contrast to its recent use in individual dengue clinical prognosis."

Applied to the candidate `.tex` (novelty sentence rewritten; in-`.tex` marker updated to `VERIFIED_SUPPORTED_WITH_HEDGE`). `NOVELTY_CLAIM_AUDIT.md` updated accordingly.

## Sources
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4475106/ (cost-effectiveness of dengue EWARS)
- https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2024.1323618/full (EWARS-csd)
- https://www.medrxiv.org/content/10.1101/2024.10.22.24315684.full.pdf (dengue epidemic alert thresholds)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4775211/ (Brazil prototype EWS forecast evaluation)
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7971894/ (Vietnam superensemble seasonal forecasting)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6777022/ (DCA interpretation guide, methodology)
- https://en.wikipedia.org/wiki/Decision_curve_analysis (DCA overview)
