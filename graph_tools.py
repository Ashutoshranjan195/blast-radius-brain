"""
Deterministic graph tools for Blast Radius Brain with full Evidence Contract.
Every tool accepts an entity (and optional question) and returns the Evidence Contract.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from falkordb import FalkorDB

load_dotenv()

HOST = os.getenv("FALKORDB_HOST", "localhost")
PORT = int(os.getenv("FALKORDB_PORT", "6379"))
GRAPH_NAME = os.getenv("FALKORDB_GRAPH", "company")


def get_graph():
    db = FalkorDB(host=HOST, port=PORT)
    return db.select_graph(GRAPH_NAME)


def get_known_systems() -> List[str]:
    """Retrieve list of all known system names from the graph."""
    try:
        g = get_graph()
        res = g.query("MATCH (s:System) RETURN s.name AS name ORDER BY s.name")
        return [row[0] for row in res.result_set]
    except Exception:
        return [
            "auth-service",
            "notification-service",
            "ledger-service",
            "payments-api",
            "checkout-ui",
            "refund-worker",
            "reporting-batch",
            "billing-cron",
            "search-service",
            "mobile-gateway",
        ]


def blast_radius(system_name: str, question: Optional[str] = None) -> Dict[str, Any]:
    """
    Answers: What breaks if <system> goes down?
    Traverses multi-hop DEPENDS_ON incoming edges.
    """
    system_name = system_name.strip()
    q_str = question or f"What breaks if {system_name} goes down?"

    cypher = """MATCH path = (s:System {name: $system})<-[:DEPENDS_ON*1..5]-(downstream:System)
RETURN downstream.name AS affected_system,
       length(path) AS hops,
       [n IN nodes(path) | n.name] AS node_path,
       [r IN relationships(path) | type(r)] AS rel_path
ORDER BY hops, affected_system"""

    params = {"system": system_name}
    g = get_graph()
    res = g.query(cypher, params)

    raw_rows = []
    all_paths = []
    canonical_by_system = {}

    for row in res.result_set:
        affected = row[0]
        hops = row[1]
        node_path = row[2]
        rel_path = row[3]

        row_dict = {
            "affected_system": affected,
            "hops": hops,
            "node_path": node_path,
            "rel_path": rel_path,
        }
        raw_rows.append(row_dict)
        all_paths.append(node_path)

        # Canonical path = minimum hops
        if affected not in canonical_by_system or hops < canonical_by_system[affected]["hops"]:
            canonical_by_system[affected] = {
                "hops": hops,
                "node_path": node_path,
            }

    # Fetch node IDs for systems in paths
    node_metadata = []
    all_system_names = list({name for path in all_paths for name in path})
    if all_system_names:
        id_query = "MATCH (s:System) WHERE s.name IN $names RETURN id(s) AS id, s.name AS name"
        id_res = g.query(id_query, {"names": all_system_names})
        node_metadata = [{"id": row[0], "label": "System", "name": row[1]} for row in id_res.result_set]

    # Generate answer
    sorted_affected = sorted(canonical_by_system.items(), key=lambda x: (x[1]["hops"], x[0]))
    total_affected = len(sorted_affected)

    if total_affected == 0:
        answer = f"No downstream systems depend on '{system_name}'. Outage blast radius is isolated."
    else:
        breakdown_items = [f"{sys} ({info['hops']} hop{'s' if info['hops'] > 1 else ''})" for sys, info in sorted_affected]
        breakdown_str = ", ".join(breakdown_items)
        
        top3 = sorted_affected[:3]
        top3_paths_str = "; ".join([" -> ".join(info["node_path"]) for _, info in top3])

        answer = (
            f"If '{system_name}' goes down, {total_affected} downstream system{'s' if total_affected > 1 else ''} will be affected: "
            f"{breakdown_str}. "
            f"Shortest blast radius paths for the most critical dependencies: {top3_paths_str}."
        )

    return {
        "tool": "blast_radius",
        "question": q_str,
        "answer": answer,
        "cypher": cypher,
        "params": params,
        "evidence": {
            "nodes": node_metadata,
            "paths": all_paths,
            "rows": raw_rows,
        },
    }


def expert_finder(system_name: str, question: Optional[str] = None) -> Dict[str, Any]:
    """
    Answers: Who knows <system> best?
    Joins Person -[:WORKS_ON]-> Project -[:USES]-> System, ranked by distinct projects.
    """
    system_name = system_name.strip()
    q_str = question or f"Who knows {system_name} best?"

    cypher = """MATCH (p:Person)-[:WORKS_ON]->(proj:Project)-[:USES]->(s:System {name: $system})
RETURN p.name AS person, p.role AS role, p.team AS team,
       collect(DISTINCT proj.name) AS projects,
       count(DISTINCT proj) AS score
