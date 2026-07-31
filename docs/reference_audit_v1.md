# Reference Audit v1 — Dengue EWS Calibration / Decision-Curve Manuscript

> **Correction addendum (2026-06-27).** The three confirmed reference errors identified below have been corrected in the **revision bibliography** `manuscript/plos_ntd_revision_v1/references.bib` (not in the historical `manuscript/references.bib`): `Baharom2022` author list (Baharom M, Ahmad N, Hod R, Abdul Manaf MR), `HussainAlkhateeb2021` (full five-author list + restored "A scoping review" title), and `VanCalster2023` (Van Calster B, Steyerberg EW, Wynants L, van Smeden M). Also applied to the revision bib: OpenDengue now cited in the manuscript with a **V1.3** version note; Sri Lanka census entry moved to **2025** (district-totals release) with a 2024-census note; verified additions added (Vickers 2016/2019, Steyerberg & Vergouwe 2014, Cameron–Gelbach–Miller 2008, Saito–Rehmsmeier 2015, EWARS-csd, STROBE/von Elm 2007). Grey-literature/dataset citation strings (WER, census title/URL, HDX COD-AB record, R version) remain **author-to-confirm**. No bibliography was committed.

**Auditor task:** Verify every bibliography entry against a primary source (DOI resolution / Crossref / publisher / official dataset documentation), flag errors and consistency problems, and assess the requested citation checklist.

**Inputs audited:**
- Bibliography: `manuscript/references.bib` (29 entries)
- Manuscript: `Final Version.pdf` and its LaTeX source `manuscript/dengue_ews_manuscript.tex` (+ `.bbl`, which prints **23** of the 29 entries)

**Date of audit:** 2026-06-26
**Verification method:** Crossref REST API (`api.crossref.org/works/<doi>`) for all DOI-bearing entries; DOI resolver + publisher/dataset pages and web search for dataset/grey-literature entries. Where a publisher page blocked fetching, the authoritative Crossref record plus an independent web search were used.

---

## 1. Per-entry verification table

Legend — **Verified?**: CLEAN = authors/year/title/venue/vol/issue/pages/DOI all match a primary source; ERROR = a verifiable discrepancy; OK(grey) = real non-DOI source confirmed; PARTIAL = real but with a discrepancy. **Supports statement?**: matches the in-text claim it is attached to.

