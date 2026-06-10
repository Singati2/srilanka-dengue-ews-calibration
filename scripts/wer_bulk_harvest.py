#!/usr/bin/env python3
"""WER bulk harvester (2018-2025 ONLY). Quarantined.
Harvests issue URLs from the RENDERED listing (never constructs blindly),
handles both URL schemes, downloads, verifies mime=application/pdf, stores raw
read-only, records a manifest. Tries alternate suffixes for the 2022 w44 gap.
NOT pre-2018. NOT exposure. NOT models."""
import re, subprocess, csv, hashlib, os
from concurrent.futures import ThreadPoolExecutor

RETRIEVAL_DATE = "2026-06-10"
LISTING_URL = "https://www.epid.gov.lk/weekly-epidemiological-report"
VOLYEAR = {45:2018,46:2019,47:2020,48:2021,49:2022,50:2023,51:2024,52:2025}
RAW = "raw_bulk"

def get_listing():
    return subprocess.run(["curl","-sL","--max-time","60",LISTING_URL],
                          capture_output=True, text=True).stdout

def harvest_urls(html):
    urls = set(re.findall(
        r"https://www\.epid\.gov\.lk/storage/post/pdfs/[^\"'\s]*?[Vv]ol_\d+_no_\d+[^\"'\s]*?\.pdf",
        html))
    cand = {}
    for u in urls:
        m = re.search(r"[Vv]ol_(\d+)_no_(\d+)", u)
        vol, iss = int(m.group(1)), int(m.group(2))
        if vol in VOLYEAR and 1 <= iss <= 53:
            cand.setdefault((VOLYEAR[vol], vol, iss), []).append(u)
    # 2022 week 44 known listing gap -> try alternate suffixes explicitly
    if (2022,49,44) not in cand:
        b = "https://www.epid.gov.lk/storage/post/pdfs/"
        cand[(2022,49,44)] = [b+"vol_49_no_44-english.pdf",
                              b+"vol_49_no_44-english_1.pdf",
                              b+"vol_49_no_44-english_2.pdf"]
    return cand

def is_pdf(path):
    if not (os.path.exists(path) and os.path.getsize(path) > 10000):
        return False
    mt = subprocess.run(["file","-b","--mime-type",path],
                        capture_output=True,text=True).stdout.strip()
    return mt == "application/pdf"

def fetch(item):
    (year, vol, iss), urls = item
    outdir = os.path.join(RAW, str(year)); os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f"Vol_{vol}_no_{iss:02d}.pdf")
    for u in urls:
        subprocess.run(["curl","-sL","--max-time","90",u,"-o",out],
                       capture_output=True)
        if is_pdf(out):
            h = hashlib.sha256(open(out,"rb").read()).hexdigest()
            return dict(year=year, vol=vol, issue=iss, url=u, outfile=out,
                        sha256=h, bytes=os.path.getsize(out),
                        retrieval_date=RETRIEVAL_DATE, status="ok")
        if os.path.exists(out):
            os.remove(out)
    return dict(year=year, vol=vol, issue=iss, url=(urls[0] if urls else ""),
                outfile="", sha256="", bytes=0,
                retrieval_date=RETRIEVAL_DATE, status="MISSING")

def main():
    os.makedirs(RAW, exist_ok=True)
    cand = harvest_urls(get_listing())
    items = sorted(cand.items())
    print(f"harvested {len(items)} unique (year,vol,issue) keys for 2018-2025")
    manifest = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(fetch, items):
            manifest.append(rec)
    manifest.sort(key=lambda r:(r["year"],r["issue"]))
    # lock raw read-only
    for r in manifest:
        if r["status"]=="ok" and os.path.exists(r["outfile"]):
            os.chmod(r["outfile"], 0o444)
    with open(os.path.join(RAW,"harvest_manifest.csv"),"w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year","vol","issue","url","outfile",
                            "sha256","bytes","retrieval_date","status"])
        w.writeheader(); w.writerows(manifest)
    ok = sum(r["status"]=="ok" for r in manifest)
    miss = [(r["year"],r["issue"]) for r in manifest if r["status"]!="ok"]
    print(f"downloaded OK: {ok}/{len(manifest)}")
    print(f"missing: {miss}")
    print("manifest:", os.path.join(RAW,"harvest_manifest.csv"))

if __name__ == "__main__":
    main()
