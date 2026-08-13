"""Stage the Sri Lanka ERA5 0.25 deg window, 2018-2025, hourly t2m + d2m, from ARCO-ERA5 raw.

Anonymous (no CDS key). Resumable: one .npz per (year, variable); re-running skips what exists.
"""
import sys, time, warnings
from pathlib import Path
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.path.insert(0, str(Path(__file__).parent))
import srilanka_era5_window_reader_v1 as E

OUT = Path("/Users/mpcr/aj/Dengue/srilanka-dengue-ews-calibration/"
           "data_quarantine/wp5_exposure/era5_0p25_window")
OUT.mkdir(parents=True, exist_ok=True)

VARS = {"2m_temperature": "t2m", "2m_dewpoint_temperature": "d2m"}
YEARS = [int(y) for y in sys.argv[1:]] or list(range(2018, 2026))
I0, I1, J0, J1 = E.lat_lon_index(10.0, 5.8, 79.5, 82.0)
WORKERS = 10


def session():
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.5,
                                                      status_forcelist=[429, 500, 502, 503, 504]),
                                    pool_maxsize=WORKERS * 2))
    return s


def one_day(args):
    d, folder, var = args
    s = TL.s if hasattr(TL, "s") else None
    if s is None:
        s = TL.s = session()
    url = E.BASE % (d.year, d.month, d.day, folder)
    return E.read_window(s, url, var, I0, I1, J0, J1)


import threading
TL = threading.local()

for year in YEARS:
    for folder, var in VARS.items():
        f = OUT / f"era5_0p25_{var}_{year}.npz"
        if f.exists():
            print(f"{year} {var}  cached", flush=True)
            continue
        days = [date(year, 1, 1) + timedelta(days=i)
                for i in range((date(year + 1, 1, 1) - date(year, 1, 1)).days)]
        t0 = time.time()
        with ThreadPoolExecutor(WORKERS) as ex:
            arrs = list(ex.map(one_day, [(d, folder, var) for d in days]))
        A = np.concatenate(arrs, axis=0).astype("float32")     # (hours, 18, 11)
        np.savez_compressed(f, data=A,
                            dates=np.array([d.isoformat() for d in days]),
                            window=np.array([I0, I1, J0, J1]))
        print(f"{year} {var}  {A.shape}  {time.time()-t0:6.1f}s  "
              f"{A.min()-273.15:6.2f}..{A.max()-273.15:6.2f} degC", flush=True)

print("DONE", flush=True)
