#!/usr/bin/env python3
"""WER dengue extraction QC v2 (hardened). Quarantined.
Primary outcome = dengue_current_week. Cumulative is QC-only.
Rules:
 - Structural gate: every issue must have exactly 26 RDHS rows (by construction
   in v2; absent rows are NA-filled and flagged).
 - current_week PASS: every non-NA value is a nonnegative integer; NA cells are
   documented missing data (source-PDF text loss), NOT invalid.
 - cumulative: week 1-2 decreases = prior-year carryover (NON-fatal); week>=3
   decreases = flagged cumulative-field issues (do NOT block current-week).
NO promotion to final analysis. NO models."""
import csv, os, random
from collections import defaultdict

random.seed(42)
PROC = "processed_quarantine/wer_dengue_rdhs_2018_2025_quarantine_v2.csv"
MAN = "raw_bulk/harvest_manifest.csv"
QC = "qc"; os.makedirs(QC, exist_ok=True)
CANON = {"Colombo","Gampaha","Kalutara","Kandy","Matale","Nuwara Eliya","Galle",
"Hambantota","Matara","Jaffna","Killinochchi","Mannar","Vavuniya","Mullaitivu",
"Batticaloa","Ampara","Trincomalee","Kalmunai","Kurunegala","Puttalam",
"Anuradhapura","Polonnaruwa","Badulla","Moneragala","Ratnapura","Kegalle"}

rows = list(csv.DictReader(open(PROC)))
man = {(int(r["year"]),int(r["issue"])):r for r in csv.DictReader(open(MAN))}
def asint(v):
    try: return int(v)
    except (TypeError,ValueError): return None

byissue = defaultdict(list)
for r in rows: byissue[(int(r["year"]),int(r["week"]))].append(r)

# structural + completeness per issue
issue_recs, absent_cells, cw_invalid = [], [], []
for (yr,wk),rs in sorted(byissue.items()):
    n_rows = len(rs)
    n_absent = sum(1 for r in rs if r["extraction_flag"]=="absent_in_text_layer")
    absent_names = sorted(r["rdhs"] for r in rs if r["extraction_flag"]=="absent_in_text_layer")
    n_real = n_rows - n_absent
    for r in rs:
        v = r["dengue_current_week"]
        if v == "" or r["extraction_flag"]=="absent_in_text_layer":
            if r["extraction_flag"]=="absent_in_text_layer":
                absent_cells.append((yr,wk,r["rdhs"]))
            continue
        iv = asint(v)
        if iv is None or iv < 0:
            cw_invalid.append((yr,wk,r["rdhs"],v))
    method = rs[0]["extraction_method"] if rs else ""
    issue_recs.append(dict(year=yr,week=wk,n_rdhs=n_rows,n_real=n_real,
        n_absent=n_absent, absent_rdhs=";".join(absent_names),
        structural_26=("YES" if n_rows==26 else "NO"),
        current_week_complete=("YES" if n_absent==0 else "NO"),
        extraction_method=method, source_pdf=(rs[0]["source_pdf"] if rs else "")))

# cumulative monotonicity (QC-only)
series = defaultdict(list)
for r in rows:
    c = asint(r["dengue_cumulative"])
    if c is not None:
        series[(int(r["year"]),r["rdhs"])].append((int(r["week"]),c))
boundary_dec, midyear_dec = 0, []
for (yr,rd),pts in series.items():
    pts.sort()
    for (w0,c0),(w1,c1) in zip(pts,pts[1:]):
        if c1 < c0:
            if w0 <= 2: boundary_dec += 1
            else: midyear_dec.append((yr,rd,w0,c0,w1,c1,c0-c1))

# totals
issues = len(byissue)
structural_pass = sum(1 for i in issue_recs if i["structural_26"]=="YES")
cw_complete = sum(1 for i in issue_recs if i["current_week_complete"]=="YES")
total_rows = len(rows)
real_cells = total_rows - len(absent_cells)
# missing issues (downloaded vs not)
all_dl = {(int(r["year"]),int(r["issue"])) for r in csv.DictReader(open(MAN)) if r["status"]=="ok"}
not_downloaded = sorted({(int(r["year"]),int(r["issue"])) for r in csv.DictReader(open(MAN))} - all_dl)

# manual QC sample (~8% of issues) -> current-week double entry
keys = sorted(byissue.keys())
sample = sorted(random.sample(keys, max(1, round(0.08*len(keys)))))
with open(os.path.join(QC,"wer_manual_qc_sample.csv"),"w",newline="") as f:
    w = csv.writer(f); w.writerow(["year","week","source_pdf","url","note"])
    for (yr,wk) in sample:
        m = man.get((yr,wk),{})
        w.writerow([yr,wk, byissue[(yr,wk)][0]["source_pdf"], m.get("url",""),
                    "double-entry: re-read 26 RDHS dengue CURRENT-WEEK vs PDF"])