ORDER BY score DESC, person
LIMIT 5"""

    params = {"system": system_name}
    g = get_graph()
    res = g.query(cypher, params)

    raw_rows = []
    paths = []
    node_names = set()

    for row in res.result_set:
        person = row[0]
        role = row[1]
        team = row[2]
        projects = row[3]
        score = row[4]

        raw_rows.append({
            "person": person,
            "role": role,
            "team": team,
            "projects": projects,
            "score": score,
        })
        node_names.add(person)
        for prj in projects:
            node_names.add(prj)
            paths.append([person, prj, system_name])

    node_names.add(system_name)

    # Fetch node metadata
    node_metadata = []
    if node_names:
        id_query = "MATCH (n) WHERE n.name IN $names RETURN id(n) AS id, labels(n)[0] AS label, n.name AS name"
        id_res = g.query(id_query, {"names": list(node_names)})
        node_metadata = [{"id": row[0], "label": row[1], "name": row[2]} for row in id_res.result_set]

    # Generate answer
    if not raw_rows:
        answer = f"No active engineers found linked to projects utilizing '{system_name}'."
    else:
        top_candidates = raw_rows[:3]
        details = []
        for cand in top_candidates:
            details.append(f"{cand['person']} ({cand['role']}, {cand['team']}) via projects {', '.join(cand['projects'])} (score: {cand['score']})")
        details_str = "; ".join(details)
        answer = (
            f"Top domain expert{'s' if len(top_candidates) > 1 else ''} for '{system_name}': {details_str}. "
            f"The graph ranks them by the number of active projects they work on that directly utilize {system_name}."
        )

    return {
        "tool": "expert_finder",
        "question": q_str,
        "answer": answer,
        "cypher": cypher,
        "params": params,
        "evidence": {
            "nodes": node_metadata,
            "paths": paths,
            "rows": raw_rows,
        },
    }


def decision_provenance(query_text: str, question: Optional[str] = None) -> Dict[str, Any]:
    """
    Answers: Who decided to pause Helios, and why?
    Traces Decision -> author -> project -> systems.
    """
    q_clean = query_text.strip()
    q_str = question or f"Who decided '{q_clean}' and why?"

    cypher = """MATCH (dec:Decision)
WHERE toLower(dec.title) CONTAINS toLower($q)
   OR toLower(dec.summary) CONTAINS toLower($q)
OPTIONAL MATCH (dec)-[:DECIDED_IN]->(proj:Project)
OPTIONAL MATCH (author:Person)-[:DECIDED]->(dec)
OPTIONAL MATCH (dec)-[:ABOUT]->(s:System)
RETURN dec.title AS decision, dec.date AS date, dec.status AS status,
       dec.summary AS summary, proj.name AS project,
       author.name AS decided_by,
       collect(DISTINCT s.name) AS systems
ORDER BY date DESC
LIMIT 5"""

    params = {"q": q_clean}
    g = get_graph()
    res = g.query(cypher, params)

    raw_rows = []
    paths = []
    node_names = set()

    for row in res.result_set:
        title = row[0]
        date = row[1]
        status = row[2]
        summary = row[3]
        proj = row[4]
        decided_by = row[5]
        systems = row[6] or []

        raw_rows.append({
            "decision": title,
            "date": date,
            "status": status,
            "summary": summary,
            "project": proj,
            "decided_by": decided_by,
            "systems": systems,
        })

        if decided_by:
            node_names.add(decided_by)
        if proj:
            node_names.add(proj)
        for s in systems:
            node_names.add(s)
            if decided_by and proj:
                paths.append([decided_by, title, proj, s])
            elif decided_by:
                paths.append([decided_by, title, s])

    # Fetch node metadata
    node_metadata = []
    if node_names:
        id_query = "MATCH (n) WHERE n.name IN $names RETURN id(n) AS id, labels(n)[0] AS label, n.name AS name"
        id_res = g.query(id_query, {"names": list(node_names)})
        node_metadata = [{"id": row[0], "label": row[1], "name": row[2]} for row in id_res.result_set]

    # Generate answer
    if not raw_rows:
        answer = f"No decision records found matching '{q_clean}'."
    else:
        top_dec = raw_rows[0]
        sys_str = ", ".join(top_dec["systems"]) if top_dec["systems"] else "none specified"
        answer = (
            f"Decision: '{top_dec['decision']}' (Status: {top_dec['status']}, Date: {top_dec['date']}). "
            f"Decided by {top_dec['decided_by']} for project {top_dec['project']} affecting system(s): {sys_str}. "
            f"Summary: \"{top_dec['summary']}\""
        )

    return {
        "tool": "decision_provenance",
        "question": q_str,
        "answer": answer,
        "cypher": cypher,
        "params": params,
        "evidence": {
            "nodes": node_metadata,
            "paths": paths,
            "rows": raw_rows,
        },
    }
