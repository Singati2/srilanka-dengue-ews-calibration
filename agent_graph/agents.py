"""The 11 deterministic audit agents + adversarial reviewer.

Convention: each agent returns dict(name, status, findings) where status in
{PASS, REVIEW, FAIL} and findings is a list of {severity, msg, evidence}.
severity in {critical, major, minor}. Deterministic; no LLM, no network.
"""
import os, re, glob, subprocess
from knowledge_graph import schema

PASS, REVIEW, FAIL = "PASS", "REVIEW", "FAIL"


def _read(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def _manuscript(g):
    return next((n for n in g["nodes"].values() if n["type"] == "Manuscript" and n.get("found")), None)


def _result_values(g):
    return g.get("meta", {}).get("result_values", {})


def _agg(findings, fail_on=("critical",), review_on=("major",)):
    sev = {f["severity"] for f in findings}
    if sev & set(fail_on):
        return FAIL
    if sev & set(review_on):
        return REVIEW
    return PASS


def _mk(name, findings, status=None):
    return {"name": name, "status": status or _agg(findings), "findings": findings}


# ---------- 11.1 Repository ----------
def repository_agent(g, repo):
    f = []
    tracked = subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True).stdout.split()
    absre = re.compile(r'/(Users|home)/[A-Za-z0-9._-]+/')
    hits = []
    for path in tracked:
        if path.endswith((".py", ".md", ".tex", ".txt", ".yml", ".yaml", ".cfg", ".toml")):
            for m in absre.finditer(_read(os.path.join(repo, path))):
                hits.append(f"{path}: {m.group(0)}")
    if hits:
        f.append({"severity": "major", "msg": f"{len(hits)} absolute machine-specific path(s) in tracked files (portability)",
                  "evidence": hits[:8]})
    if not os.path.exists(os.path.join(repo, "README.md")):
        f.append({"severity": "minor", "msg": "no root README.md", "evidence": []})
    proj = g["nodes"].get("Project:srilanka-dengue-ews-calibration", {})
    if proj.get("dirty"):
        f.append({"severity": "minor", "msg": "working tree dirty at audit time", "evidence": []})
    tags = [n for n in g["nodes"].values() if n["type"] == "GitTag"]
    for need in ["v6-analysis-frozen", "alt-stats-plan-v1", "alt-stats-results-v1", "alt-stats-results-v2"]:
        if not any(need in t["id"] for t in tags):
            f.append({"severity": "major", "msg": f"manuscript-cited tag missing: {need}", "evidence": []})
    return _mk("REPOSITORY DOCUMENTATION", f)


# ---------- 11.2 Data Provenance ----------
def data_provenance_agent(g, repo):
    f = []
    checks = [n for n in g["nodes"].values() if n["type"] == "Checksum"]
    if not checks:
        f.append({"severity": "major", "msg": "no *.sha256 checksum file found for frozen inputs", "evidence": []})
    # committed data (should be quarantined) — flag tracked csv/json data under analysis/
    tracked = subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True).stdout.split()
    leaked = [p for p in tracked if re.search(r'(analysis|ALT_STATS)/.*\.(csv|json)$', p)
              and "results" not in p and "provenance" not in p and "_provenance" not in p]
    if leaked:
        f.append({"severity": "major", "msg": f"{len(leaked)} data-like csv/json tracked under analysis/ (quarantine risk)",
                  "evidence": leaked[:8]})
    prov = [n for n in g["nodes"].values() if n["type"] == "Result" and "provenance" in n.get("path", "")]
    if prov:
        f.append({"severity": "minor", "msg": f"{len(prov)} provenance record(s) present", "evidence": [p["path"] for p in prov[:5]], "ok": True})
    return _mk("DATA PROVENANCE", [x for x in f if not x.get("ok")] or f)


# ---------- 11.3 Temporal Leakage ----------
def temporal_leakage_agent(g, repo):
    f = []
    for n in g["nodes"].values():
        if n["type"] == "Script" and n.get("leak_flags"):
            f.append({"severity": "critical", "msg": f"temporal-leakage red flag in {n['path']}",
                      "evidence": n["leak_flags"]})
    m = _manuscript(g)
    if m:
        src = _read(os.path.join(repo, m["path"]))
        if "no future climate" not in src and "past-only" not in src and "available at the forecast origin" not in src:
            f.append({"severity": "major", "msg": "manuscript does not explicitly state past-only / no-future-data availability", "evidence": []})
    return _mk("TEMPORAL LEAKAGE", f)


