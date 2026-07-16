# Reconstruction environment (V6 + Phase-2 analysis)
The original V6 Python modeling-stack versions were NOT preserved. `requirements-lock.txt`
(`pip freeze`, Python 3.10.12) pins the RECONSTRUCTION environment under which the committed
pipelines reproduce the manuscript numbers via their reproduce-gates (Colombia matched point
+0.00783 vs frozen +0.00786; Colombia M5_recal fidelity 1.1e-16; Sri Lanka M1/M4/M5 <1e-6).
This makes the numbers RECONSTRUCTION-reproducible, not bit-identical to the original run.
Key libraries: numpy 1.26.4, pandas 2.1.3, scikit-learn 1.7.2, scipy 1.11.4, statsmodels 0.14.6,
patsy 1.0.2. R comparator: R 4.6.0; dlnm 2.4.10; mgcv 1.9.4; tsModel 0.6-2.
