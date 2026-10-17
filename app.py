"""
Blast Radius Brain — Streamlit Web Application
Aurora Labs Knowledge Graph Agent powered by FalkorDB
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from seed import get_graph_counts, get_graph
from router import route
from graph_tools import blast_radius, expert_finder, decision_provenance, get_known_systems

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Blast Radius Brain — Aurora Labs",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (Dark sleek glassmorphism & typography)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    code, pre, [class*="stCode"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Title Styling */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFA834 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    /* Glassmorphic Cards */
    .answer-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 107, 107, 0.25);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .answer-card h4 {
        color: #F8FAFC;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .answer-card p {
        color: #E2E8F0;
        font-size: 1.05rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Path Chip Styling */
    .path-container {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        margin-bottom: 1.25rem;
    }
    .path-row {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.4rem;
        background: rgba(15, 23, 42, 0.6);
        padding: 0.5rem 0.8rem;
        border-radius: 8px;
        border-left: 3px solid #FF8E53;
    }
    .path-node {
        background: #1E293B;
        color: #38BDF8;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        font-weight: 500;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .path-node.root {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border-color: rgba(239, 68, 68, 0.4);
    }
    .path-node.target {
        background: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border-color: rgba(34, 197, 94, 0.4);
    }
    .path-arrow {
        color: #94A3B8;
        font-weight: bold;
        font-size: 0.9rem;
    }

    /* Sidebar Health Card */
    .health-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(34, 197, 94, 0.15);
        color: #22C55E;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    /* Router Badge */
    .router-badge {
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        background: #334155;
        color: #CBD5E1;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: Graph Health & Links
with st.sidebar:
    st.markdown("### 🌐 Graph Health")
    try:
        counts = get_graph_counts()
        st.markdown(
            f'<span class="health-pill">● FALKORDB CONNECTED</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Graph: `{os.getenv('FALKORDB_GRAPH', 'company')}`")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Nodes", counts["total_nodes"])
        with col2:
            st.metric("Relationships", counts["total_relationships"])

        with st.expander("Node Breakdown", expanded=False):
            for lbl, cnt in counts["nodes"].items():
                st.write(f"• **{lbl}**: {cnt}")

        with st.expander("Relationship Breakdown", expanded=False):
            for rel, cnt in counts["relationships"].items():
                st.write(f"• **{rel}**: {cnt}")

    except Exception as e:
        st.error(f"FalkorDB Connection Error: {e}")
        st.caption("Ensure FalkorDB docker container is running.")

    st.markdown("---")
    st.markdown("### 🖥️ FalkorDB Browser")
    st.markdown(
        "[Open FalkorDB Browser ↗](http://localhost:3000)",
        help="Interactive graph visualization interface on port 3000",
    )
    st.caption("Connect host: `localhost`, port: `6379`")

    st.markdown("---")
    st.markdown("### 🛡️ Provenance Guarantee")
    st.info(
        "**Zero Halucination**: Every answer is a deterministic Cypher graph traversal. "
        "Full query, parameters, node paths, and raw graph rows are attached below each response."
    )


# Main Content Area
st.markdown('<div class="hero-title">⚡ Blast Radius Brain</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Deterministic Graph Intelligence for Aurora Labs Infrastructure & Teams</div>',
    unsafe_allow_html=True,
)

# Example Buttons
st.markdown("**Quick Examples (click to test):**")
btn_col1, btn_col2, btn_col3 = st.columns(3)

example_selected = None
with btn_col1:
    if st.button("💥 What breaks if ledger-service goes down?", use_container_width=True):
        example_selected = "What breaks if ledger-service goes down?"
with btn_col2:
    if st.button("🧑‍💻 Who knows ledger-service best?", use_container_width=True):
        example_selected = "Who knows ledger-service best?"
with btn_col3:
    if st.button("📋 Who decided to pause Helios?", use_container_width=True):
        example_selected = "Who decided to pause Helios?"

# Search Input
default_query = example_selected or ""
query_input = st.text_input(
    "Ask a question about systems, dependencies, experts, or decisions:",
    value=default_query,
    placeholder="e.g. What breaks if payments-api goes down? or Who knows auth-service best?",
)

submit_btn = st.button("Execute Graph Query", type="primary")

# Execute query if clicked or entered
active_query = default_query if example_selected else (query_input if submit_btn else "")

if active_query:
    with st.spinner("Traversing knowledge graph..."):
        routing = route(active_query)

        if routing["tool"] == "clarification":
            st.warning(routing["message"])
        else:
            tool_name = routing["tool"]
            entity = routing["entity"]
            router_type = routing.get("router_type", "deterministic")

            # Execute Deterministic Graph Tool
            if tool_name == "blast_radius":
                result = blast_radius(entity, question=active_query)
            elif tool_name == "expert_finder":
                result = expert_finder(entity, question=active_query)
            elif tool_name == "decision_provenance":
                result = decision_provenance(entity, question=active_query)
            else:
                st.error(f"Unknown tool: {tool_name}")
                st.stop()

            # 1. Answer Card
            router_badge_text = (
                "⚡ Deterministic Keyword Router"
                if router_type == "deterministic"
                else "🤖 LLM Intent Router"
            )
            st.markdown(
                f'<span class="router-badge">{router_badge_text} &bull; TOOL: {tool_name.upper()}</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="answer-card">
                    <h4>Graph Traversal Answer</h4>
                    <p>{result['answer']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 2. Path Chips
            paths = result["evidence"].get("paths", [])
            if paths:
                st.markdown("#### 🔗 Traced Graph Paths")
                path_html = '<div class="path-container">'
                for p in paths:
                    path_html += '<div class="path-row">'
                    for i, node in enumerate(p):
                        cls = "path-node"
                        if i == 0:
                            cls += " root"
                        elif i == len(p) - 1:
                            cls += " target"
                        path_html += f'<span class="{cls}">{node}</span>'
                        if i < len(p) - 1:
                            path_html += '<span class="path-arrow">&rarr;</span>'
                    path_html += '</div>'
                path_html += '</div>'
                st.markdown(path_html, unsafe_allow_html=True)

            # 3 & 4. Cypher & Parameters
            col_cyp, col_par = st.columns([3, 1])
            with col_cyp:
                st.markdown("#### ⚙️ Executed Cypher Query")
                st.code(result["cypher"], language="cypher")
            with col_par:
                st.markdown("#### 🎯 Parameters")
                st.json(result["params"])

            # 5. Raw Rows Expander
            with st.expander("📊 Raw Evidence Rows (FalkorDB ResultSet)", expanded=True):
                rows = result["evidence"].get("rows", [])
                if rows:
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)
                else:
                    st.caption("No matching rows returned by Cypher query.")

            # 6. Graph Nodes Metadata Expander
            nodes = result["evidence"].get("nodes", [])
            if nodes:
                with st.expander("🏷️ Discovered Node IDs & Metadata", expanded=False):
                    st.dataframe(pd.DataFrame(nodes), use_container_width=True)

