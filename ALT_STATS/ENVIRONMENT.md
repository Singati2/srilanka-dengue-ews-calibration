# ENVIRONMENT.md
- OS: Linux 6.8.0-124-generic
- Python: 3.10.12
- numpy 1.26.4 · pandas 2.1.3 · scikit-learn 1.7.2 · scipy 1.11.4 · statsmodels 0.14.6 · patsy 1.0.2
- RNG: numpy `default_rng` (PCG64); seed **20260612**; single-threaded percentile bootstrap.
- Full pip lock: `environment/requirements-lock.txt` (490 pkgs). OS detail: `environment/os.txt`.
- **Caveat:** V6 Python modeling-stack versions were not preserved; this is a reconstruction
  environment. Numerical reproduce-gates (SL <1e-6; Colombia M5_recal 1.11e-16) confirm the
  reconstruction reproduces the frozen V6 predictions despite unpinned original versions.
