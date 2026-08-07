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
        assert r["status"] in schema.GATE_STATUSES
        assert isinstance(r["findings"], list)


def test_run_audit_is_deterministic():
    _, _, r1 = run_audit.run(REPO)
    _, _, r2 = run_audit.run(REPO)
    assert [x["status"] for x in r1["gates"]] == [x["status"] for x in r2["gates"]]


# ---------------- v44 s3.3 regression tests (gate MEANING, not just legal strings) ----------------

_V43_CONTRADICTION = (
    "Methods. The refit-both-models bootstrap was not re-executed, so development-inclusive "
    "proper-score intervals were gated and not computed; conditional intervals only. "
    "Results. Development-inclusive proper scores: Sri Lanka NLL -0.0403 to +0.0040; "
    "Brier -0.0153 to +0.0013; Colombia NLL -0.0224 to -0.0002.")
_V44_CONSISTENT = (
    "The refit-both-models bootstrap was subsequently executed for the proper scores, giving "
    "development-inclusive Sri Lanka NLL -0.0403 to +0.0040 and Colombia NLL -0.0224 to -0.0002.")


def test_1_v43_proper_score_contradiction_is_caught():
    contra, reports, claims_not = agents.detect_proper_score_contradiction(_V43_CONTRADICTION)
    assert contra is True and reports and claims_not          # synthetic v43 must be detected
    contra2, _, _ = agents.detect_proper_score_contradiction(_V44_CONSISTENT)
    assert contra2 is False                                    # consistent text must NOT be detected


def test_1b_real_v43_file_is_detected():
    # R2 s2.1/2.4: the ACTUAL tracked manuscript_v43 CONTAINS the contradiction and MUST be
    # detected. (A test expecting the real v43 to be 'consistent' is historically wrong.)
    p = os.path.join(REPO, "manuscript_v43", "revised_manuscript.tex")
    if not os.path.exists(p):
        return  # branch without the manuscript; skip
    src = agents._read(p)
    assert agents.detect_proper_score_contradiction(src)[0] is True


def test_1c_latex_interval_variants_are_equivalent():
    # R2 s2.3: all these interval forms must be recognized (do not overfit the 4 values)
    claim = " The development-inclusive proper scores were gated and not computed."
    for iv in ["-0.0403 to +0.0040", "$-0.0403$ to $+0.0040$", "(-0.0403, +0.0040)",
               "[-0.0403, +0.0040]", r"\(-0.0403\) to \(+0.0040\)"]:
        txt = "development-inclusive proper-score NLL " + iv + "." + claim
        assert agents.detect_proper_score_contradiction(txt)[0] is True, iv


def test_1d_corrected_v44_text_is_not_detected():
    # after repair (no 'not computed/gated' claim), the same reported intervals are consistent
    ok = ("development-inclusive proper-score NLL $-0.0403$ to $+0.0040$ were subsequently "
          "computed under the refit-both-models bootstrap.")
    assert agents.detect_proper_score_contradiction(ok)[0] is False


def test_2_reference_scientific_support_not_verified():
    # a valid \cite key does not prove the source supports the claim -> never a strong PASS offline
    g = ingest.build_graph(REPO)
    r = agents.reference_agent(g, REPO)
    assert r["status"] in ("NOT_VERIFIED", "FAIL")
    assert any("NOT_VERIFIED" in f["msg"] or "support" in f["msg"] for f in r["findings"])


def test_3_reproducibility_presence_only_is_not_strong_pass():
    g = ingest.build_graph(REPO)
    r = agents.reproducibility_agent(g, REPO)
    assert r["status"] != "PASS"                               # lockfile+checksum alone must not PASS
    assert r["status"] in ("NOT_VERIFIED", "PARTIAL", "REVIEW", "FAIL")


def test_4_modis_composite_end_past_origin_is_leakage():
    assert agents.composite_leaks_if_joined_by_start("2023-01-01", "2023-01-16", "2023-01-08") is True
    assert agents.composite_leaks_if_joined_by_start("2022-12-20", "2023-01-04", "2023-01-08") is False
    assert agents.composite_leaks_if_joined_by_start("2023-01-01", "2023-01-07", "2023-01-08") is False


def test_5_traceability_is_token_based_not_strong_pass():
    # RESULT TRACEABILITY relies on decimal-token matching; it must never claim a strong PASS,
    # because the same 4-dp number can appear in unrelated results (collision risk).
    g = ingest.build_graph(REPO)
    r = agents.claim_agent(g, REPO)
    assert r["status"] != "PASS"


def test_6_a_clean_property_can_still_pass():
    # not everything is downgraded: a genuinely demonstrated property still earns PASS.
    g = ingest.build_graph(REPO)
    statuses = [fn(g, REPO)["status"] for fn in agents.ALL_AGENTS]
    assert "PASS" in statuses, "at least one gate should PASS on a demonstrated property"


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
