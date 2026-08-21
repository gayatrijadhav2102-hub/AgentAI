"""
HR MCP Server
=============
An MCP (Model Context Protocol) server that exposes company HR knowledge
(policies, benefits, and FAQs) as tools an AI agent can call.

Data is simple in-memory mock data (see hr_data.py) — swap that module out
for a real database / HRIS / document store later without touching the
tool definitions below.

Run standalone (stdio transport, the default MCP transport for local
agents / Claude Desktop):

    python hr_mcp_server.py

Or install for Claude Desktop with the `mcp` CLI:

    mcp install hr_mcp_server.py
"""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from hr_data import BENEFITS, FAQS, POLICIES

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

mcp = MCPServer(
    name="hr-agent",
    title="HR Knowledge Server",
    description=(
        "Exposes company HR policies, benefits information, and FAQs so an "
        "agent can answer employee questions accurately."
    ),
    instructions=(
        "Use these tools to look up authoritative HR information before "
        "answering employee questions. Prefer get_policy / get_benefit for "
        "precise lookups, and search_hr_knowledge when the user's question "
        "doesn't map cleanly to a known topic name. Never invent policy "
        "details that aren't returned by these tools — if nothing relevant "
        "is found, say so and suggest the employee contact HR directly."
    ),
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_policies() -> list[str]:
    """List the titles of every HR policy available in the knowledge base."""
    return sorted(POLICIES.keys())


@mcp.tool()
def get_policy(policy_name: str) -> str:
    """Get the full text of a specific HR policy.

    Args:
        policy_name: The policy title, e.g. "Remote Work Policy". Case
            insensitive; use list_policies() to see valid options.
    """
    match = _find_key_case_insensitive(POLICIES, policy_name)
    if match is None:
        available = ", ".join(sorted(POLICIES.keys()))
        return (
            f"No policy found matching '{policy_name}'. "
            f"Available policies: {available}"
        )
    return f"# {match}\n\n{POLICIES[match]}"


@mcp.tool()
def list_benefits() -> list[str]:
    """List the names of all employee benefits documented in the knowledge base."""
    return sorted(BENEFITS.keys())


@mcp.tool()
def get_benefit(benefit_name: str) -> str:
    """Get details about a specific employee benefit.

    Args:
        benefit_name: The benefit name, e.g. "Health Insurance" or "401(k)".
            Case insensitive; use list_benefits() to see valid options.
    """
    match = _find_key_case_insensitive(BENEFITS, benefit_name)
    if match is None:
        available = ", ".join(sorted(BENEFITS.keys()))
        return (
            f"No benefit found matching '{benefit_name}'. "
            f"Available benefits: {available}"
        )
    return f"# {match}\n\n{BENEFITS[match]}"


@mcp.tool()
def search_faq(query: str) -> list[dict]:
    """Search frequently-asked-questions by keyword.

    Args:
        query: Free-text search terms, e.g. "sick leave" or "parking".

    Returns:
        A list of matching {"question": ..., "answer": ...} entries, ranked
        by how many query words they match. Empty list if nothing matches.
    """
    terms = [t.lower() for t in query.split() if t.strip()]
    if not terms:
        return []

    scored: list[tuple[int, dict]] = []
    for entry in FAQS:
        haystack = f"{entry['question']} {entry['answer']}".lower()
        score = sum(haystack.count(term) for term in terms)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [entry for _, entry in scored]


@mcp.tool()
def search_hr_knowledge(query: str) -> dict:
    """Search across policies, benefits, and FAQs at once by keyword.

    Use this when you're not sure whether the answer lives in a policy,
    a benefit description, or an FAQ. For precise, known-topic lookups
    prefer get_policy / get_benefit instead.

    Args:
        query: Free-text search terms, e.g. "maternity leave".

    Returns:
        A dict with "policies", "benefits", and "faqs" keys, each a list
        of matching titles/entries.
    """
    terms = [t.lower() for t in query.split() if t.strip()]

    def matches(text: str) -> bool:
        text = text.lower()
        return any(term in text for term in terms)

    matched_policies = [
        {"title": title, "excerpt": _excerpt(body, terms)}
        for title, body in POLICIES.items()
        if matches(title) or matches(body)
    ]
    matched_benefits = [
        {"name": name, "excerpt": _excerpt(body, terms)}
        for name, body in BENEFITS.items()
        if matches(name) or matches(body)
    ]
    matched_faqs = search_faq(query)

    return {
        "policies": matched_policies,
        "benefits": matched_benefits,
        "faqs": matched_faqs,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _find_key_case_insensitive(d: dict, key: str) -> str | None:
    key_lower = key.strip().lower()
    for k in d:
        if k.lower() == key_lower:
            return k
    # fallback: substring match
    for k in d:
        if key_lower in k.lower():
            return k
    return None


def _excerpt(text: str, terms: list[str], context_chars: int = 120) -> str:
    lower = text.lower()
    for term in terms:
        idx = lower.find(term.lower())
        if idx != -1:
            start = max(0, idx - context_chars // 2)
            end = min(len(text), idx + len(term) + context_chars // 2)
            prefix = "..." if start > 0 else ""
            suffix = "..." if end < len(text) else ""
            return f"{prefix}{text[start:end].strip()}{suffix}"
    return text[:context_chars] + ("..." if len(text) > context_chars else "")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
