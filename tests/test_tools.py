"""
Acceptance tests for Blast Radius Brain (Aurora Labs).
Hits the live FalkorDB instance and validates the graph tools and router.
"""

import os
import pytest
from seed import seed_graph, get_graph_counts
from graph_tools import blast_radius, expert_finder, decision_provenance
from router import route


@pytest.fixture(scope="session", autouse=True)
def ensure_seeded_graph():
    """Ensure graph is seeded before tests run."""
    seed_graph()


def test_seed_idempotency():
    """Test 1: seed.py run twice -> node and relationship counts identical."""
    counts_run1 = seed_graph()
    counts_run2 = seed_graph()

    assert counts_run1["total_nodes"] == counts_run2["total_nodes"]
    assert counts_run1["total_relationships"] == counts_run2["total_relationships"]
    assert counts_run1["nodes"] == counts_run2["nodes"]
    assert counts_run1["relationships"] == counts_run2["relationships"]

    # Verify expected counts
    assert counts_run1["nodes"]["System"] == 10
    assert counts_run1["nodes"]["Project"] == 8
    assert counts_run1["nodes"]["Person"] == 14
    assert counts_run1["nodes"]["Decision"] == 5
    assert counts_run1["nodes"]["Doc"] == 5
    assert counts_run1["total_nodes"] == 42


def test_blast_radius_ledger_service():
    """
    Test 2: blast_radius("ledger-service") includes:
    - payments-api (1 hop)
    - checkout-ui (2)
    - refund-worker
    - reporting-batch (1)
    - billing-cron
    - mobile-gateway (2 or 3)
    Every returned path starts with ledger-service.
    """
    result = blast_radius("ledger-service")
    rows = result["evidence"]["rows"]
    affected_map = {r["affected_system"]: r["hops"] for r in rows}

    assert "payments-api" in affected_map
    assert affected_map["payments-api"] == 1

    assert "checkout-ui" in affected_map
    assert affected_map["checkout-ui"] == 2

    assert "refund-worker" in affected_map
    assert "reporting-batch" in affected_map
    assert affected_map["reporting-batch"] == 1

    assert "billing-cron" in affected_map
    assert "mobile-gateway" in affected_map
    assert affected_map["mobile-gateway"] in [2, 3]

    # Every returned path starts with ledger-service
    for path in result["evidence"]["paths"]:
        assert len(path) >= 2
        assert path[0] == "ledger-service"


def test_expert_finder_ledger_service():
    """
    Test 3: expert_finder("ledger-service") returns Maya Chen in the top 3,
    and her projects include Helios.
    """
    result = expert_finder("ledger-service")
    rows = result["evidence"]["rows"]
    assert len(rows) > 0

    top_3_names = [r["person"] for r in rows[:3]]
    assert "Maya Chen" in top_3_names

    # Check Maya Chen projects include Helios
    maya_row = next(r for r in rows if r["person"] == "Maya Chen")
    assert "Helios" in maya_row["projects"]


def test_decision_provenance_helios():
    """
    Test 4: decision_provenance("Helios") returns "Pause Helios rollout"
    with decided_by == "Nora Haddad" and systems containing ledger-service.
    """
    result = decision_provenance("Helios")
    rows = result["evidence"]["rows"]
    assert len(rows) > 0

    pause_decision = next((r for r in rows if r["decision"] == "Pause Helios rollout"), None)
    assert pause_decision is not None
    assert pause_decision["decided_by"] == "Nora Haddad"
    assert "ledger-service" in pause_decision["systems"]


def test_router_deterministic_fallback():
    """
    Test 5: router.route("What breaks if ledger-service goes down?")
    returns tool == "blast_radius" and entity == "ledger-service" with no API key set.
    """
    # Temporarily unset any keys to test pure deterministic fallback
    orig_openai = os.environ.pop("OPENAI_API_KEY", None)
    orig_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        routed = route("What breaks if ledger-service goes down?")
        assert routed["tool"] == "blast_radius"
        assert routed["entity"] == "ledger-service"
    finally:
        if orig_openai is not None:
            os.environ["OPENAI_API_KEY"] = orig_openai
        if orig_anthropic is not None:
            os.environ["ANTHROPIC_API_KEY"] = orig_anthropic


def test_evidence_contract():
    """
    Test 6: Every tool result contains non-empty answer, cypher, params,
    and evidence.paths (or evidence.rows for decision tool).
    """
    b_res = blast_radius("ledger-service")
    e_res = expert_finder("ledger-service")
    d_res = decision_provenance("Helios")

    for res, tool_name in [(b_res, "blast_radius"), (e_res, "expert_finder"), (d_res, "decision_provenance")]:
        assert res["tool"] == tool_name
        assert isinstance(res["question"], str) and len(res["question"]) > 0
        assert isinstance(res["answer"], str) and len(res["answer"]) > 0
        assert isinstance(res["cypher"], str) and len(res["cypher"]) > 0
        assert isinstance(res["params"], dict) and len(res["params"]) > 0
        assert "evidence" in res
        assert "rows" in res["evidence"] and len(res["evidence"]["rows"]) > 0
        assert "paths" in res["evidence"]
        assert "nodes" in res["evidence"]