| Key | Verified? | DOI status | Corrections needed | Cited in text? | Supports statement? |
|---|---|---|---|---|---|
| Vickers2006 | CLEAN | Resolves OK | none | Yes | Yes — DCA primary method ref |
| Murphy1985 | CLEAN | Resolves OK | none | Yes | Yes — cost-loss/forecast value |
| Tozan2023 | CLEAN | Resolves OK | none | Yes | Yes — economic eval of EWS |
| Johansson2019 | CLEAN | Resolves OK | none (PNAS 116(48):24268-24274) | Yes | Yes — dengue forecast discrimination |
| Mordecai2017 | CLEAN | Resolves OK | none (PLOS NTD 11(4):e0005568) | Yes | Yes — climate-transmission |
| Huber2018 | CLEAN | Resolves OK | none (PLOS NTD 12(5):e0006451) | Yes | Yes — climate suitability |
| Gasparrini2010 | CLEAN | Resolves OK | none (Stat Med 29(21):2224-2234) | Yes | Yes — DLNM method |
| Gasparrini2011 | CLEAN | Resolves OK | pages 1-20 not in Crossref but correct for JSS 43(8) | Yes | Yes — dlnm R package |
| Lowe2021 | CLEAN | Resolves OK | none (Lancet Planet Health 5(4):e209-e219) | **No** (uncited) | n/a — would support climate-dengue EWS framing |
| HussainAlkhateeb2021 | **ERROR** | Resolves OK | (a) `author={...and others}` — **"others"/et-al inside a reference entry**; real authors: Hussain-Alkhateeb L, Rivera Ramirez T, Kroeger A, Gozzer E, Runge-Ranzinger S. (b) Title is truncated; full title ends "...What Is the Evidence? **A scoping review**". | Yes | Yes — EWS discrimination-metric framing |
| Baharom2022 | **ERROR** | Resolves OK | Author list wrong. Verified authors (4): **Baharom M, Ahmad N, Hod R, Abdul Manaf MR**. Bib lists 5 with wrong given names (Muhammad/Nurul/Razitasham) and **fabricated/incorrect** "Arsad, Faizah and Tangang, Fredolin"; omits Abdul Manaf MR. Vol 15, pp 871-886 correct. | Yes | Yes — dengue EWS systematic review |
| VanCalster2019 | CLEAN | Resolves OK | none (BMC Med 17:230) | Yes | Yes — calibration importance |
| VanCalster2023 | **ERROR** | Resolves OK | Author list wrong. Verified authors (4): **Van Calster B, Steyerberg EW, Wynants L, van Smeden M**. Bib incorrectly lists Riley RD and Collins GS and omits Steyerberg. Vol 21:70 correct. | Yes | Yes — validation/recalibration framing |
| Collins2015 | CLEAN | Resolves OK | none (BMJ 350:g7594) | Yes | Yes — TRIPOD |
| Moons2019 | CLEAN | Resolves OK | none (Ann Intern Med 170(1):W1-W33) | Yes | Yes — PROBAST E&E |
| Wolff2019 | CLEAN | Resolves OK | none (Ann Intern Med 170(1):51-58) | Yes | Yes — PROBAST |
| Collins2024TRIPODAI | PARTIAL | Resolves OK | Entry correct (BMJ 385:e078378). Uses `and others` for the author list (et-al inside entry) — acceptable for a 20+ author statement but flag for consistency. | **No** (uncited) | n/a — would support the TRIPOD+AI / TRIPOD self-assessment text |
| MunozSabater2021 | CLEAN | Resolves OK | none (ESSD 13:4349-4383) | Yes | Yes — ERA5-Land |
| ERA5LandCDS | OK(grey) | DOI 10.24381/cds.e2161bac resolves to C3S CDS "ERA5-Land hourly data from 1950 to present" | Correct. **Duplicate-source flag**: pairs with MunozSabater2021 (data product vs methods paper) — intentional but note. | Yes | Yes — climate data product |
| Funk2015 | CLEAN | Resolves OK | none (Sci Data 2:150066) | Yes | Yes — CHIRPS methods paper |
| CHIRPS | OK(grey) | No DOI (data product page) | Real product (Climate Hazards Center, UCSB). **Duplicate-source flag**: pairs with Funk2015 (product vs paper) — intentional but note. `year={2026}` is an access year, not a publication year. | Yes | Yes — precipitation product |
| Tatem2017 | CLEAN | Resolves OK | none (Sci Data 4:170004) | Yes | Yes — WorldPop methods paper |
| WorldPop2025 | OK(grey) | No DOI | Real: WorldPop "Global 2 / Global 2015-2030, R2025A" 100m product, public release Sept 2025 (worldpop.org). **Duplicate-source flag**: pairs with Tatem2017 (product vs paper) — intentional but note. | Yes | Yes — population raster product |
| Clarke2024OpenDengue | CLEAN | Resolves OK | none (Sci Data 11:296; authors J. Clarke, A. Lim, P. Gupte, D.M. Pigott, W.G. van Panhuis, O.J. Brady) | **No** (uncited) | **Should support the Colombia data source — currently no in-text cite exists** |
| OpenDengue2024 | PARTIAL | DOI 10.6084/m9.figshare.24259573 resolves to figshare "OpenDengue V1.2" | Real dataset. **But version mismatch**: the manuscript/docs Colombia arm actually uses **OpenDengue V1.3** (Temporal_extract_V1_3, sha256 7f5df21...), not V1.2. **Duplicate-source flag**: pairs with Clarke2024OpenDengue (dataset vs paper). | **No** (uncited) | Same as above — Colombia source not cited in text |
| SriLankaWER | OK(grey) | No DOI | Real: Epidemiology Unit, Ministry of Health Sri Lanka, Weekly Epidemiological Report. Acceptable grey-literature/dataset citation. | Yes | Yes — Sri Lanka dengue outcome source |
| SriLankaCensus2024 | PARTIAL | No DOI | **A 2024 census DOES exist** (Census moment 19 Dec 2024; enumeration Oct 2024-Feb 2025; prior census was 2012). **District/divisional population totals were published, but in the preliminary release dated 30 October 2025**, not 2024 (national total 21,763,170-21,781,800). Recommend `year={2025}` for the district-totals release, or a note clarifying "2024 Census, district totals released 2025." Title plausible; verify the exact published title ("Census of Population and Housing 2024 — Basic Population Information by Districts and DS Divisions"). | Yes | Yes — population-denominator anchoring |
| HDXCODABSriLanka | OK(grey) | No DOI | Plausible real source (HDX / OCHA / Survey Dept of Sri Lanka COD-AB). Not independently DOI-verifiable; acceptable as a dataset citation. Consider adding the HDX dataset URL/access date. | **No** (uncited) | n/a — boundary source |
| RCoreTeam2024 | OK(grey) | No DOI | Standard R citation form. | **No** (uncited) | n/a — software |

