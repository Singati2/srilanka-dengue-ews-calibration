"""Controlled agent graph: deterministic audit checkers over the knowledge graph.

Each agent is a pure function of (graph, repo_root) -> AgentResult. NO LLM calls
(prompt s17). Explicit PASS / REVIEW / FAIL with evidence for every check.
"""
__all__ = ["agents", "run_audit"]
