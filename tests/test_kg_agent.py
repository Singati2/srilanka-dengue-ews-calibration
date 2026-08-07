"""Deterministic tests for the KG + agent graph (prompt s7,s18). Run: python -m pytest tests/ -q
Falls back to a plain runner if pytest is absent."""
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from knowledge_graph import schema, ingest
from agent_graph import agents, run_audit


def test_schema_vocab_nonempty():
    assert len(schema.ENTITY_TYPES) >= 40
    assert len(schema.RELATION_TYPES) >= 20
    assert len(schema.ANALYSIS_STATUSES) == 7


def test_graph_builds_and_has_manuscript():
    g = ingest.build_graph(REPO)
    assert g["meta"]["counts"]["nodes"] > 100
    m = agents._manuscript(g)
    assert m is not None and m.get("found")
    assert m.get("abstract_words")  # abstract parsed


def test_placeholders_are_detected():
    # regression for the '[AUTHOR INPUT REQUIRED: field]' marker bug
    g = ingest.build_graph(REPO)
    m = agents._manuscript(g)
    total = sum(p["count"] for p in m.get("placeholders", []))
    assert total >= 8, f"expected >=8 author-input placeholders, found {total}"


def test_submission_blocks_when_placeholders_present():
    g = ingest.build_graph(REPO)
    r = agents.submission_declarations_agent(g, REPO)
    assert r["status"] == "FAIL"


def test_every_analysis_has_a_valid_status():
    g = ingest.build_graph(REPO)
    for n in g["nodes"].values():
        if n["type"] == "Analysis":
            assert n.get("status") in schema.ANALYSIS_STATUSES, n


def test_all_agents_return_valid_status():
    g = ingest.build_graph(REPO)
    for fn in agents.ALL_AGENTS:
        r = fn(g, REPO)
        assert r["status"] in ("PASS", "REVIEW", "FAIL")
        assert isinstance(r["findings"], list)


def test_run_audit_is_deterministic():
    _, _, r1 = run_audit.run(REPO)
    _, _, r2 = run_audit.run(REPO)
    assert [x["status"] for x in r1["gates"]] == [x["status"] for x in r2["gates"]]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    ok = 0
    for fn in fns:
        try:
            fn(); print("PASS", fn.__name__); ok += 1
        except AssertionError as e:
            print("FAIL", fn.__name__, "->", e)
    print(f"\n{ok}/{len(fns)} tests passed")
    sys.exit(0 if ok == len(fns) else 1)
