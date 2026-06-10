#!/usr/bin/env python3
"""WER bulk dengue extractor v2 (hardened). Quarantined, OUTCOME-ONLY.
Improvements over v1:
  - Relaxed table-header detection: 'RDHS  Dengue' (matches 'Dengue' OR
    'Dengue Fever') -> recovers the 3 zero-row PDFs.
  - Fallback extractor: when pdftotext -layout yields <26 RDHS, retry with
    plain pdftotext (no -layout) and merge any newly-found RDHS.
  - Structural completeness: emit EXACTLY 26 rows/issue; canonical RDHS not
    found in ANY text method are emitted as NA with flag 'absent_in_text_layer'
    (genuine source-PDF text loss; needs OCR / institutional data).
Primary outcome field = dengue_current_week. Cumulative retained for QC only.
NO climate linkage. NO models. Output stays in quarantine."""
import subprocess, re, csv, os

RAW = "raw_bulk"; OUTDIR = "processed_quarantine"
MANIFEST = os.path.join(RAW, "harvest_manifest.csv")
OUT = os.path.join(OUTDIR, "wer_dengue_rdhs_2018_2025_quarantine_v2.csv")

CANON = ["Colombo","Gampaha","Kalutara","Kandy","Matale","Nuwara Eliya","Galle",
"Hambantota","Matara","Jaffna","Killinochchi","Mannar","Vavuniya","Mullaitivu",
"Batticaloa","Ampara","Trincomalee","Kalmunai","Kurunegala","Puttalam",
"Anuradhapura","Polonnaruwa","Badulla","Moneragala","Ratnapura","Kegalle"]
def _norm(s): return re.sub(r"[^a-z]","",s.lower())
NORM = {_norm(c): c for c in CANON}
ALIAS = {"kalmune":"Kalmunai","monaragala":"Moneragala","kilinochchi":"Killinochchi"}
name_re = re.compile(r"^([A-Za-z][A-Za-z .'\-]*?)\s+(\d.*)$")
HEADER_RE = re.compile(r"RDHS\s+Dengue", re.I)   # relaxed: Dengue or Dengue Fever

def match_rdhs(cand):
    n = _norm(cand)
    if len(n) < 4: return None
    if n in NORM: return NORM[n]
    if n in ALIAS: return ALIAS[n]
    for k,c in NORM.items():
        if k.startswith(n) or n.startswith(k): return c
    for a,c in ALIAS.items():
        if a.startswith(n) or n.startswith(a): return c
    return None

def parse_text(txt):
    """Return {rdhs: (current_week, cumulative)} from a pdftotext dump."""
    found, in_table = {}, False
    for ln in txt.splitlines():
        s = ln.strip()
        if HEADER_RE.search(ln):
            in_table = True; continue
        if "RDHS Divisions:" in ln or s.startswith("Sri Lanka"):
            in_table = False
        if not in_table: continue
        m = name_re.match(s)
        if not m: continue
        name = match_rdhs(m.group(1))
        if name is None or name in found: continue
        ints = re.findall(r"-?\d+", m.group(2))
        if len(ints) >= 2:
            found[name] = (int(ints[0]), int(ints[1]))
        elif len(ints) == 1:
            found[name] = (int(ints[0]), None)
    return found

def extract_issue(path):
    """Primary -layout; fallback plain pdftotext if <26. Returns (found, method)."""
    lay = subprocess.run(["pdftotext","-layout",path,"-"],
                         capture_output=True,text=True).stdout
    found = parse_text(lay); method = "layout"
    if len(found) < 26:
        plain = subprocess.run(["pdftotext",path,"-"],
                               capture_output=True,text=True).stdout
        extra = parse_text(plain)
        added = False
        for k,v in extra.items():
            if k not in found:
                found[k] = v; added = True
        if added: method = "layout+plain_fallback"
    return found, method

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    with open(MANIFEST) as f:
        man = [r for r in csv.DictReader(f) if r["status"] == "ok"]
    rows = []
    for r in man:
        yr, wk, vol = int(r["year"]), int(r["issue"]), int(r["vol"])
        found, method = extract_issue(r["outfile"])
        for rd in CANON:                      # emit EXACTLY 26 rows/issue
            if rd in found:
                cw, cum = found[rd]
                flag = "ok" if cw is not None else "no_value"
            else:
                cw, cum, flag = None, None, "absent_in_text_layer"
            rows.append(dict(year=yr, week=wk, vol=vol, rdhs=rd,
                dengue_current_week=("" if cw is None else cw),
                dengue_cumulative=("" if cum is None else cum),
                source_pdf=os.path.basename(r["outfile"]),
                extraction_flag=flag, extraction_method=method))
    with open(OUT,"w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year","week","vol","rdhs",
            "dengue_current_week","dengue_cumulative","source_pdf",
            "extraction_flag","extraction_method"])
        w.writeheader(); w.writerows(rows)
    issues = {(x["year"],x["week"]) for x in rows}
    absent = [(x["year"],x["week"],x["rdhs"]) for x in rows if x["extraction_flag"]=="absent_in_text_layer"]
    print(f"issues: {len(issues)}  rows: {len(rows)} (expect {len(issues)*26})")
    print(f"absent_in_text_layer cells (NA): {len(absent)}")
    for a in absent: print("   NA:", a)
    print("output:", OUT)

if __name__ == "__main__":
    main()
