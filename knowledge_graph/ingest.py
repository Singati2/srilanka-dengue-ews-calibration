"""Deterministic ingestion of the repository into a project knowledge graph.

Stdlib only. Every node/edge carries provenance (source file + why) so a downstream
query can explain any finding. No network, no LLM.
"""
import os, re, json, subprocess, hashlib, glob
from . import schema

NUM_RE = re.compile(r'[+\-]?\d+\.\d{2,5}')                       # signed decimals (result values)
CI_RE = re.compile(r'([+\-]?\d+\.\d{2,5})\s*(?:to|,)\s*([+\-]?\d+\.\d{2,5})')
CITE_RE = re.compile(r'\\cite\{([^}]*)\}')
BIBITEM_RE = re.compile(r'\\bibitem\{([^}]*)\}')
DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+')
SECTION_RE = re.compile(r'\\(?:sub)*section\*?\{([^}]*)\}')
SEED_RE = re.compile(r'(?:seed|SEED)\s*[=:]\s*(\d{6,})')
B_RE = re.compile(r'\bB\s*=\s*(\d{2,6})')


def _sh(args, cwd):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception:
        return ""


def _read(path):
    try:
        return open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def normalize_latex(tex):
    """v44 R2 s2.2: deterministic LaTeX -> semantic text. Preserves scientific meaning
    (numbers, minus signs, 'development-inclusive', 'not computed', 'NLL', 'Brier') while
    removing formatting noise ($...$, \\Delta, ~, braces, \\texttt{}) that breaks matching.
    Not a full TeX parser."""
    t = tex
    # unwrap simple text-formatting commands, keep their content
    for _ in range(3):
        t = re.sub(r'\\(?:texttt|emph|textbf|textit|textsc|mathrm|text|mathbf|mathit|underline)\s*\{([^{}]*)\}', r'\1', t)
    t = t.replace(r'$-$', '-').replace(r'$+$', '+').replace(r'\,', ' ')
    t = re.sub(r'\\\((.*?)\\\)', r'\1', t)          # \( ... \) inline math
    t = re.sub(r'\$([^$]*)\$', r'\1', t)            # $ ... $ inline math -> keep content
    t = t.replace(r'\Delta', ' Delta ').replace('~', ' ').replace(r'\%', '%')
    t = re.sub(r'\\[a-zA-Z]+', ' ', t)              # remaining TeX commands -> space
    t = t.replace('{', ' ').replace('}', ' ')
    t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)           # join wrapped lines
    t = re.sub(r'\s+', ' ', t)
    return t


def new_graph():
    return {"nodes": {}, "edges": [], "meta": {}}


def add_node(g, nid, ntype, **attrs):
    if ntype not in schema.ENTITY_TYPES:
        attrs["_unknown_type"] = ntype
    g["nodes"].setdefault(nid, {"id": nid, "type": ntype, **attrs})
    return nid


def add_edge(g, src, rel, dst, why="", **meta):
    g["edges"].append({"src": src, "rel": rel, "dst": dst, "why": why, **meta})


def ingest_git(g, repo):
    add_node(g, "Project:srilanka-dengue-ews-calibration", "Project",
             branch=_sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo),
             head=_sh(["git", "rev-parse", "--short", "HEAD"], repo),
             dirty=bool(_sh(["git", "status", "--porcelain"], repo)))
    for tag in [t for t in _sh(["git", "tag"], repo).splitlines() if t]:
        commit = _sh(["git", "rev-list", "-n1", "--abbrev-commit", tag], repo)
        date = _sh(["git", "log", "-1", "--format=%ci", tag], repo)
        add_node(g, f"GitTag:{tag}", "GitTag", commit=commit, date=date)
        add_edge(g, f"GitTag:{tag}", "FROZEN_AT", f"GitCommit:{commit}", why="tag points at commit")
    for line in _sh(["git", "log", "--format=%h|%an|%ci|%s", "-40"], repo).splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            h, an, ci, subj = parts
            add_node(g, f"GitCommit:{h}", "GitCommit", author=an, date=ci, subject=subj)