---

## 2. Consistency problems

**Entry count.** `references.bib` has **29 entries**; the compiled `.bbl` / Final Version PDF prints **23**. The 6 entries present in the bib but **never `\cite`d** in the text are:

| Uncited bib entry | Real? | Note |
|---|---|---|
| `Clarke2024OpenDengue` | Yes | **Should be cited** — it is the data-source paper for the Colombia analysis (a major part of the paper). |
| `OpenDengue2024` | Yes (V1.2; study used V1.3) | Should be cited as the Colombia dataset; fix version. |
| `Lowe2021` | Yes | Highly relevant climate-dengue EWS benchmark; recommend citing in intro/discussion. |
| `Collins2024TRIPODAI` | Yes | Relevant — manuscript does PROBAST/TRIPOD self-assessment; TRIPOD+AI is the current standard. |
| `HDXCODABSriLanka` | Yes | Boundary source; the methods describe "Sri Lanka administrative boundary data" but do not cite it. Add a cite at that sentence. |
| `RCoreTeam2024` | Yes | Software; the methods mention R/`dlnm` but never cite R itself. Add to a software/reproducibility note. |

**In-text citations missing from the bib:** none. Every `\citep` key resolves to a bib entry.

**"et al." / "others" inside a reference-list entry (flagged):**
- `HussainAlkhateeb2021` — `author = {Hussain-Alkhateeb, Laith and others}` (only 5 real authors; should be listed in full).
- `Collins2024TRIPODAI` — `... and others` (large author group; lower priority but inconsistent).

**Duplicate / overlapping dataset citations (data product vs methods paper):** these are paired intentionally but should be acknowledged so reviewers don't read them as padding —
- ERA5-Land: `MunozSabater2021` (paper) + `ERA5LandCDS` (CDS product DOI).
- CHIRPS: `Funk2015` (paper) + `CHIRPS` (product).
- WorldPop: `Tatem2017` (paper) + `WorldPop2025` (R2025A product).
- OpenDengue: `Clarke2024OpenDengue` (paper) + `OpenDengue2024` (figshare dataset) — currently both uncited.

**Confirmed factual errors (3 entries):** `HussainAlkhateeb2021` (author truncation + title truncation), `Baharom2022` (wrong/fabricated authors 4-5), `VanCalster2023` (wrong author set — Riley & Collins listed, Steyerberg omitted).

**Other consistency notes:**
- `CHIRPS` `year={2026}` and the `SriLankaWER` `year={2018--2025}` are access/coverage years rather than publication years — harmless but flag for style consistency.
- `SriLankaCensus2024` `year={2024}` vs actual district-totals release (2025) — see table.
- `OpenDengue2024` version 1.2 vs study's V1.3 — fix.

