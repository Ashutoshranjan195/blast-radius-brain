# Blast Radius Brain — 3-Minute Demo Video Script

**Title**: Blast Radius Brain: Why Graph Traversal Outperforms Vector RAG for Company Intelligence  
**Track**: 03 — Company Brain (Graph Hacks: Give Your AI Agents Real Context)  
**Presenter**: Solo Builder / Senior Full-Stack Engineer  

---

## [0:00 – 0:30] The Problem: Why Vector RAG Fails Blast Radius

*(Visual: Slide or split screen showing a prompt: "What breaks if ledger-service goes down?" and a traditional Vector RAG returning generic runbooks without dependency chains.)*

**Voiceover:**
"When an incident strikes at 3:00 AM, the first question on-call engineers ask is: *'What breaks if this system goes down?'*

Today, teams build AI agents with Vector RAG. But vector similarity cannot answer topological questions. Similarity search matches keywords like 'ledger' and 'service', dumping paragraphs of runbooks. It has zero concept of multi-hop dependency chains. It can't tell you that `checkout-ui` breaks because it calls `payments-api`, which calls `ledger-service`.

Vector search is probabilistic and blind to topology. Today, we're introducing **Blast Radius Brain**—an agent built on **FalkorDB** where the knowledge graph is load-bearing, queries are deterministic Cypher traversals, and every answer is backed by verifiable provenance."

---

## [0:30 – 1:30] Live Demo: The Three Mission-Critical Questions

*(Visual: Screen switches to the Streamlit UI running at `http://localhost:8501`. Dark mode, glassmorphic layout, live graph health in sidebar: 42 nodes, 85 relationships.)*

### Question 1: Blast Radius Traversal
*(Visual: Click '💥 What breaks if ledger-service goes down?')*

**Voiceover:**
"First, let's ask: *'What breaks if ledger-service goes down?'*

Notice what happens. In under 15 milliseconds, FalkorDB executes a multi-hop `DEPENDS_ON` traversal. 
The agent reports that **6 downstream systems will be affected**:
- Immediate tier-1 impacts: `billing-cron`, `payments-api`, and `reporting-batch` (1 hop).
- Cascading tier-2 failures: `checkout-ui`, `mobile-gateway`, and `refund-worker` (2 hops).

Look right below the answer: here are the **traced graph paths** rendered as interactive chips:
`ledger-service → payments-api → checkout-ui` and `ledger-service → payments-api → refund-worker`.
Below that, we see the exact Cypher query, parameter bindings, and the raw row results. There is zero hallucination: the answer is the exact projection of the graph."

### Question 2: Expert Finder
*(Visual: Click '🧑‍💻 Who knows ledger-service best?')*

**Voiceover:**
"Next, an incident commander needs the right engineer immediately: *'Who knows ledger-service best?'*

Rather than guessing from git commits, the agent runs a graph join:
`(Person)-[:WORKS_ON]->(Project)-[:USES]->(System)`
FalkorDB ranks engineers by how many active projects they lead or work on that directly touch `ledger-service`.
Top expert: **Maya Chen**, Staff Engineer, connected via projects `Helios`, `Atlas`, and `Zephyr` with a score of 3, followed by Diego Ramos and Marco Silva. We get actionable on-call routing with proven attribution."

### Question 3: Decision Provenance
*(Visual: Click '📋 Who decided to pause Helios?')*

**Voiceover:**
"Finally: *'Who decided to pause Helios, and why?'*

The agent traverses `(Decision)-[:DECIDED_IN]->(Project)` and `(Person)-[:DECIDED]->(Decision)`.
It uncovers: *'Pause Helios rollout'*, paused on 2026-09-12 by Engineering Manager **Nora Haddad**, citing a staging latency regression on `ledger-service`. 
We just connected infrastructure telemetry, team knowledge, and governance into a single explainable trail."

---

## [1:30 – 2:30] FalkorDB Browser: Under the Hood

*(Visual: Switch browser tab to FalkorDB Web Browser at `http://localhost:3000`.)*

**Voiceover:**
"Now let's see why FalkorDB makes this possible. 

Here in the FalkorDB Browser on port 3000, we're inspecting our `company` graph.
FalkorDB represents graph structures directly using sparse GraphBLAS adjacency matrices inside Redis. This gives us sub-millisecond multi-hop matrix multiplications.

Let's execute the live Cypher query:
```cypher
MATCH path = (s:System {name: 'ledger-service'})<-[:DEPENDS_ON*1..5]-(downstream:System)
RETURN path
```

Look at the visual graph: `ledger-service` sits at the epicenter. We see directed dependency edges radiating out to `payments-api`, and expanding further to `checkout-ui` and `mobile-gateway`.

When we inspect our data model:
- 10 core systems and 11 dependency links
- 14 engineers across 8 cross-functional projects
- 5 formal decisions and 5 design/runbook docs

Because FalkorDB is Cypher-native, our seed is 100% idempotent using `MERGE` and `UNWIND`, and our application runs natively without any external LLM requirement."

---

## [2:30 – 3:00] The Provenance Guarantee & Conclusion

*(Visual: Return to the Streamlit UI, expanding the 'Raw Evidence Rows' and 'Discovered Node IDs & Metadata' accordions.)*

**Voiceover:**
"To wrap up: notice the **Evidence Contract** attached to every single tool response:
1. Canonical natural-language summary
2. Exact Cypher query and parameters
3. Discrete node path arrays
4. Node internal IDs (`id(n)`) and labels
5. Raw rows straight from the FalkorDB engine

If an OpenAI or Anthropic API key is provided, the LLM acts purely as an intent router and explainer. If no API key is present, our deterministic keyword router takes over seamlessly with 100% offline uptime.

**Blast Radius Brain** proves that for critical operational decisions, AI agents don't need fuzzy similarity—they need deterministic, verifiable graph traversal. 

Code, seed scripts, acceptance tests, and Docker setup are all open source on GitHub. Thank you!"
