# Population-Denominator DCS/Census Validation & Rescaling Plan (Geomatics WP1)
*Validation analysis + proposed rescaling rule. Census tables and the WorldPop CSV stay in git-ignored quarantine and are NOT committed. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged. **No rescaled dataset built yet** — this document proposes the formula and decision rule only.*

**Date:** 2026-06-11

## A. Official DCS / Census sources
- **2024 Census national total: 21,781,800** (Dept of Census & Statistics, CPH 2024). https://www.statistics.gov.lk/Population/StaticalInformation/CPH2024
- **2024 Census district-level totals (all 25 districts):** obtained (e.g., Gampaha 2,436,142; Colombo 2,375,415; Ampara 744,551; …). Primary: DCS CPH-2024; transcribed for validation (confirm against the DCS final district table before the actual rescale).
- **2012 Census** district + DS-level totals (DCS) — available; useful for inter-census trend / DS shares.
- **Mid-year district estimates 2014–2024** (DCS, 2012-census-based) — available (PDF) but anchored to 2012 and not reconciled to the lower 2024 census; use only as a secondary cross-check.
- **2024 DS-level tables** (GN/DS published) — available; can refine the Kalmunai/Ampara internal split if desired.

## B. Validation data downloaded locally (quarantined, not committed)
- `~/data_quarantine/geomatics/population_validation_dcs/census2024_districts.csv` — 25 district 2024-census totals (sums to 21,781,800 ✓). Transcribed from authoritative DCS figures for comparison.

## C. WorldPop vs Census — national
WorldPop 2024 national = **23,008,642** vs Census 2024 **21,781,800** → **+5.6%**.

## D. WorldPop vs Census — district (the key finding)
The +5.6% is **NOT uniform — it is spatially uneven.** Per-district WorldPop-minus-Census:
- **Over-counts (interior/rural):** Moneragala **+24.3%**, Ratnapura +15.3%, Anuradhapura +13.4%, Ampara(district) +13.8%, Kurunegala +12.3%, Galle +11.3%, Kalutara +11.1%, Gampaha +8.0%, Jaffna +8.8%.
- **Under-counts:** Mannar **−12.7%**, Mullaitivu −8.2%, Matale −8.0%, Colombo −4.5%, Matara −4.3%, Killinochchi −2.8%, Kegalle −2.7%, Batticaloa −2.0%.
- **Spread:** min −12.7% → max +24.3% (**37 percentage-point range**), stdev **8.5 pp**, median +4.2%.

**Interpretation:** WorldPop R2025A (constrained, UN-WPP-projected) systematically **over-allocates to interior agricultural districts and under-allocates to some urban/northern districts** relative to the 2024 census. This is a **spatially-structured denominator bias** — exactly the kind that could contaminate a spatial calibration / decision-curve analysis (incidence = cases/pop), since a district with +24% pop has its incidence understated ~20%.

## E. Ampara / Kalmunai validation
WorldPop Ampara district (Ampara RDHS + Kalmunai RDHS) 2024 = **847,385** vs Census Ampara district **744,551** → **+13.8%** (over-count). WorldPop internal split (2024): Ampara RDHS 321,298 / Kalmunai RDHS 526,087 (coastal Kalmunai denser — plausible). The combined over-count must be corrected; the internal split can be kept from WorldPop (or refined with 2024 DS-level census).

## F–H. Denominator options, recommendation, formula
### Options evaluated
- **A. Keep WorldPop as-is** — ❌ leaves a spatially-uneven ±10–24% district bias; risks artificial spatial structure in incidence/calibration.
- **B. National rescale by year** — ❌ corrects the mean only; Moneragala would remain ~+18%, Mannar ~−18% after a single national factor. Insufficient given the 37-pp spread.
- **C / E. District-anchored rescale (WorldPop trend, census level)** — ✅ recommended (see below).
- **D. Census-table-only** — usable but the only full-coverage district anchor is the 2024 census (single point); annual mid-year estimates are 2012-anchored and discontinuous with 2024; 2025 unavailable. Loses WorldPop's smooth annual trend.

### G. Is rescaling recommended? **YES — district-level rescaling (not national).**
The bias is spatially uneven, so a defensible spatial study requires district-anchored correction.

### H. Proposed formula (district-anchored, WorldPop-trend) — NOT yet built
Anchor every district to the **2024 census total**, use WorldPop only for the **annual trajectory** and the **Ampara/Kalmunai internal split**.

For each 1:1 district-RDHS *d*, year *y* ∈ 2018…2025:
```
pop_adj(d, y) = Census2024(d) × WorldPop(d, y) / WorldPop(d, 2024)
```
For the Ampara split (Ampara RDHS *a*, Kalmunai RDHS *k*):
```
AmparaDistrict_adj(y) = Census2024(Ampara) × [WP(a,y)+WP(k,y)] / [WP(a,2024)+WP(k,2024)]
pop_adj(a, y) = AmparaDistrict_adj(y) × WP(a,y) / [WP(a,y)+WP(k,y)]
pop_adj(k, y) = AmparaDistrict_adj(y) × WP(k,y) / [WP(a,y)+WP(k,y)]
```
Properties: at *y*=2024, `pop_adj(d,2024) = Census2024(d)` exactly for all 26 RDHS; district totals match the census; the Ampara/Kalmunai split is preserved; supports all of 2018–2025; 26-RDHS compatible.

### Decision rule
- If per-district |WorldPop−Census| spread were small (e.g., <~10 pp and stdev <~3 pp) → national rescale (B) acceptable.
- Observed spread is 37 pp (stdev 8.5 pp) → **reject A and B; adopt the district-anchored formula (H).**

## Caveats / limitations (to document with the rescale)
- The WorldPop **temporal trend is assumed valid** (smooth ~0.6%/yr); reasonable for an inter-census interval, but 2018–2023 levels are back-projected from the 2024 anchor (not each-year census-validated).
- The 2024 census district figures should be **confirmed against the DCS final district table** (a ~0.1% Colombo provisional/final difference was noted) before building the rescaled dataset.
- The Ampara/Kalmunai internal split currently uses the **WorldPop ratio**; optionally refine with **2024 DS-level census** (pull the DS table into quarantine) for a fully census-based split.
- Mid-year (2012-based) estimates are **not** used as the anchor to avoid a 2012↔2024 discontinuity.

## Next step (on approval)
Build the rescaled denominator dataset per the formula in H → `rdhs_population_dcs_anchored_2018_2025_quarantine.csv` (quarantined), with QC (district totals == census 2024; national == census; split preserved) and a new checksum. Then WP1 (spatial backbone) is complete — still before any climate download, exposure construction, outcome↔exposure linkage, or modeling.