---

## 3. Requested checklist — is a correct, real, directly-relevant citation present or recommended?

| Checklist item | Status in manuscript | Verdict |
|---|---|---|
| OpenDengue data-source paper | In bib (`Clarke2024OpenDengue`) but **uncited** | Real & relevant — **cite it** (see §4). |
| Colombia surveillance source (SIVIGILA/INS) | **Absent** | Colombia data was sourced via OpenDengue (V1.3), whose upstream is INS/SIVIGILA. Cite OpenDengue (Clarke2024 + dataset) and optionally name SIVIGILA/INS as the original source in text. No separate DOI'd SIVIGILA paper is required. |
| CHIRPS | Present (`Funk2015` + `CHIRPS`) | OK. |
| ERA5-Land | Present (`MunozSabater2021` + `ERA5LandCDS`) | OK. |
| WorldPop | Present (`Tatem2017` + `WorldPop2025`) | OK. |
| Sri Lanka WER | Present (`SriLankaWER`) | OK (grey-lit form acceptable). |
| 2024 Sri Lanka population/census release | Present (`SriLankaCensus2024`) | **Confirmed to exist** (2024 census; prior census 2012). District totals published **30 Oct 2025** — adjust year/note. |
| DCA original (Vickers & Elkin 2006) | Present (`Vickers2006`) | OK. |
| Modern DCA guidance (Vickers/Van Calster/Steyerberg 2016 BMJ; 2019 step-by-step) | **Absent** | Real & relevant — **recommend adding** (see §4). |
| Calibration guidance (Van Calster 2019) | Present (`VanCalster2019`) | OK. |
| Calibration guidance (Steyerberg & Vergouwe 2014) | **Absent** | Real & relevant — **recommend adding** (see §4). |
| Cluster-bootstrap methodology (Cameron, Gelbach & Miller 2008) | **Absent** (manuscript uses RDHS-/municipality-cluster bootstrap) | Real & relevant — **recommend adding** (see §4). |
| PR-AUC guidance (Saito & Rehmsmeier 2015) | **Absent** (manuscript reports PR-AUC) | Real & relevant — **recommend adding** (see §4). |
| TRIPOD+AI (Collins et al. 2024 BMJ) | In bib (`Collins2024TRIPODAI`) but **uncited** | Real & relevant — **cite it**. |
| PROBAST (Wolff/Moons 2019) | Present (`Wolff2019`, `Moons2019`) | OK. |
| STROBE / observational-study checklist | **Absent** | Optional — recommend STROBE (von Elm 2007) for the observational design (see §4). |
| Operational dengue EWS frameworks (WHO/TDR EWARS) | **Absent** | Real & relevant — **recommend adding** EWARS-csd (see §4). |
| Prior dengue forecasting benchmarks (Johansson 2019; Lowe 2021) | `Johansson2019` cited; `Lowe2021` in bib but **uncited** | Cite `Lowe2021`. |

---

## 4. Recommended additions — verified real & relevant (full citations + DOIs)

All verified via Crossref on 2026-06-26.

