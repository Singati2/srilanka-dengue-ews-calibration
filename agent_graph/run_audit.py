"""Top-level audit runner.

    python -m agent_graph.run_audit --repo .

Builds the knowledge graph, runs every deterministic agent, prints a release-gate
summary, and writes audit/CURRENT_KG_AGENT_AUDIT.{md,json}. Exit code 1 if not
submission-ready (usable as a CI gate). No LLM, no network.
"""
import os, sys, json, argparse, datetime
from knowledge_graph import ingest
from agent_graph import agents


def run(repo):
    g = ingest.build_graph(repo)
    ingest.save_graph(g, repo)
    results = [fn(g, repo) for fn in agents.ALL_AGENTS]
    # SUBMISSION READY only if no FAIL gate
    ready = not any(r["status"] == "FAIL" for r in results)
    report = {
        "repo": os.path.abspath(repo),
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "graph": g["meta"]["counts"],
        "gates": [{"name": r["name"], "status": r["status"],
                   "n_findings": len(r["findings"]), "findings": r["findings"]} for r in results],
        "submission_ready": ready,
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
    print()
    print(f"SUBMISSION READY: {'YES' if report['submission_ready'] else 'NO'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic KG+Agent audit")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json", action="store_true", help="print full JSON report")
    a = ap.parse_args(argv)
    g, results, report = run(a.repo)
    write_outputs(a.repo, g, results, report)
    if a.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print_summary(results, report)
    return 0 if report["submission_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
