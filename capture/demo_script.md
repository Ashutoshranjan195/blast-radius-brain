# Blast Radius Brain — 3-Minute Demo Video Script (180 Seconds)

**Target Duration**: 180 seconds (Allowed: 170–185s)  
**Total Word Count**: 259 words (Allowed: ≤ 450 words)  
**Format**: 1080p 1920x1080 H.264 @ 30fps  
**Audio**: 48kHz Stereo AAC, Normalized to -16 LUFS  

---

### Scene 1 — The Problem (0:00–0:15 / 15s)
- **Visual**: `01_home.png` — Aurora Labs home screen with title, metrics sidebar, and clean interface.
- **On-Screen Overlay**: Top banner: *"Vector RAG gives you similar documents. It cannot tell you what breaks."*
- **Voiceover (0:01–0:12)**:
  > *"Vector RAG gives you similar documents. It cannot tell you what breaks when a service goes down. This is Blast Radius Brain — a company brain where the graph does the reasoning."*

---

### Scene 2 — Blast Radius Hero (0:15–0:50 / 35s)
- **Visual**: `02_blast_radius.png` — Question submitted, answer card, and **traced path chips** clearly visible.
- **On-Screen Overlay**: Highlight badges: `payments-api — 1 hop`, `checkout-ui — 2 hops`, path chip: `ledger-service → payments-api → checkout-ui`.
- **Path Chips Visibility**: Held on screen for > 15 seconds (requirement: ≥ 5s).
- **Voiceover (0:16–0:32)**:
  > *"The agent traverses the dependency graph. payments-api breaks immediately. checkout-ui, two hops away, also breaks. Every affected system comes with the exact path the graph followed."*

---

### Scene 3 — Cypher Proof (0:50–1:05 / 15s)
- **Visual**: Zoomed / highlighted focus on the executed Cypher query box: `MATCH path = (s:System {name: $system})<-[:DEPENDS_ON*1..5]-(downstream:System)`.
- **On-Screen Overlay**: Lower-third: *"The answer is a traversal — not a similarity search."*
- **Cypher Visibility**: Visible for 15 seconds (requirement: ≥ 4s).
- **Voiceover (0:51–1:03)**:
  > *"This is not a guess. This is the exact Cypher query. A variable-length traversal over DEPENDS_ON edges. Deterministic, auditable, fast enough to run on every agent step."*

---

### Scene 4 — Expert Finder (1:05–1:25 / 20s)
- **Visual**: `03_expert_finder.png` — Ranked domain expert results.
- **On-Screen Overlay**: Callout on `Maya Chen (Staff Engineer, Payments)` with score 3 across projects `Zephyr`, `Atlas`, and `Helios`.
- **Voiceover (1:06–1:20)**:
  > *"The same graph ranks experts by project overlap. Maya Chen has worked on three projects that use ledger-service. No embeddings. Just a join the graph already stores."*

---

### Scene 5 — Decision Provenance (1:25–1:45 / 20s)
- **Visual**: `04_decision.png` — Architectural decision provenance record for Helios.
- **On-Screen Overlay**: Provenance trail: `Nora Haddad` (author) → `Pause Helios rollout` → `ledger-service` latency regression.
- **Voiceover (1:26–1:38)**:
  > *"Every decision traces back to its author, the project it was made in, and the systems it affects. A decision with an audit trail built into the graph."*

---

### Scene 6 — Honest Unknown (1:45–2:00 / 15s)
- **Visual**: `05_honest_unknown.png` — Question "Who owns Project Phoenix?".
- **On-Screen Overlay**: Lower-third: *"When the graph doesn't have it, the agent says so."*
- **Voiceover (1:46–1:56)**:
  > *"And when the graph doesn't know, it says so. No hallucination. The evidence layer is honest about missing data."*

---

### Scene 7 — FalkorDB Browser (2:00–2:30 / 30s)
- **Visual**: `06_graph_browser.png` and `07_graph_ledger_highlight.png` — FalkorDB Browser running at `localhost:3000` with the live graph canvas and blast radius subgraph.
- **On-Screen Overlay**: Top banner: *"The graph is the reasoning layer."*
- **Voiceover (2:01–2:18)**:
  > *"This is the graph underneath. Every answer you saw is a traversal over these nodes and edges. The FalkorDB Browser shows the same query running live — and the same subgraph the agent used."*

---

### Scene 8 — Engineering Credibility (2:30–2:50 / 20s)
- **Visual**: Split screen — Left: `08_seed_counts.png` (idempotent seed run twice) | Right: `09_tests_passing.png` (pytest 6/6 passed).
- **On-Screen Overlay**: Lower-third: *"Idempotent seed. Deterministic tools. Passing tests."*
- **Voiceover (2:31–2:44)**:
  > *"The seed is idempotent — running it twice produces the same graph. The tools are deterministic. The tests pass. This is a working system, not a mockup."*

---

### Scene 9 — Close & Architecture (2:50–3:00 / 10s)
- **Visual**: `10_architecture.png` / End Card with GitHub repository, live demo URL, and track info.
- **On-Screen Overlay**: Center card: *"Blast Radius Brain — Track 03: Company Brain"*  
  - Live Demo: `https://tune-explosion-stainless-nicholas.trycloudflare.com`  
  - GitHub: `https://github.com/Ashutoshranjan195/blast-radius-brain`
- **Voiceover (2:50–2:58)**:
  > *"Blast Radius Brain. A company brain where the graph is the reasoning layer — and every answer ships with its evidence."*
