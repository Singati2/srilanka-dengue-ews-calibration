# Referee-Response Matrix — Adversarial Peer Review (`dengue_ews_peer_review.md`)

*Read-only decision artifact for author + PI. Each knockout triaged against the verified files (v18 / validity-corrected candidate / frozen Path-B outputs). Nothing recomputed, staged, or committed. Disposition legend: **ACCEPT-FIX** (valid, act on it) · **DONE** (already handled in the corrected candidate) · **CONTEST** (defensible pushback) · **DEFER** (Paper 2 / out of scope).*

**Bottom line:** the review's core knockouts are factually accurate against our own text and cannot be rebutted on facts. The paper's problem is **framing** (a null primary sold as "beyond surveillance"), not fabrication. The honest, review-surviving move is the reviewer's **Option A** (negative/methodological reframe), which is convergent with our Six Hats + Path B trajectory.

---

## A. Primary knockouts (review §3, ranked)

| # | Knockout | Valid? | Status in corrected candidate | Disposition | Concrete action |
|---|---|---|---|---|---|
| K1 | Primary estimand SL M4−M1 = −0.008 (CI crosses 0); conclusions ride on non-primary M5/Colombia → outcome-switching + title–finding mismatch | **Yes** (verified: candidate prints M4−M1 −0.008 as planned primary) | Partial — candidate is honest that M4 is primary/null and M5 is sensitivity, but title/abstract still imply "beyond surveillance" | **ACCEPT-FIX** | Retitle (drop "beyond surveillance"); lead Abstract/Discussion with M1 dominance + the matched null; present positive shards as shards |
| K2 | Isolated climate +0.0078 fails the authors' own ±0.005 band (lower CI 0.0039 < 0.005) | **Yes** (verified) | **DONE** — candidate states CI "included values below the internal +0.005 reference level" | ACCEPT (tighten) | Stop calling it "value retained"; say "did not clear a permissive self-chosen band" |
| K3 | Uncontrolled multiplicity; only SL "win" at p\*=0.40 and grows monotonically with threshold → prevalence/threshold artifact | **Yes** | Partial — labeled exploratory, unadjusted noted | **ACCEPT-FIX** | Declare ONE primary contrast; everything else explicitly exploratory/FDR; state the monotone-threshold pattern is prevalence-linked, not climate |
| K4 | Undefended p\*=0.30 (not elicited/cost-derived) — whole NB apparatus floats on it | **Yes** (candidate concedes verbatim) | Partial — grid + implied cost ratio only | **ACCEPT-FIX** | Add a threshold-averaged NB summary **from the existing frozen DCA grid (0.05–0.50), no refit**; report robustness range. (AUNBC needs pre-stated weights — see validity verdict) |
| K5 | Only clean positive (Colombia) sits in COVID 2020–2022; 2022-only (+0.0150) doesn't rescue | Partial-Yes | Partial — 2022-only present; "not pandemic-free" stated | **ACCEPT-FIX** | Foreground plainly that Colombia may be a pandemic artifact; note the matched climate increment is small regardless |
| K6 | No contribution once novelty disclaimed (DCA is 2006; "recent cases are a strong baseline" is textbook) | **Contestable** (adversarial opinion) | n/a | **CONTEST via Option A** | Reframe the contribution as the *evaluation + matched-baseline-confound* lesson — underused in dengue EWS |

## B. Reviewer-specific points

