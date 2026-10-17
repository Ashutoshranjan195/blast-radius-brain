"""
Router for Blast Radius Brain.
Supports optional LLM routing (OpenAI or Anthropic) and deterministic keyword fallback.
Loads known systems dynamically from the graph.
"""

import os
import re
import json
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

from graph_tools import get_known_systems

load_dotenv()

ALLOWED_TOOLS = ["blast_radius", "expert_finder", "decision_provenance"]

# Common stopwords to strip when extracting decision query terms
STOPWORDS = {
    "who", "what", "where", "when", "why", "how", "did", "do", "does",
    "is", "are", "was", "were", "to", "the", "a", "an", "and", "or",
    "of", "in", "for", "on", "about", "paused", "pause", "decided", "decide",
    "decision", "tell", "me", "show", "can", "you", "please", "why did"
}


def _extract_known_system(text: str, known_systems: list[str]) -> Optional[str]:
    """Finds the first matching known system name in the user query."""
    text_lower = text.lower()
    for sys in sorted(known_systems, key=lambda s: len(s), reverse=True):
        if sys.lower() in text_lower:
            return sys
    return None


def _extract_decision_entity(question: str) -> str:
    """
    Extracts a meaningful entity/phrase for decision provenance queries.
    E.g., 'Who decided to pause Helios?' -> 'Helios'
    'Why was search-service deprecated?' -> 'search-service'
    """
    # Check if a known project is mentioned
    known_projects = ["Helios", "Atlas", "Orion", "Vega", "Nova", "Pulse", "Quasar", "Zephyr"]
    for proj in known_projects:
        if proj.lower() in question.lower():
            return proj

    # Check for known systems
    known_sys = get_known_systems()
    for sys in known_sys:
        if sys.lower() in question.lower():
            return sys

    # Tokenize and strip stopwords to find the distinctive subject
    tokens = re.findall(r"[A-Za-z0-9_-]+", question)
    filtered = [t for t in tokens if t.lower() not in STOPWORDS]
    if filtered:
        return " ".join(filtered)
    
    return question.strip()


def route_with_llm(question: str, known_systems: list[str]) -> Optional[Dict[str, str]]:
    """
    Optional LLM classification if OPENAI_API_KEY or ANTHROPIC_API_KEY is available.
    Returns {"tool": "...", "entity": "..."} or None if unavailable/fails.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not openai_key and not anthropic_key:
        return None

    prompt = f"""You are a query router for Aurora Labs' knowledge graph.
Classify the question into exactly one tool:
- "blast_radius": Questions about what breaks, outage impact, dependency chains, or cascading failures when a system fails.
- "expert_finder": Questions about who knows a system, who has experience with it, who worked on it, or team ownership.
- "decision_provenance": Questions about decisions, rollouts, freezes, deprecations, approvals, who decided, or why a change occurred.

Extract the relevant entity:
- For blast_radius and expert_finder, extract the exact system name from this list: {known_systems}.
- For decision_provenance, extract the project name, system name, or key topic keyword.

Respond ONLY with valid JSON in this format:
{{"tool": "blast_radius"|"expert_finder"|"decision_provenance", "entity": "<extracted_entity>"}}

Question: {question}"""

    # Try OpenAI
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            raw = resp.choices[0].message.content
            parsed = json.loads(raw)
            if parsed.get("tool") in ALLOWED_TOOLS and parsed.get("entity"):
                return {"tool": parsed["tool"], "entity": parsed["entity"]}
        except Exception:
            pass

    # Try Anthropic
    if anthropic_key:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=anthropic_key)
            resp = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                temperature=0.0,
                system="Respond with valid JSON only.",
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text
            # Extract json block
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                if parsed.get("tool") in ALLOWED_TOOLS and parsed.get("entity"):
                    return {"tool": parsed["tool"], "entity": parsed["entity"]}
        except Exception:
            pass

    return None


def route_deterministic(question: str, known_systems: list[str]) -> Dict[str, Any]:
    """
    Deterministic fallback routing logic based on keywords and known graph entities.
    """
    q_lower = question.lower()

    # Rule 1: blast_radius
    # contains break, down, impact, depends, blast
    blast_keywords = ["break", "down", "impact", "depends", "blast"]
    if any(kw in q_lower for kw in blast_keywords):
        system = _extract_known_system(question, known_systems)
        if not system:
            return {
                "tool": "clarification",
                "entity": "",
                "message": (
                    "Could not determine which system you are asking about. "
                    f"Known systems: {', '.join(known_systems)}"
                ),
            }
        return {"tool": "blast_radius", "entity": system}

    # Rule 2: expert_finder
    # contains who knows, expert, worked on, experience
    expert_keywords = ["who knows", "expert", "worked on", "experience"]
    if any(kw in q_lower for kw in expert_keywords):
        system = _extract_known_system(question, known_systems)
        if not system:
            return {
                "tool": "clarification",
                "entity": "",
                "message": (
                    "Could not determine which system you want an expert for. "
                    f"Known systems: {', '.join(known_systems)}"
                ),
            }
        return {"tool": "expert_finder", "entity": system}

    # Rule 3: decision_provenance
    # contains decide, decision, approved, why did, who paused
    decision_keywords = ["decide", "decision", "approved", "why did", "who paused", "pause"]
    if any(kw in q_lower for kw in decision_keywords):
        entity = _extract_decision_entity(question)
        return {"tool": "decision_provenance", "entity": entity}

    # Fallback heuristic: check if any known system is mentioned
    system = _extract_known_system(question, known_systems)
    if system:
        return {"tool": "blast_radius", "entity": system}

    return {
        "tool": "clarification",
        "entity": "",
        "message": (
            "I could not classify your query. Please ask a question about:\n"
            "1. Blast radius (e.g. 'What breaks if ledger-service goes down?')\n"
            "2. Expert finder (e.g. 'Who knows ledger-service best?')\n"
            "3. Decision provenance (e.g. 'Who decided to pause Helios?')"
        ),
    }


def route(question: str) -> Dict[str, Any]:
    """
    Main routing entrypoint.
    Checks LLM first if configured; falls back reliably to deterministic matching.
    """
    known_systems = get_known_systems()

    # 1. Try LLM if API keys are set
    llm_result = route_with_llm(question, known_systems)
    if llm_result:
        return {
            "tool": llm_result["tool"],
            "entity": llm_result["entity"],
            "router_type": "llm",
        }

    # 2. Fall back to deterministic keyword routing
    fallback_res = route_deterministic(question, known_systems)
    fallback_res["router_type"] = "deterministic"
    return fallback_res
