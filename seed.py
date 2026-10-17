"""
Idempotent graph seeder for Blast Radius Brain (Aurora Labs).
Uses FalkorDB with MERGE and UNWIND so running it multiple times does not duplicate data.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv
from falkordb import FalkorDB

load_dotenv()

HOST = os.getenv("FALKORDB_HOST", "localhost")
PORT = int(os.getenv("FALKORDB_PORT", "6379"))
GRAPH_NAME = os.getenv("FALKORDB_GRAPH", "company")

# 1. Systems: name, kind, criticality
SYSTEMS = [
    {"name": "auth-service", "kind": "service", "criticality": "high"},
    {"name": "notification-service", "kind": "service", "criticality": "medium"},
    {"name": "ledger-service", "kind": "service", "criticality": "high"},
    {"name": "payments-api", "kind": "service", "criticality": "high"},
    {"name": "checkout-ui", "kind": "frontend", "criticality": "high"},
    {"name": "refund-worker", "kind": "worker", "criticality": "medium"},
    {"name": "reporting-batch", "kind": "batch", "criticality": "medium"},
    {"name": "billing-cron", "kind": "batch", "criticality": "high"},
    {"name": "search-service", "kind": "service", "criticality": "medium"},
    {"name": "mobile-gateway", "kind": "gateway", "criticality": "high"},
]

# 2. Dependencies: A depends on B (A)-[:DEPENDS_ON]->(B)
DEPENDENCIES = [
    {"source": "payments-api", "target": "ledger-service"},
    {"source": "payments-api", "target": "auth-service"},
    {"source": "checkout-ui", "target": "payments-api"},
    {"source": "refund-worker", "target": "payments-api"},
    {"source": "reporting-batch", "target": "ledger-service"},
    {"source": "billing-cron", "target": "ledger-service"},
    {"source": "billing-cron", "target": "notification-service"},
    {"source": "notification-service", "target": "auth-service"},
    {"source": "search-service", "target": "auth-service"},
    {"source": "mobile-gateway", "target": "payments-api"},
    {"source": "mobile-gateway", "target": "search-service"},
]

# 3. Projects: name, status, owner
PROJECTS = [
    {"name": "Helios", "status": "active", "owner": "Maya Chen"},
    {"name": "Atlas", "status": "active", "owner": "Diego Ramos"},
    {"name": "Orion", "status": "active", "owner": "Priya Nair"},
    {"name": "Vega", "status": "active", "owner": "Sam Okafor"},
    {"name": "Nova", "status": "active", "owner": "Lena Fischer"},
    {"name": "Pulse", "status": "active", "owner": "Tom Becker"},
    {"name": "Quasar", "status": "active", "owner": "Aisha Khan"},
    {"name": "Zephyr", "status": "active", "owner": "Marco Silva"},
]

# 4. People: name, role, team (14 people)
PEOPLE = [
    {"name": "Maya Chen", "role": "Staff Engineer", "team": "Payments"},
    {"name": "Diego Ramos", "role": "Senior Engineer", "team": "Data"},
    {"name": "Priya Nair", "role": "Engineer", "team": "Checkout"},
    {"name": "Sam Okafor", "role": "Security Lead", "team": "Platform"},
    {"name": "Lena Fischer", "role": "Engineer", "team": "Mobile"},
    {"name": "Tom Becker", "role": "Engineer", "team": "Platform"},
    {"name": "Aisha Khan", "role": "Engineer", "team": "Search"},
    {"name": "Marco Silva", "role": "Engineer", "team": "Billing"},
    {"name": "Nora Haddad", "role": "Engineering Manager", "team": "Payments"},
    {"name": "Eli Park", "role": "SRE", "team": "Platform"},
    {"name": "Ruth Adeyemi", "role": "Product Manager", "team": "Payments"},
    {"name": "Jonas Weber", "role": "Engineer", "team": "Data"},
    {"name": "Keiko Tanaka", "role": "SRE", "team": "Platform"},
    {"name": "Omar Farouk", "role": "Engineer", "team": "Checkout"},
]

# 5. WORKS_ON: (person, project)
WORKS_ON = [
    {"person": "Maya Chen", "project": "Helios"},
    {"person": "Maya Chen", "project": "Atlas"},
    {"person": "Maya Chen", "project": "Zephyr"},
    {"person": "Diego Ramos", "project": "Atlas"},
    {"person": "Diego Ramos", "project": "Helios"},
    {"person": "Priya Nair", "project": "Orion"},
    {"person": "Priya Nair", "project": "Helios"},
    {"person": "Sam Okafor", "project": "Vega"},
    {"person": "Sam Okafor", "project": "Pulse"},
    {"person": "Lena Fischer", "project": "Nova"},
    {"person": "Lena Fischer", "project": "Orion"},
    {"person": "Tom Becker", "project": "Pulse"},
    {"person": "Tom Becker", "project": "Vega"},
    {"person": "Aisha Khan", "project": "Quasar"},
    {"person": "Marco Silva", "project": "Zephyr"},
    {"person": "Marco Silva", "project": "Atlas"},
    {"person": "Nora Haddad", "project": "Helios"},
    {"person": "Nora Haddad", "project": "Orion"},
    {"person": "Eli Park", "project": "Vega"},
    {"person": "Eli Park", "project": "Zephyr"},
    {"person": "Ruth Adeyemi", "project": "Helios"},
    {"person": "Ruth Adeyemi", "project": "Nova"},
    {"person": "Jonas Weber", "project": "Atlas"},
    {"person": "Jonas Weber", "project": "Quasar"},
    {"person": "Keiko Tanaka", "project": "Pulse"},
    {"person": "Keiko Tanaka", "project": "Vega"},
    {"person": "Omar Farouk", "project": "Orion"},
    {"person": "Omar Farouk", "project": "Nova"},
]

# 6. LEADS: (person, project)
LEADS = [
    {"person": "Maya Chen", "project": "Helios"},
    {"person": "Diego Ramos", "project": "Atlas"},
    {"person": "Priya Nair", "project": "Orion"},
    {"person": "Sam Okafor", "project": "Vega"},
    {"person": "Lena Fischer", "project": "Nova"},
    {"person": "Tom Becker", "project": "Pulse"},
    {"person": "Aisha Khan", "project": "Quasar"},
    {"person": "Marco Silva", "project": "Zephyr"},
]

# 7. USES: (project, system)
USES = [
    {"project": "Helios", "system": "payments-api"},
    {"project": "Helios", "system": "ledger-service"},
    {"project": "Atlas", "system": "reporting-batch"},
    {"project": "Atlas", "system": "ledger-service"},
    {"project": "Orion", "system": "checkout-ui"},
    {"project": "Orion", "system": "payments-api"},
    {"project": "Vega", "system": "auth-service"},
    {"project": "Nova", "system": "mobile-gateway"},
    {"project": "Nova", "system": "payments-api"},
    {"project": "Pulse", "system": "notification-service"},
    {"project": "Quasar", "system": "search-service"},
    {"project": "Zephyr", "system": "billing-cron"},
    {"project": "Zephyr", "system": "ledger-service"},
]

# 8. Decisions: title, date, status, summary, project, decided_by, system
DECISIONS = [
    {
        "title": "Pause Helios rollout",
        "date": "2026-09-12",
        "status": "paused",
        "summary": "Rollout paused after ledger-service latency regression in staging.",
        "project": "Helios",
        "decided_by": "Nora Haddad",
        "system": "ledger-service",
    },
    {
        "title": "Adopt ledger-service v2",
        "date": "2026-08-03",
        "status": "approved",
        "summary": "Helios will migrate to ledger-service v2 with dual-write cutover.",
        "project": "Helios",
        "decided_by": "Maya Chen",
        "system": "ledger-service",
    },
    {
        "title": "Freeze auth-service changes",
        "date": "2026-09-01",
        "status": "active",
        "summary": "Change freeze on auth-service until the Vega hardening audit closes.",
        "project": "Vega",
        "decided_by": "Sam Okafor",
        "system": "auth-service",
    },
    {
        "title": "Move billing to billing-cron",
        "date": "2026-07-21",
        "status": "approved",
        "summary": "Retire the legacy billing job and standardize on billing-cron.",
        "project": "Zephyr",
        "decided_by": "Marco Silva",
        "system": "billing-cron",
    },
    {
        "title": "Deprecate search-service v1",
        "date": "2026-06-15",
        "status": "approved",
        "summary": "Quasar will move to search-service v2; v1 read-only from Q4.",
        "project": "Quasar",
        "decided_by": "Aisha Khan",
        "system": "search-service",
    },
]

# 9. Docs: title, kind, author, summary, about
DOCS = [
    {
        "title": "Ledger Service Runbook",
        "kind": "runbook",
        "author": "Maya Chen",
        "summary": "On-call procedures and failure modes for ledger-service.",
        "system": "ledger-service",
    },
    {
        "title": "Helios Dual-Write Design",
        "kind": "design",
        "author": "Diego Ramos",
        "summary": "Dual-write plan for ledger-service v2 migration.",
        "system": "ledger-service",
    },
    {
        "title": "Auth Freeze Postmortem",
        "kind": "postmortem",
        "author": "Sam Okafor",
        "summary": "Root cause and freeze decision for auth-service incident.",
        "system": "auth-service",
    },
    {
        "title": "Billing Cron Migration Guide",
        "kind": "design",
        "author": "Marco Silva",
        "summary": "Cutover checklist for billing-cron.",
        "system": "billing-cron",
    },
    {
        "title": "Checkout Latency Playbook",
        "kind": "runbook",
        "author": "Priya Nair",
        "summary": "Playbook for checkout-ui latency incidents.",
        "system": "checkout-ui",
    },
]


def get_graph():
    db = FalkorDB(host=HOST, port=PORT)
    return db.select_graph(GRAPH_NAME)


def seed_graph() -> Dict[str, Any]:
    g = get_graph()

    # 1. Systems
    g.query(
        """
        UNWIND $systems AS row
        MERGE (s:System {name: row.name})
        SET s.kind = row.kind, s.criticality = row.criticality
        """,
        {"systems": SYSTEMS},
    )

    # 2. People
    g.query(
        """
        UNWIND $people AS row
        MERGE (p:Person {name: row.name})
        SET p.role = row.role, p.team = row.team
        """,
        {"people": PEOPLE},
    )

    # 3. Projects
    g.query(
        """
        UNWIND $projects AS row
        MERGE (pr:Project {name: row.name})
        SET pr.status = row.status, pr.owner = row.owner
        """,
        {"projects": PROJECTS},
    )

    # 4. Decisions
    g.query(
        """
        UNWIND $decisions AS row
        MERGE (d:Decision {title: row.title})
        SET d.date = row.date, d.status = row.status, d.summary = row.summary
        """,
        {"decisions": DECISIONS},
    )

    # 5. Docs
    g.query(
        """
        UNWIND $docs AS row
        MERGE (dc:Doc {title: row.title})
        SET dc.kind = row.kind, dc.author = row.author, dc.summary = row.summary
        """,
        {"docs": DOCS},
    )

    # 6. DEPENDS_ON
    g.query(
        """
        UNWIND $dependencies AS row
        MATCH (a:System {name: row.source})
        MATCH (b:System {name: row.target})
        MERGE (a)-[:DEPENDS_ON]->(b)
        """,
        {"dependencies": DEPENDENCIES},
    )

    # 7. WORKS_ON
    g.query(
        """
        UNWIND $works_on AS row
        MATCH (p:Person {name: row.person})
        MATCH (pr:Project {name: row.project})
        MERGE (p)-[:WORKS_ON]->(pr)
        """,
        {"works_on": WORKS_ON},
    )

    # 8. LEADS
    g.query(
        """
        UNWIND $leads AS row
        MATCH (p:Person {name: row.person})
        MATCH (pr:Project {name: row.project})
        MERGE (p)-[:LEADS]->(pr)
        """,
        {"leads": LEADS},
    )

    # 9. USES
    g.query(
        """
        UNWIND $uses AS row
        MATCH (pr:Project {name: row.project})
        MATCH (s:System {name: row.system})
        MERGE (pr)-[:USES]->(s)
        """,
        {"uses": USES},
    )

    # 10. Decision Relationships: DECIDED, DECIDED_IN, ABOUT
    g.query(
        """
        UNWIND $decisions AS row
        MATCH (d:Decision {title: row.title})
        MATCH (p:Person {name: row.decided_by})
        MATCH (pr:Project {name: row.project})
        MATCH (s:System {name: row.system})
        MERGE (p)-[:DECIDED]->(d)
        MERGE (d)-[:DECIDED_IN]->(pr)
        MERGE (d)-[:ABOUT]->(s)
        """,
        {"decisions": DECISIONS},
    )

    # 11. Doc Relationships: AUTHORED, ABOUT
    g.query(
        """
        UNWIND $docs AS row
        MATCH (dc:Doc {title: row.title})
        MATCH (p:Person {name: row.author})
        MATCH (s:System {name: row.system})
        MERGE (p)-[:AUTHORED]->(dc)
        MERGE (dc)-[:ABOUT]->(s)
        """,
        {"docs": DOCS},
    )

    return get_graph_counts(g)


def get_graph_counts(g=None) -> Dict[str, Any]:
    if g is None:
        g = get_graph()
    
    # Node counts by label
    label_res = g.query("MATCH (n) RETURN labels(n)[0] AS label, count(n) AS cnt ORDER BY label")
    node_counts = {row[0]: row[1] for row in label_res.result_set}
    
    # Relationship counts by type
    rel_res = g.query("MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS cnt ORDER BY rel_type")
    rel_counts = {row[0]: row[1] for row in rel_res.result_set}

    total_nodes = sum(node_counts.values())
    total_rels = sum(rel_counts.values())

    return {
        "nodes": node_counts,
        "relationships": rel_counts,
        "total_nodes": total_nodes,
        "total_relationships": total_rels,
    }


if __name__ == "__main__":
    print(f"Connecting to FalkorDB at {HOST}:{PORT}, graph '{GRAPH_NAME}'...")
    counts = seed_graph()
    print("Seed completed successfully!")
    print("\n--- Node Counts ---")
    for lbl, cnt in counts["nodes"].items():
        print(f"  {lbl}: {cnt}")
    print(f"Total Nodes: {counts['total_nodes']}")

    print("\n--- Relationship Counts ---")
    for rel, cnt in counts["relationships"].items():
        print(f"  {rel}: {cnt}")
    print(f"Total Relationships: {counts['total_relationships']}")