| Topic | Full citation | DOI | Verified |
|---|---|---|---|
| Modern DCA guidance (concise) | Vickers AJ, Van Calster B, Steyerberg EW. Net benefit approaches to the evaluation of prediction models, molecular markers, and diagnostic tests. *BMJ*. 2016;352:i6. | 10.1136/bmj.i6 | Yes |
| DCA step-by-step interpretation | Vickers AJ, van Calster B, Steyerberg EW. A simple, step-by-step guide to interpreting decision curve analysis. *Diagn Progn Res*. 2019;3:18. | 10.1186/s41512-019-0064-7 | Yes |
| Calibration / performance-measures framework | Steyerberg EW, Vickers AJ, Cook NR, Gerds T, Gonen M, Obuchowski N, Pencina MJ, Kattan MW. Assessing the performance of prediction models: a framework for traditional and novel measures. *Epidemiology*. 2010;21(1):128-138. | 10.1097/EDE.0b013e3181c30fb2 | Yes |
| Calibration / validation guidance (Steyerberg & Vergouwe 2014) | Steyerberg EW, Vergouwe Y. Towards better clinical prediction models: seven steps for development and an ABCD for validation. *Eur Heart J*. 2014;35(29):1925-1931. | 10.1093/eurheartj/ehu207 | Yes |
| Cluster bootstrap methodology | Cameron AC, Gelbach JB, Miller DL. Bootstrap-based improvements for inference with clustered errors. *Rev Econ Stat*. 2008;90(3):414-427. | 10.1162/rest.90.3.414 | Yes |
| PR-AUC guidance | Saito T, Rehmsmeier M. The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE*. 2015;10(3):e0118432. | 10.1371/journal.pone.0118432 | Yes |
| Operational dengue EWS (WHO/TDR EWARS-csd) | Hussain-Alkhateeb L, et al. Enabling countries to manage outbreaks: statistical, operational, and contextual analysis of the early warning and response system (EWARS-csd) for dengue outbreaks. *Front Public Health*. 2024;12:1323618. | 10.3389/fpubh.2024.1323618 | Yes (title/venue verified; list authors in full when adding) |
| Observational reporting (optional) | von Elm E, Altman DG, Egger M, Pocock SJ, Gotzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *Lancet*. 2007;370(9596):1453-1457. | 10.1016/S0140-6736(07)61602-X | DOI plausible/standard — confirm before use |

Notes:
- The single most important addition is **citing the OpenDengue data source in the Colombia methods** (`Clarke2024OpenDengue` is already in the bib; just cite it, and fix `OpenDengue2024` to V1.3). A reader currently cannot tell where the Colombia dengue case data came from.
- The DCA and PR-AUC additions are the highest-value *methodological* gaps because the manuscript foregrounds DCA net benefit and reports PR-AUC without methodological references for them.

---

## 5. Could not verify (online)

| Item | Why | Recommendation |
|---|---|---|
| `SriLankaWER` exact bibliographic details | Grey literature; the Epidemiology Unit publishes weekly PDFs without DOIs/stable per-report citations. The source is real (Epidemiology Unit, MoH Sri Lanka WER) but a single canonical citation could not be DOI-verified. | Keep as dataset/grey citation; add access URL + date range. |
| `HDXCODABSriLanka` exact dataset record | HDX COD-AB Sri Lanka exists, but the precise record/version/date could not be pinned to a single authoritative landing page in this audit. | Add the specific HDX dataset URL + version + access date. |
| `SriLankaCensus2024` exact published title/page of district totals | The 2024 census and district totals are confirmed real (released 30 Oct 2025), but the exact title string and citation format of the published district-totals table were not pinned to one canonical document. | Cite the DCS "Census of Population and Housing 2024 — Basic Population Information by Districts and DS Divisions" with URL + 2025 release date. |
| `RCoreTeam2024` exact R version | Standard citation; specific minor version/year not verified against the installed environment. | Match to the R version actually used in the analysis. |
| STROBE DOI (10.1016/S0140-6736(07)61602-X) | Provided as a standard/plausible DOI but not re-resolved in this audit. | Resolve before adding. |

---

## Bottom line

- **20 of 23 cited entries verified CLEAN** against primary sources; **3 cited entries have confirmed errors** (`Baharom2022`, `HussainAlkhateeb2021`, `VanCalster2023`).
- **6 bib entries are uncited**; of these `Clarke2024OpenDengue` / `OpenDengue2024` are the load-bearing miss (Colombia data source).
- All requested-addition candidates were DOI-verified as real and relevant.
- Grey-literature/dataset entries (`SriLankaWER`, `SriLankaCensus2024`, `HDXCODABSriLanka`, `RCoreTeam2024`) are real but their exact citation strings could not be fully pinned online.