def ingest_manuscript(g, repo, manuscript_path=None):
    """R2 s3: explicit manuscript targeting. If manuscript_path is given it is authoritative;
    otherwise fall back to the known candidates. The exact path + SHA-256 are recorded so v43
    and v44 are separately auditable and SUBMISSION READY refers to a named file."""
    tex = None
    if manuscript_path:
        p = manuscript_path if os.path.isabs(manuscript_path) else os.path.join(repo, manuscript_path)
        tex = p if os.path.exists(p) else None
    if not tex:
        for cand in ["manuscript_v44/revised_manuscript.tex",
                     "manuscript_v43/revised_manuscript.tex",
                     "manuscript/revised_manuscript.tex",
                     "manuscript/dengue_ews_manuscript.tex"]:
            p = os.path.join(repo, cand)
            if os.path.exists(p):
                tex = p; break
    if not tex:
        add_node(g, "Manuscript:none", "Manuscript", found=False, requested=manuscript_path)
        return None
    src = _read(tex)
    rel = os.path.relpath(tex, repo)
    sha = hashlib.sha256(src.encode("utf-8", "ignore")).hexdigest()[:16]
    g["meta"]["manuscript_path"] = rel
    g["meta"]["manuscript_sha256_16"] = sha
    mid = add_node(g, f"Manuscript:{rel}", "Manuscript", path=rel, found=True,
                   sha256_16=sha, n_chars=len(src), abstract_words=_abstract_words(src))
    # sections
    for m in SECTION_RE.finditer(src):
        add_node(g, f"Section:{m.group(1)[:60]}", "ManuscriptSection", title=m.group(1)[:120])
    # citations used vs defined
    cited = set(k.strip() for grp in CITE_RE.findall(src) for k in grp.split(","))
    defined = set(BIBITEM_RE.findall(src))
    mid_attrs = g["nodes"][mid]
    mid_attrs["cited_keys"] = sorted(cited)
    mid_attrs["bibitem_keys"] = sorted(defined)
    mid_attrs["undefined_citations"] = sorted(cited - defined - {""})
    mid_attrs["uncited_bibitems"] = sorted(defined - cited)
    for k in defined:
        add_node(g, f"Reference:{k}", "Reference")
        add_edge(g, mid, "CITES", f"Reference:{k}", why="bibitem in reference list")
    for d in set(DOI_RE.findall(src)):
        add_node(g, f"DOI:{d}", "DOI", value=d)
    # numeric claims (each signed decimal with context) -> NumericClaim nodes
    for i, line in enumerate(src.splitlines(), 1):
        for m in NUM_RE.finditer(line):
            val = m.group(0)
            nid = f"NumericClaim:{rel}:{i}:{m.start()}:{val}"
            add_node(g, nid, "NumericClaim", value=val, line=i, context=line.strip()[:160])
            add_edge(g, nid, "APPEARS_IN", mid, why="numeric token in manuscript")
    # placeholders
    ph = []
    for marker in schema.PLACEHOLDER_MARKERS:
        c = src.count(marker)
        if c:
            ph.append({"marker": marker, "count": c})
    mid_attrs["placeholders"] = ph
    # public-repo / DOI assertion flags (verify later, don't trust prose)
    mid_attrs["claims_public_github"] = bool(re.search(r'github\.com/\S+', src))
    mid_attrs["em_dashes"] = src.count("---")
    return mid


def _abstract_words(src):
    m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', src, re.S)
    if not m:
        return None
    return len(re.sub(r'\\[a-zA-Z]+|\{|\}|\$', ' ', m.group(1)).split())


def ingest_results(g, repo):
    # frozen artifacts + checksums
    for sha in glob.glob(os.path.join(repo, "**", "*.sha256"), recursive=True):
        rel = os.path.relpath(sha, repo)
        add_node(g, f"Checksum:{rel}", "Checksum", path=rel)
    # result JSONs (analysis outputs) — these are the ground truth for numeric claims
    result_values = {}
    for jf in glob.glob(os.path.join(repo, "**", "*results*.json"), recursive=True) + \
              glob.glob(os.path.join(repo, "**", "_provenance.json"), recursive=True):
        rel = os.path.relpath(jf, repo)
        add_node(g, f"Result:{rel}", "Result", path=rel)
        try:
            data = json.load(open(jf))
            for v in _flatten_numbers(data):
                result_values.setdefault(_fmt(v), []).append(rel)
        except Exception:
            pass
    # audit / results markdown + csv also carry ground-truth numbers
    for mf in glob.glob(os.path.join(repo, "audit_v42", "*.md")) + \
              glob.glob(os.path.join(repo, "audit_v42", "*.csv")) + \
              glob.glob(os.path.join(repo, "**", "*route_a*.csv"), recursive=True):
        rel = os.path.relpath(mf, repo)
        add_node(g, f"ResultDoc:{rel}", "Result", path=rel)
        for m in NUM_RE.finditer(_read(mf)):
            result_values.setdefault(m.group(0), []).append(rel)
    g["meta"]["result_values"] = result_values      # value -> [source files]
    return result_values


