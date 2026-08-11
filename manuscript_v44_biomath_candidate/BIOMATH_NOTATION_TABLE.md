# BIOMATH_NOTATION_TABLE

Notation used in the biomath candidate's *Mathematical and decision-analytic framework* (Section~"Materials and methods"). Every symbol maps to an object that already exists in the canonical v44 manuscript; **no symbol denotes a newly estimated quantity.**

| Symbol | Meaning | Empirical object (canonical v44) |
|---|---|---|
| $i$ | spatial unit | RDHS division (Sri Lanka, 26) / municipality (Colombia) |
| $t$ | forecast-origin week | epidemiological week |
| $h$ | forecast horizon | primary $h=4$; sensitivities $h=1,2,8,12$ |
| $\tau_i$ | unit alert threshold | training-period 75th percentile of weekly incidence (90th = sensitivity) |
| $Y_{i,t+h}$ | future elevated-activity indicator | $\mathbf 1\{\text{incidence}_{i,t+h}>\tau_i\}$; date-based join |
| $\mathcal I^{S}_{it}$ | recent-surveillance information by week $t$ | recent-incidence lags (+ seasonal harmonics + RDHS FE in SL M1) |
| $\mathcal I^{C}_{it}$ | climate information by week $t$ | ERA5-Land/CHIRPS climate feature block |
| $\mathcal I^{H}=\mathcal I^{SC}$ | hybrid information | $\mathcal I^{S}\cup\mathcal I^{C}$ (realized by M5 vs its matched no-climate comparator) |
| $\mathcal I^{G},\mathcal I^{SG}$ | geomatics / surveillance+geomatics info | **pending** M6 workstream; mentioned only in a Discussion note, not in the main framework |
| $p^{(m)}_{it}$ | predicted alert probability | $P(Y_{i,t+h}=1\mid\mathcal I^{(m)}_{it})$, fitted-model output |
| $\widetilde p^{(m)}_{it}$ | recalibrated probability | $\operatorname{logit}^{-1}[\alpha_t+\beta_t\operatorname{logit}(p_{it})]$; SL rolling intercept-only, CO Platt |
| $\alpha_t,\beta_t$ | recalibration intercept/slope | primary fixes $\beta_t=1$ (intercept-only) |
| $p^*$ | decision threshold | illustrative $p^*=0.30$; grid reported |
| $\delta_{p^*}(p),\,a^{(m)}_{it}$ | decision rule / alert action | $\mathbf 1\{p\ge p^*\}$ |
| $\pi$ | test-set alert prevalence | 0.336 (SL test), 0.375 (CO test); 24.2% SL train |
| $\mathrm{TP},\mathrm{FP},N$ | true/false positive counts, sample size | alert counts; unit-weeks evaluated |
| $\mathrm{NB}(p^*)$ | net benefit | $\frac{\mathrm{TP}}{N}-\frac{\mathrm{FP}}{N}\frac{p^*}{1-p^*}$ (Vickers DCA sense) |
| $\mathrm{NB}_{\mathrm{all}}$ | alert-all net benefit | $\pi-(1-\pi)\frac{p^*}{1-p^*}$; $=0\iff p^*=\pi$ |
| $V_k$ | oriented value functional (larger = better) | $V_{\mathrm{AUC}}{=}\mathrm{AUC}$, $V_{\mathrm{NB}}{=}\mathrm{NB}$, $V_{\mathrm{Brier}}{=}{-}\mathrm{Brier}$, $V_{\mathrm{NLL}}{=}{-}\mathrm{NLL}$ |
| $\Delta V_{C,k}$ | metric-specific incremental climate value | $V_k(\mathcal I^{SC})-V_k(\mathcal I^{S})$; matched ablation M5$-$M5$_{\text{no-climate}}$ |
| $\Delta\mathrm{NB}_C$ | incremental climate net benefit | $\mathrm{NB}_{SC}-\mathrm{NB}_S$; e.g. SL $+0.0087$ raw / $+0.0157$ recal, CO $+0.0078$ |
| $\Delta\mathrm{NLL},\Delta\mathrm{Brier}$ | paired proper-score differences | full $-$ no-climate; negative favors climate |
| $\Delta V_G$ | incremental geomatics value | $V(\mathcal I^{SG})-V(\mathcal I^{S})$ — **PENDING / NOT ESTIMATED** |
| $\tau_{\mathrm{avail}}(X_j)$ | availability time of item $X_j$ | admissibility: $X_j\in\mathcal I_t \iff \tau_{\mathrm{avail}}(X_j)\le t$ (σ-algebra/filtration notation removed in tightening) |
| $r,\,d(r),\,w(d(r))$ | WER issue number / reporting date / ISO week | date-aligned surveillance join (vs naive $r=w$) |
| $\mathcal A_w[X](D_i,t)$ | spatial exposure operator (Discussion note only) | $\int_{D_i}w X/\int_{D_i}w$; $w{=}1$ area-mean **used**; $w{=}P(s)$ pop-weight **pending (WP5)** |
| $\Delta V_G$ | incremental geomatics value (Discussion note only) | $V(\mathcal I^{SG})-V(\mathcal I^{S})$ — **PENDING / NOT ESTIMATED** |
| $D^{(b)}\to\hat f^{(b)}\to\hat p^{(b)}\to\Delta^{(b)}$ | development-inclusive resample | refit-both-models bootstrap ($B{=}1000$, seed 20260612) |

Conventions: signs follow the manuscript (negative $\Delta$NLL/$\Delta$Brier favor climate; positive $\Delta$NB favors the hybrid). "Pending" items are framework-only and carry no number.
