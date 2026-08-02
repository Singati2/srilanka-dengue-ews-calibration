# Archive / release plan (v6) — author decisions required; nothing created

This plan distinguishes what *could* be released. **No repository, Zenodo record, DOI, or license has been created or chosen.** Platform, timing, identifier, and license all require author confirmation (M-7). No unconditional Zenodo promise appears in the manuscript.

| Component | Description | Release disposition | Notes |
|---|---|---|---|
| Analysis code | Modeling, linkage, DCA, bootstrap, recalibration scripts | Likely releasable | Author to confirm scope and license |
| Derived non-restricted artifacts | Frozen analysis tables / metric reports not bound by third-party redistribution terms | Likely releasable | Confirm each artifact's source terms first |
| Third-party source data | OpenDengue, CHIRPS, ERA5-Land, WorldPop, Sri Lanka WER | **Do not redistribute** | Provide by citation + documented fetch instructions only |
| Data-fetch instructions | Scripts/README describing how to obtain each source dataset and the exact version (e.g., OpenDengue Temporal extract V1.3) | Releasable | Replaces redistribution of restricted data |
| Environment information | R 4.6.0; dlnm 2.4.10; mgcv 1.9.4; tsModel 0.6-2 (verified). Python stack versions not preserved | Releasable (state "not preserved" for Python) | Do not guess unrecorded versions |
| License | e.g., code license + data-statement | **Author to choose** | Not selected |
| Archival platform | e.g., Zenodo / Dryad / institutional | **Author to choose** | Not selected; no record created |
| Release timing | e.g., upon acceptance | **Author to choose** | Not promised in the manuscript |
| Persistent identifier | DOI | **Pending** | Assigned only after platform + deposit chosen |

**Manuscript data-availability wording (interim, internal):** "Public repository URL, release scope, license, archival platform, and persistent identifier require author confirmation." No platform/DOI/timing is asserted in the manuscript until chosen and verified.