# ---------- 11.4 Spatial ----------
def spatial_agent(g, repo):
    f = []
    m = _manuscript(g)
    src = _read(os.path.join(repo, m["path"])) if m else ""
    # cluster-count consistency
    if "26 RDHS" in src or "26 RDHS units" in src:
        pass
    else:
        f.append({"severity": "minor", "msg": "Sri Lanka cluster count (26 RDHS) not clearly stated", "evidence": []})
    if "31 " in src and ("department" in src.lower()):
        pass
    if "Moran" not in src:
        f.append({"severity": "minor", "msg": "no residual spatial-autocorrelation (Moran's I) diagnostic referenced", "evidence": []})
    # 32 vs 31 department FE mismatch (known issue prompt s6)
    if "32 department" in src and "31 " in src:
        f.append({"severity": "minor", "msg": "manuscript mentions both 32 dept fixed-effect columns and 31 test departments — ensure this is explained",
                  "evidence": ["32 department fixed effects vs 31 analyzed test departments"]})
    return _mk("SPATIAL CONSISTENCY", f)


# ---------- 11.5 Statistical ----------
def statistical_agent(g, repo):
    f = []
    m = _manuscript(g)
    src = _read(os.path.join(repo, m["path"])) if m else ""
    # seeds/B consistency across scripts
    seeds = set()
    for n in g["nodes"].values():
        if n["type"] == "Script":
            seeds |= set(n.get("seeds", []))
    if len(seeds) > 3:
        f.append({"severity": "minor", "msg": f"{len(seeds)} distinct seeds across scripts", "evidence": sorted(seeds)})
    # DI-vs-conditional: manuscript should treat development-inclusive as primary robustness
    if "development-inclusive" in src and "conditional" in src:
        pass
    else:
        f.append({"severity": "major", "msg": "conditional vs development-inclusive distinction not clearly present", "evidence": []})
    # net-benefit significance-testing (Vickers 2023) discipline
    if re.search(r'significan\w* (net benefit|decision)', src, re.I):
        f.append({"severity": "major", "msg": "possible significance-testing language applied to net benefit (contested; Vickers 2023)",
                  "evidence": []})
    return _mk("MODEL SPECIFICATION", f)


# ---------- 11.6 Calibration ----------
def calibration_agent(g, repo):
    f = []
    m = _manuscript(g)
    src = _read(os.path.join(repo, m["path"])) if m else ""
    for term in ["calibration", "recalibrat", "CITL", "slope", "integrated calibration index"]:
        if term.lower() not in src.lower():
            f.append({"severity": "minor", "msg": f"calibration reporting term missing: {term}", "evidence": []})
    return _mk("CALIBRATION", f)


# ---------- 11.7 Reproducibility ----------
def reproducibility_agent(g, repo):
    f = []
    lock = glob.glob(os.path.join(repo, "**", "requirements-lock.txt"), recursive=True) + \
           glob.glob(os.path.join(repo, "**", "*requirements*lock*"), recursive=True)
    if not lock:
        f.append({"severity": "major", "msg": "no environment lockfile (requirements-lock.txt) found", "evidence": []})
    if not any(n["type"] == "Checksum" for n in g["nodes"].values()):
        f.append({"severity": "major", "msg": "no checksum file for frozen inputs/outputs", "evidence": []})
    seeded = [n for n in g["nodes"].values() if n["type"] == "Script" and n.get("seeds")]
    unseeded = [n for n in g["nodes"].values() if n["type"] == "Script" and not n.get("seeds")
                and "bootstrap" in n.get("path", "").lower()]
    if unseeded:
        f.append({"severity": "minor", "msg": f"{len(unseeded)} bootstrap script(s) without an inline seed token", "evidence": [n["path"] for n in unseeded[:5]]})
    return _mk("REPRODUCIBILITY", f)


# ---------- 11.8 Reference ----------
def reference_agent(g, repo):
    f = []
    m = _manuscript(g)
    if m:
        und = m.get("undefined_citations", [])
        if und:
            f.append({"severity": "critical", "msg": f"{len(und)} \\cite key(s) with no \\bibitem", "evidence": und[:10]})
        n_ref = len(m.get("bibitem_keys", []))
        dois = [n for n in g["nodes"].values() if n["type"] == "DOI"]
        if n_ref and len(dois) < n_ref * 0.5:
            f.append({"severity": "minor", "msg": f"only {len(dois)} DOIs for {n_ref} references (<50% DOI coverage)", "evidence": []})
    return _mk("REFERENCE INTEGRITY", f)