def _flatten_numbers(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _flatten_numbers(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _flatten_numbers(v)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield float(obj)


def _fmt(v):
    s = f"{v:+.4f}"
    return s


def ingest_scripts(g, repo):
    for py in glob.glob(os.path.join(repo, "analysis", "**", "*.py"), recursive=True) + \
              glob.glob(os.path.join(repo, "ALT_STATS", "**", "*.py"), recursive=True) + \
              glob.glob(os.path.join(repo, "scripts", "**", "*.py"), recursive=True):
        rel = os.path.relpath(py, repo)
        src = _read(py)
        seeds = sorted(set(SEED_RE.findall(src)))
        bvals = sorted(set(B_RE.findall(src)))
        leak_flags = []
        if ".interpolate(" in src:
            leak_flags.append("uses .interpolate() (future-value leakage risk)")
        if re.search(r'fillna\([^)]*method\s*=\s*["\']bfill', src):
            leak_flags.append("bfill (backward fill = future leakage)")
        add_node(g, f"Script:{rel}", "Script", path=rel, seeds=seeds, B=bvals, leak_flags=leak_flags)


def ingest_audit_docs(g, repo):
    for md in glob.glob(os.path.join(repo, "audit_v42", "*.md")) + \
              glob.glob(os.path.join(repo, "docs", "*.md")):
        rel = os.path.relpath(md, repo)
        add_node(g, f"AuditDoc:{rel}", "AuditFinding", path=rel,
                 mtime=os.path.getmtime(md))


def ingest_analyses(g, repo):
    """Seed the analysis-status ontology from known chronology (audit_v42/03) + tags."""
    analyses = {
        "M4_M1_primary": ("internally_design_locked", "design-locked primary SL contrast; non-nested, does not isolate climate"),
        "matched_climate_ablation": ("post_hoc_exploratory", "M5 vs independently-refit M5_no-climate"),
        "proper_score_reanalysis": ("post_result_design_locked", "locked (alt-stats-plan-v1) before scoring, after primary known"),
        "calibration_intercept_sensitivity": ("sensitivity", "-0.5 logit shift"),
        "dlnm_functional_form": ("sensitivity", "Colombia DLNM cross-basis vs linear"),
        "devinclusive_bootstrap": ("diagnostic", "refit-both-models uncertainty; primary robustness basis"),
        "matched_ablation_90pct": ("post_hoc_exploratory", "reviewer-responsive; 90th-pct outbreak label"),
        "devincl_proper_scores": ("post_hoc_exploratory", "reviewer-responsive; removes conditional-only asymmetry"),
    }
    for name, (status, why) in analyses.items():
        nid = add_node(g, f"Analysis:{name}", "Analysis", status=status, rationale=why)
        add_edge(g, nid, "CLASSIFIED_AS", f"Status:{status}", why=why)
    # matched comparison structure (prompt s6)
    add_node(g, "Model:M5", "Model", features="cases+season+geo+climate")
    add_node(g, "Model:M5_no_climate", "Model", features="cases+season+geo")
    add_node(g, "Model:M1", "Comparator", features="recent cases (SL: +season+RDHS)")
    add_edge(g, "Analysis:matched_climate_ablation", "COMPARES", "Model:M5", why="ablation full model")
    add_edge(g, "Analysis:matched_climate_ablation", "ABLATES", "Model:M5_no_climate", why="climate block removed, independently refit")


def build_graph(repo, manuscript_path=None):
    g = new_graph()
    ingest_git(g, repo)
    ingest_manuscript(g, repo, manuscript_path=manuscript_path)
    ingest_results(g, repo)
    ingest_scripts(g, repo)
    ingest_audit_docs(g, repo)
    ingest_analyses(g, repo)
    g["meta"]["counts"] = {
        "nodes": len(g["nodes"]),
        "edges": len(g["edges"]),
        "by_type": _count_by_type(g),
    }
    return g


def _count_by_type(g):
    out = {}
    for n in g["nodes"].values():
        out[n["type"]] = out.get(n["type"], 0) + 1
    return out


def save_graph(g, repo):
    outdir = os.path.join(repo, "knowledge_graph", "graph")
    os.makedirs(outdir, exist_ok=True)
    json.dump(g, open(os.path.join(outdir, "project_graph.json"), "w"), indent=1, default=str)
    summary = {"meta": g["meta"], "manuscript": next((n for n in g["nodes"].values()
               if n["type"] == "Manuscript"), {})}
    json.dump(summary, open(os.path.join(outdir, "project_graph_summary.json"), "w"), indent=1, default=str)
