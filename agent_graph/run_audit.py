"""Top-level audit runner.

    python -m agent_graph.run_audit --repo .

Builds the knowledge graph, runs every deterministic agent, prints a release-gate
summary, and writes audit/CURRENT_KG_AGENT_AUDIT.{md,json}. Exit code 1 if not
submission-ready (usable as a CI gate). No LLM, no network.
"""
import os, sys, json, argparse, datetime
from knowledge_graph import ingest, schema
from agent_graph import agents


def manuscript_readiness(by_name):
    """v44 R4 s5: READY iff every mandatory scientific gate == PASS. Returns (readiness, blocking).
    by_name: {gate_name: status}."""
    blocking = {name: by_name.get(name, "MISSING") for name in schema.MANDATORY_SCIENTIFIC_GATES
                if by_name.get(name, "MISSING") != "PASS"}
    return ("READY" if not blocking else "NOT_READY"), blocking


def run(repo, manuscript_path=None):
    g = ingest.build_graph(repo, manuscript_path=manuscript_path)
    ingest.save_graph(g, repo)
    results = [fn(g, repo) for fn in agents.ALL_AGENTS]
    # v44 R4 s5: TWO separate concepts.
    # (1) audit software health: did the tool run without an internal error? (agents catch their
    #     own exceptions and always return a legal status, so a completed run is PASS.)
    audit_software_health = "PASS"
    # (2) manuscript submission readiness: READY iff EVERY mandatory scientific gate == PASS.
    #     "No literal FAIL" is NOT sufficient — REVIEW/PARTIAL/NOT_VERIFIED also block.
    by_name = {r["name"]: r["status"] for r in results}
    manuscript_submission_readiness, blocking = manuscript_readiness(by_name)
    ready = (manuscript_submission_readiness == "READY")
    not_verified = [r["name"] for r in results if r["status"] in ("NOT_VERIFIED", "PARTIAL")]
    report = {
        "repo": os.path.abspath(repo),
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "manuscript_audited": g["meta"].get("manuscript_path"),
        "manuscript_sha256_16": g["meta"].get("manuscript_sha256_16"),
        "graph": g["meta"]["counts"],
        "gates": [{"name": r["name"], "status": r["status"],
                   "n_findings": len(r["findings"]), "findings": r["findings"]} for r in results],
        "audit_software_health": audit_software_health,
        "manuscript_submission_readiness": manuscript_submission_readiness,
        "blocking_mandatory_gates": blocking,
        "submission_ready": ready,          # bool alias (drives exit code / back-compat)
        "not_verified_gates": not_verified,
    }
    return g, results, report


def _sev_counts(results):
    c = {"critical": 0, "major": 0, "minor": 0}
    for r in results:
        for f in r["findings"]:
            if f.get("ok"):
                continue
            c[f["severity"]] = c.get(f["severity"], 0) + 1
    return c


def write_outputs(repo, g, results, report):
    outdir = os.path.join(repo, "audit")
    os.makedirs(outdir, exist_ok=True)
    json.dump(report, open(os.path.join(outdir, "CURRENT_KG_AGENT_AUDIT.json"), "w"), indent=2, default=str)
    sev = _sev_counts(results)
    lines = ["# Knowledge-Graph + Agent-Graph Audit", "",
             f"- Generated: {report['generated']}",
             f"- Repo: `{report['repo']}`",
             f"- Graph: {report['graph']['nodes']} nodes / {report['graph']['edges']} edges",
             f"- Findings: {sev['critical']} critical · {sev['major']} major · {sev['minor']} minor",
             f"- **SUBMISSION READY: {'YES' if report['submission_ready'] else 'NO'}**", "",
             "## Release gates", "", "| Gate | Status | Findings |", "|---|---|---|"]
    for r in results:
        lines.append(f"| {r['name']} | {r['status']} | {len([f for f in r['findings'] if not f.get('ok')])} |")
    lines += ["", "## Findings by gate", ""]
    for r in results:
        real = [f for f in r["findings"] if not f.get("ok")]
        lines.append(f"### {r['name']} — {r['status']}")
        if not real:
            lines.append("- (no issues)")
        for f in real:
            ev = f.get("evidence") or []
            ev_s = ("  \n    - " + "\n    - ".join(str(e) for e in ev)) if ev else ""
            lines.append(f"- **[{f['severity']}]** {f['msg']}{ev_s}")
        lines.append("")
    open(os.path.join(outdir, "CURRENT_KG_AGENT_AUDIT.md"), "w").write("\n".join(lines))


def print_summary(results, report):
    width = max(len(r["name"]) for r in results) + 2
    print()
    for r in results:
        print(f"{r['name']:<{width}} {r['status']}")
    if report.get("not_verified_gates"):
        print()
        print("NOT_VERIFIED (not demonstrated; needs out-of-audit check): " + ", ".join(report["not_verified_gates"]))
    print()
    print(f"AUDIT SOFTWARE HEALTH:          {report.get('audit_software_health', 'PASS')}")
    print(f"MANUSCRIPT SUBMISSION READINESS: {report.get('manuscript_submission_readiness', '?')}")
    if report.get("blocking_mandatory_gates"):
        for name, st in report["blocking_mandatory_gates"].items():
            print(f"    - blocked by mandatory gate {name}: {st}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic KG+Agent audit")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--manuscript", default=None,
                    help="explicit manuscript .tex to audit (R2 s3); e.g. manuscript_v43/revised_manuscript.tex")
    ap.add_argument("--json", action="store_true", help="print full JSON report")
    a = ap.parse_args(argv)
    g, results, report = run(a.repo, manuscript_path=a.manuscript)
    if report.get("manuscript_audited"):
        print(f"manuscript audited: {report['manuscript_audited']} (sha {report['manuscript_sha256_16']})")
    write_outputs(a.repo, g, results, report)
    if a.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print_summary(results, report)
    return 0 if report["submission_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