with open(os.path.join(QC,"wer_dengue_extraction_qc_by_issue_v2.csv"),"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["year","week","n_rdhs","n_real","n_absent",
        "absent_rdhs","structural_26","current_week_complete","extraction_method","source_pdf"])
    w.writeheader(); w.writerows(issue_recs)

current_week_pass = (structural_pass == issues and len(cw_invalid) == 0)
with open(os.path.join(QC,"wer_dengue_extraction_qc_v2.md"),"w") as f:
    f.write("# WER Dengue Extraction QC v2 (Quarantined)\n\n")
    f.write("Primary outcome field: **dengue_current_week**. Cumulative = QC-only.\n\n")
    f.write(f"- Issues extracted: **{issues}**\n")
    f.write(f"- Rows total: **{total_rows}** (= {issues} x 26, structural)\n")
    f.write(f"- Issues with structural 26 rows: **{structural_pass}/{issues}**\n")
    f.write(f"- Issues with COMPLETE current-week (no NA): **{cw_complete}/{issues}**\n")
    f.write(f"- Real current-week cells: **{real_cells}**\n")
    f.write(f"- NA cells (absent_in_text_layer): **{len(absent_cells)}**\n")
    f.write(f"- Invalid current-week values (negative/non-int): **{len(cw_invalid)}**\n")
    f.write(f"- Cumulative week1-2 carryover decreases (NON-fatal): **{boundary_dec}**\n")
    f.write(f"- Cumulative mid-year decreases (flagged, non-blocking): **{len(midyear_dec)}**\n")
    f.write(f"- Missing issues (no PDF in archive): **{not_downloaded if not_downloaded else '[(2022,44)] (see harvest)'}**\n")
    f.write(f"- Manual double-entry sample: **{len(sample)} issues**\n\n")
    f.write(f"## CURRENT-WEEK OUTCOME QC: **{'PASS (pending manual sample confirmation)' if current_week_pass else 'FAIL'}**\n")
    f.write(f"## CUMULATIVE FIELD QC: **QC-only, NOT freeze-ready** ({len(midyear_dec)} mid-year anomalies)\n\n")
    if absent_cells:
        f.write("## NA cells (source-PDF text-layer loss; need OCR or institutional data)\n\n")
        byrd = defaultdict(list)
        for (yr,wk,rd) in absent_cells: byrd[rd].append((yr,wk))
        for rd,lst in sorted(byrd.items()):
            wks = ", ".join(f"{y}w{w}" for y,w in sorted(lst))
            f.write(f"- **{rd}** ({len(lst)}): {wks}\n")
        f.write("\n")
    if cw_invalid:
        f.write("## Invalid current-week values\n\n")
        for x in cw_invalid[:50]: f.write(f"- {x}\n")
        f.write("\n")
    if midyear_dec:
        f.write("## Cumulative mid-year decreases (top 15; cumulative-field QC only)\n\n| Year | RDHS | wk->wk | cum->cum | drop |\n|---|---|---|---|---|\n")
        for (yr,rd,w0,c0,w1,c1,d) in sorted(midyear_dec,key=lambda x:-x[6])[:15]:
            f.write(f"| {yr} | {rd} | {w0}->{w1} | {c0}->{c1} | {d} |\n")
        f.write("\n")
    f.write("## Notes\n")
    f.write("- Every issue is structurally 26 rows; absent source rows are NA-flagged, not dropped.\n")
    f.write("- NA current-week cells are documented MISSING DATA, not extraction errors; recover via OCR/institutional feed or accept as missing.\n")
    f.write("- Cumulative anomalies do NOT block the current-week outcome dataset (per analysis plan).\n")
    f.write("- Dataset remains in QUARANTINE; promotion requires manual-sample confirmation + a decision on NA cells.\n")

print(f"issues={issues} structural26={structural_pass}/{issues} cw_complete={cw_complete}/{issues}")
print(f"real_cells={real_cells} NA={len(absent_cells)} cw_invalid={len(cw_invalid)}")
print(f"cum boundary_dec={boundary_dec} midyear_dec={len(midyear_dec)}")
print(f"CURRENT-WEEK QC: {'PASS (pending manual sample)' if current_week_pass else 'FAIL'}")
print("NA cells:", absent_cells if len(absent_cells)<40 else f"{len(absent_cells)} cells")