# ---------- 11.9 Claim (numeric traceability) ----------
def claim_agent(g, repo):
    f = []
    rv = _result_values(g)
    claims = [n for n in g["nodes"].values() if n["type"] == "NumericClaim"]
    # only trace "result-shaped" values (>=4 dp, i.e. effect estimates / CIs)
    traced, untraced = 0, []
    for c in claims:
        v = c["value"]
        if len(v.split(".")[-1]) < 4:
            continue
        key = v if v[0] in "+-" else "+" + v
        alt = v.lstrip("+")
        if v in rv or key in rv or alt in rv or ("+" + alt) in rv or ("-" + alt) in rv:
            traced += 1
        else:
            untraced.append(f"{v} (L{c['line']}: {c['context'][:70]})")
    n_eff = traced + len(untraced)
    if untraced:
        sev = "major" if len(untraced) > n_eff * 0.4 else "minor"
        f.append({"severity": sev, "msg": f"{len(untraced)}/{n_eff} 4-dp effect values not matched to a committed result file",
                  "evidence": untraced[:12]})
    f.append({"severity": "minor", "msg": f"{traced}/{n_eff} effect values traced to a result file/doc", "evidence": [], "ok": True})
    return _mk("RESULT TRACEABILITY", [x for x in f if not x.get("ok")] or f)


# ---------- 11.10 Manuscript Consistency ----------
def manuscript_consistency_agent(g, repo):
    f = []
    m = _manuscript(g)
    if not m:
        return _mk("MANUSCRIPT CONSISTENCY", [{"severity": "critical", "msg": "no manuscript source found", "evidence": []}])
    src = _read(os.path.join(repo, m["path"]))
    # contradiction: 'not computed' proper-score claim vs computed DI proper scores
    if "development-inclusive proper-score intervals were not computed" in src and "development-inclusive" in src:
        f.append({"severity": "critical", "msg": "contradiction: says DI proper-score intervals 'were not computed' but DI results appear present",
                  "evidence": ["retire the 'not computed' sentence"]})
    # public-repo claim (must be verified, not trusted)
    if m.get("claims_public_github"):
        f.append({"severity": "major", "msg": "manuscript asserts a public GitHub repo/commit — must be verified from a clean unauthenticated environment before submission",
                  "evidence": ["repository availability claim"]})
    # duplicate numeric value stated with conflicting neighbors (weak contradiction heuristic)
    if m.get("em_dashes", 0) > 0:
        f.append({"severity": "minor", "msg": f"{m['em_dashes']} em-dash(es) present (AI-writing tell / style)", "evidence": []})
    aw = m.get("abstract_words")
    if aw and aw > 300:
        f.append({"severity": "major", "msg": f"abstract is {aw} words (>300 PLOS limit)", "evidence": []})
    return _mk("MANUSCRIPT CONSISTENCY", f)


# ---------- 11.11 Adversarial Reviewer + submission declarations ----------
_NEGATIONS = ("no ", "not ", "never", "cannot", "can't", "without", "neither",
              "does not", "did not", "claim no", "make no", "rather than", "avoid")


def _is_negated(text, pos, window=70):
    """True if an overclaim term at `pos` sits in a disclaimer/negated context."""
    ctx = text[max(0, pos - window):pos].lower()
    return any(neg in ctx for neg in _NEGATIONS)


def adversarial_reviewer(g, repo):
    f = []
    m = _manuscript(g)
    src = _read(os.path.join(repo, m["path"])) if m else ""
    low = src.lower()
    for term in schema.OVERCLAIM_TERMS:
        # word-boundary match so 'proves' does not fire inside 'improves'
        for mm in re.finditer(r'\b' + re.escape(term), low):
            i = mm.start()
            if _is_negated(low, i):        # disclaimer, e.g. "we claim no causal climate effects"
                continue
            f.append({"severity": "major",
                      "msg": f"possible overclaim (non-negated context): '{term}'",
                      "evidence": [src[max(0, i - 55):i + len(term) + 15].replace("\n", " ")]})
    return _mk("ADVERSARIAL REVIEW", f)


def submission_declarations_agent(g, repo):
    f = []
    m = _manuscript(g)
    ph = m.get("placeholders", []) if m else []
    total = sum(p["count"] for p in ph)
    if total:
        f.append({"severity": "critical", "msg": f"{total} unresolved placeholder(s) (author-supplied fields block submission)",
                  "evidence": [f"{p['marker']} x{p['count']}" for p in ph]})
    # license quality
    lic = os.path.join(repo, "LICENSE")
    if os.path.exists(lic):
        txt = _read(lic)
        if not any(k in txt for k in ["MIT", "Apache", "BSD", "GPL", "CC-BY", "Creative Commons"]):
            f.append({"severity": "major", "msg": "LICENSE present but no recognized SPDX license text (NOASSERTION risk)", "evidence": []})
    else:
        f.append({"severity": "major", "msg": "no LICENSE file", "evidence": []})
    return _mk("SUBMISSION DECLARATIONS", f)


ALL_AGENTS = [
    repository_agent, data_provenance_agent, temporal_leakage_agent, spatial_agent,
    statistical_agent, calibration_agent, reproducibility_agent, reference_agent,
    claim_agent, manuscript_consistency_agent, adversarial_reviewer,
    submission_declarations_agent,
]