| # | Point | Valid? | Status | Disposition | Action |
|---|---|---|---|---|---|
| B1 | Near-circular outcome: exceedance label built from the same counts feeding M1's lags → M1 dominance partly built in | **Yes, sharp** | Not explicit | **ACCEPT-FIX** (add limitation) — but note it *also* supports "surveillance is a demanding benchmark" | Add a limitation on label–predictor shared source |
| B2 | Elevated-activity flagging (~⅓ weeks; 23.5% at 90th), not outbreak warning | Yes | **DONE** — candidate reclassifies to "elevated-activity alerting" | ACCEPT | — |
| B3 | Motivating EWARS-csd ≠ the M1 logistic baseline | Yes | **DONE** — candidate states M1 is a locally refit model, not EWARS-csd | ACCEPT | — |
| C1 | Two "replications" are different models (SL DLNM+humidity vs Colombia linear, no humidity, diff. penalty); no heterogeneity test | **Yes** (verified: SL has cross-basis+humidity; Colombia table lacks humidity) | Partial — settings-differ conceded | **ACCEPT-FIX** | Stop calling it "replication" or harmonize (harmonize = Paper 2); state the asymmetry explicitly |
| C3 | Flat/decaying Colombia horizon → h=4 increment is structure/overfit, not climate lead-time | **Yes** (aligns with our decomposition) | Partial — flat horizon reported | **ACCEPT-FIX** | Explicitly connect the flat horizon to the matched decomposition (the increment is department structure) |
| D1 | Declarations empty (ethics/funding/CoI/contributions/repo/PID/license "pending") | **Yes** (verified) | Open blockers | **ACCEPT-FIX** (admin) | Fill all declarations before submission |
| D2 | Not reproducible: Python versions + per-model mean predicted probabilities not retained | **Yes** | Open | **ACCEPT-FIX** (repro) | Disclose/preserve versions; state mean-pred-prob gap |
| D3 | Pre-specification self-attested (no public registration) | **Yes** | Partial — "no prospective public registration" stated | **ACCEPT-FIX** | Publicly timestamp / OSF the analysis plan |

## C. Secondary points

| Point | Valid? | Status | Disposition |
|---|---|---|---|
| 8-cluster bootstrap CIs treated as evidence | Yes | **DONE** (flagged imprecise/exploratory) | ACCEPT |
| No power/precision analysis | Yes | Not done | ACCEPT-FIX (add precision statement) |
| Single temporal holdout ("hypothesis-generating") | Yes | **DONE** (stated) | ACCEPT / rolling-origin+spatial = **DEFER** (P2) |
| MAUP / change-of-support | Yes | **DONE** (limitation) | ACCEPT |
| SL M5−M1 also crosses zero (+0.0081) | Yes | **DONE** | ACCEPT |

---

## D. Strategic decision (author + PI)

| Option | What it is | Cost | Survives this reviewer? | Recommendation |
|---|---|---|---|---|
| **A** (reviewer-recommended) | Flip to a negative/methodological result: "standard EWS evaluation overstates climate value; benchmark against recent surveillance + match structure + judge by calibration/NB → climate's standalone value collapses and its isolated increment fails a permissive band." Retitle, lead with the null. | Medium (reframe; author/PI sign-off) | **Yes** | **Recommended.** Convergent with Six Hats + Path B; converts every weakness into evidence; achievable from existing numbers |
| **B** | Shrink to one bulletproof confirmatory analysis: one setting, one pre-registered primary, one justified threshold (or threshold-averaged NB), rolling-origin + spatial-block CV; matched baseline as the **default** comparator; everything else appendix | High (new validation runs = partly Paper 2) | Yes | Viable alternative; more work; some pieces are Paper 2 |
| **C** | Keep a positive climate claim | Very high | No | Requires real-time vintages, nowcasting, non-pandemic window, elicited threshold, public pre-registration = a **new study (Paper 2)** |

## E. Punch-list status (either option)
- Pre-register / public timestamp — **OPEN**
- Make M5_no-climate the *default* comparator — **PARTIAL** (it's a diagnostic in the candidate; A/B want it primary)
- Justify/replace p\* or threshold-averaged NB — **OPEN** (frozen DCA grid enables this with no refit)
- Real multiplicity structure — **OPEN**
- Quarantine 2020–2021 harder / call Colombia a possible artifact — **PARTIAL**
- Harmonize climate or drop "replication" — **OPEN**
- Fill declarations; preserve versions + mean-pred-prob — **OPEN**
- Reconcile title with finding — **PARTIAL** (softened; A wants "beyond surveillance" dropped)

## F. Recommendation
1. **Decide direction first (this matrix):** adopt **Option A**. It is the honest, review-surviving framing and matches our own converging analysis.
2. **Then execute** an Option-A candidate (retitle; lead with the null; matched baseline as default comparator; positives as shards) — a larger reframe than the validity correction, requiring author/PI sign-off.
3. **Cheap wins available now, no model recompute:** threshold-averaged NB from the frozen DCA grid (K4); the interaction-CI + Shapley from the saved bootstrap distribution; connect flat-horizon to the decomposition (C3).
4. **Admin/repro track (D1–D3)** runs in parallel and gates submission regardless of framing.

*Advisory. No manuscript, frozen output, or repository state was modified; nothing staged, committed, or pushed.*
