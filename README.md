# ⚡ Blast Radius Brain (Aurora Labs)

> **Blast Radius Brain** is a deterministic graph intelligence agent built on **FalkorDB** for incident response and socio-technical enterprise context. Unlike Vector RAG, which flattens dependencies into fuzzy semantic similarities, Blast Radius Brain answers complex multi-hop operational questions—downstream outage cascading ("What breaks?"), cross-functional expertise ("Who knows this?"), and architectural governance ("Who decided this and why?")—using mathematically exact Cypher traversals backed by an auditable evidence contract with zero hallucinations.

## 🌐 Live Demo & Deliverables

- **Live Public App**: [https://bring-intake-greater-beautiful.trycloudflare.com](https://bring-intake-greater-beautiful.trycloudflare.com)
- **Demo Video (3-min Walkthrough)**: [YouTube Link](https://youtu.be/OFr0tyOPqvo) | Local: [`capture/demo.mp4`](capture/demo.mp4)
- **Demo Script**: [`capture/demo_script.md`](capture/demo_script.md)
- **Side-Prize Blog Post**: [Dev.to Article](https://dev.to/ashutoshranjan/why-vector-rag-fails-blast-radius-questions-and-the-4-hop-cypher-query-that-fixes-it-68b) | Local: [`blog_post.md`](blog_post.md)
- **Production Audit & Logs**: [`capture/VIDEO_LOG.md`](capture/VIDEO_LOG.md) | [`capture/CAPTURE_LOG.md`](capture/CAPTURE_LOG.md)

---

## 📸 Screenshots Gallery

| Screen | Description | File |
|---|---|---|
| **01 Home** | Title, metrics (42 nodes, 85 rels), quick questions | [`capture/screenshots/01_home.png`](capture/screenshots/01_home.png) |
| **02 Blast Radius** | `ledger-service` downstream cascade with path chips & Cypher | [`capture/screenshots/02_blast_radius.png`](capture/screenshots/02_blast_radius.png) |
| **03 Expert Finder** | Maya Chen ranked #1 across 3 cross-functional projects | [`capture/screenshots/03_expert_finder.png`](capture/screenshots/03_expert_finder.png) |
| **04 Decision Provenance** | Nora Haddad "Pause Helios rollout" ADR with rationale | [`capture/screenshots/04_decision.png`](capture/screenshots/04_decision.png) |
| **05 Honest Unknown** | Zero hallucination on unknown entity "Project Phoenix" | [`capture/screenshots/05_honest_unknown.png`](capture/screenshots/05_honest_unknown.png) |
| **06 Graph Browser** | FalkorDB visual graph explorer on `:3000` | [`capture/screenshots/06_graph_browser.png`](capture/screenshots/06_graph_browser.png) |
| **07 Blast Radius Subgraph** | FalkorDB browser highlighting downstream outage subgraph | [`capture/screenshots/07_graph_ledger_highlight.png`](capture/screenshots/07_graph_ledger_highlight.png) |
| **08 Idempotent Seeding** | Terminal verifying exact 42 nodes & 85 rels twice | [`capture/screenshots/08_seed_counts.png`](capture/screenshots/08_seed_counts.png) |
| **09 Pytest Acceptance** | Terminal showing 6/6 tests passing in 1.14s | [`capture/screenshots/09_tests_passing.png`](capture/screenshots/09_tests_passing.png) |
| **10 Architecture Diagram** | Complete graph schema (5 node labels, 9 edge types) | [`capture/screenshots/10_architecture.png`](capture/screenshots/10_architecture.png) |

---

## 🚀 Quickstart (Under 2 Minutes)

### 1. Start FalkorDB Container
Run FalkorDB with the visual browser on port 3000 and the graph engine on port 6379:
```bash
docker run -d --name falkordb -p 6379:6379 -p 3000:3000 falkordb/falkordb:latest
```
*(Or use `docker-compose up -d`)*

### 2. Install Dependencies
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Seed the Graph (Idempotent)
Populate the Aurora Labs graph with systems, engineers, projects, decisions, and dependencies:
```bash
python seed.py
```
*Note: `seed.py` uses Cypher `MERGE` and `UNWIND`. Running it repeatedly is 100% idempotent and produces identical node and relationship counts.*

### 4. Run Acceptance Tests
Verify all 6 test suites against the live FalkorDB instance:
```bash
pytest -v
```

### 5. Launch the Streamlit Web UI
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser. (The interactive FalkorDB Browser is also available at **http://localhost:3000**).

---

## 🛡️ Why the Graph is Load-Bearing

| Operational Question | Vector RAG Failure Mode | FalkorDB Graph Traversal |
|---|---|---|
| **What breaks if `ledger-service` goes down?** | Matches words "ledger" and "service", dumping runbooks. Cannot compute multi-hop dependencies or transitive closures. | Evaluates `<-[:DEPENDS_ON*1..5]-` across GraphBLAS sparse matrices. Accurately reports direct impacts (`payments-api`) and 2-hop cascading impacts (`checkout-ui`, `mobile-gateway`). |
| **Who knows `ledger-service` best?** | Guesses based on git log text or stale wiki pages. | Deterministic graph join `(Person)-[:WORKS_ON]->(Project)-[:USES]->(System)` ranked by active project load (Maya Chen = 3 projects). |
| **Who decided to pause Helios and why?** | Struggles with fuzzy temporal links and disjoint ADR records. | Traces `(Decision)-[:DECIDED_IN]->(Project)` and `(Person)-[:DECIDED]->(Decision)` to surface Nora Haddad, status, date, and staging latency rationale. |

---

## 📊 Data Model & Schema

```
 (Person) ---[:WORKS_ON]---> (Project) ---[:USES]---> (System)
    |                           |                       |
    +-------[:LEADS]------------+                       ^
    |                                            [:DEPENDS_ON]
    +-------[:AUTHORED]--------> (Doc)                  |
    |                             |                     |
    |                             +------[:ABOUT]-------+
    |                                                   |
    +-------[:DECIDED]---------> (Decision)             |
                                  |                     |
                                  +---[:DECIDED_IN]-----+
                                  +---[:ABOUT]----------+
```

### Seed Entities Summary:
- **10 Systems**: `auth-service`, `notification-service`, `ledger-service`, `payments-api`, `checkout-ui`, `refund-worker`, `reporting-batch`, `billing-cron`, `search-service`, `mobile-gateway`.
- **11 System Dependencies**: Multi-hop directed `[:DEPENDS_ON]` edges.
- **14 Engineers & Staff**: Roles across Payments, Data, Platform, Checkout, Mobile, and Search.
- **8 Cross-Functional Projects**: `Helios`, `Atlas`, `Orion`, `Vega`, `Nova`, `Pulse`, `Quasar`, `Zephyr`.
- **5 Decisions & 5 Docs**: Traceable architectural decision records, design plans, and incident runbooks.

---

## 🛠️ The Three Core Cypher Queries

### 1. Blast Radius Analysis (`blast_radius`)
```cypher
MATCH path = (s:System {name: $system})<-[:DEPENDS_ON*1..5]-(downstream:System)
RETURN downstream.name AS affected_system,
       length(path) AS hops,
       [n IN nodes(path) | n.name] AS node_path,
       [r IN relationships(path) | type(r)] AS rel_path
ORDER BY hops, affected_system
```

### 2. Expert Finder (`expert_finder`)
```cypher
MATCH (p:Person)-[:WORKS_ON]->(proj:Project)-[:USES]->(s:System {name: $system})
RETURN p.name AS person, p.role AS role, p.team AS team,
       collect(DISTINCT proj.name) AS projects,
       count(DISTINCT proj) AS score
ORDER BY score DESC, person
LIMIT 5
```

### 3. Decision Provenance (`decision_provenance`)
```cypher
MATCH (dec:Decision)
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
LIMIT 5
```

---

## 📜 The Evidence Contract

Every tool execution returns a strict evidence dictionary ensuring 100% transparency:
```json
{
  "tool": "blast_radius",
  "question": "What breaks if ledger-service goes down?",
  "answer": "If 'ledger-service' goes down, 6 downstream systems will be affected...",
  "cypher": "MATCH path = (s:System {name: $system})<-[:DEPENDS_ON*1..5]-(downstream:System)...",
  "params": {"system": "ledger-service"},
  "evidence": {
    "nodes": [
      {"id": 2, "label": "System", "name": "ledger-service"},
      {"id": 3, "label": "System", "name": "payments-api"}
    ],
    "paths": [
      ["ledger-service", "payments-api", "checkout-ui"],
      ["ledger-service", "payments-api", "refund-worker"]
    ],
    "rows": [
      {
        "affected_system": "billing-cron",
        "hops": 1,
        "node_path": ["ledger-service", "billing-cron"],
        "rel_path": ["DEPENDS_ON"]
      }
    ]
  }
}
```
*Note on Node IDs*: FalkorDB internal node IDs are queried directly via `id(n)` and included under `evidence.nodes` alongside node labels and names.

---

## 🧠 Dual-Mode Router

1. **Deterministic Fallback (Default)**: 
   - No external API key required.
   - Dynamically inspects the graph for known system and project names at startup.
   - Deterministically dispatches based on intent keywords (`blast`, `break`, `expert`, `who knows`, `decide`, `pause`).
2. **Optional LLM Intent Router**:
   - Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in `.env`.
   - The LLM parses arbitrary natural language questions into the strict tool schema `{"tool": "...", "entity": "..."}`.
   - If the API key is absent or an API request fails, the router falls through to the deterministic fallback automatically.

---

## 📁 Repository Structure

```
blast-radius-brain/
├── README.md                   # Project documentation & pitch
├── requirements.txt            # Python dependencies (falkordb, streamlit, pytest, etc.)
├── .env.example                # Environment variable configuration
├── docker-compose.yml          # Convenience container configuration
├── seed.py                     # Idempotent graph seeder (MERGE & UNWIND)
├── graph_tools.py              # 3 deterministic tools + evidence contract
├── router.py                   # LLM router + deterministic keyword fallback
├── app.py                      # Streamlit UI with glassmorphic design & path chips
├── screenshot.png              # UI visual demonstration
├── tests/
│   └── test_tools.py           # 6 Pytest acceptance tests against live DB
├── blog_post.md                # Draft article for hackathon side prize
└── demo_script.md              # 3-minute video recording script
```

---

## 🧪 Acceptance Test Suite

Run `pytest -v` to validate:
- ✅ **Test 1 (`test_seed_idempotency`)**: Ensures running `seed.py` multiple times preserves exact node (42) and relationship (85) counts.
- ✅ **Test 2 (`test_blast_radius_ledger_service`)**: Confirms `payments-api` (1 hop), `checkout-ui` (2 hops), `refund-worker`, `reporting-batch`, `billing-cron`, and `mobile-gateway` are identified, with all paths starting at `ledger-service`.
- ✅ **Test 3 (`test_expert_finder_ledger_service`)**: Confirms Maya Chen is ranked top 3 and works on Helios.
- ✅ **Test 4 (`test_decision_provenance_helios`)**: Confirms "Pause Helios rollout" by Nora Haddad referencing `ledger-service`.
- ✅ **Test 5 (`test_router_deterministic_fallback`)**: Confirms routing functions 100% reliably with zero API keys.
- ✅ **Test 6 (`test_evidence_contract`)**: Verifies presence of non-empty `answer`, `cypher`, `params`, `paths`, and `rows`.

---

## 🏆 Hackathon Context

- **Event**: Graph Hacks: Give Your AI Agents Real Context (by WeMakeDevs + FalkorDB)
- **Track**: 03 — Company Brain
- **Database**: FalkorDB (Cypher-compatible GraphBLAS engine)

---

## 🤖 AI Assistant Disclosure (Rule 11 Compliance)

In accordance with Hackathon Rule 11, **Google Antigravity / Gemini** was used as an AI pair programming assistant for boilerplate code, test scaffolding, and video pipeline automation. All graph schema modeling, Cypher traversal queries (`DEPENDS_ON*1..5`, socio-technical joins), evidence contracts, and acceptance validations were verified, executed, and benchmarked by the team against live FalkorDB instances.
