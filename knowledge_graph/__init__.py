"""Lightweight, deterministic project knowledge graph for srilanka-dengue-ews-calibration.

Stdlib-only. No LLM calls in any check (per prompt s17). A JSON graph + pure-Python
queries make it hard for an unsupported, stale, contradictory, or unreproducible claim
to survive into submission.
"""
__all__ = ["schema", "ingest", "graph"]
