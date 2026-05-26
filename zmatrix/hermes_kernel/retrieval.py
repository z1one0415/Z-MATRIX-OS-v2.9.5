"""Heuristic Retrieval Preview — lightweight tag matching, no vector DB, no network"""
from __future__ import annotations


def retrieve_relevant_heuristics(
    *,
    task: dict,
    heuristics: list[dict],
    max_results: int = 5,
) -> dict:
    """Retrieve relevant heuristics by matching ticker / role / chain / sector / scope.

    Lightweight tag matching only. No vector DB. No network. No memory write.
    """
    task_ticker = task.get("ticker", "")
    task_role = task.get("role", "")
    task_chain = task.get("chain", "")
    task_sector = task.get("sector", "")

    scored: list[tuple[int, dict]] = []

    for h in heuristics:
        score = 0
        scope = h.get("scope", {}) if isinstance(h.get("scope"), dict) else {}
        heuristic_data = h.get("heuristic", h)

        # Match ticker
        if task_ticker and scope.get("ticker") == task_ticker:
            score += 3
        # Match role
        if task_role and scope.get("role") == task_role:
            score += 2
        # Match chain
        if task_chain and scope.get("chain") == task_chain:
            score += 2
        # Match sector
        if task_sector and scope.get("sector") == task_sector:
            score += 1
        # Prefer active
        if heuristic_data.get("status") == "ACTIVE":
            score += 1

        if score > 0:
            scored.append((score, heuristic_data))

    scored.sort(key=lambda x: -x[0])
    matched = [h for _, h in scored[:max_results]]

    return {
        "matched_heuristics": matched,
        "match_count": len(matched),
        "preview_only": True,
        "write_allowed": False,
        "prompt_auto_injection_allowed": False,
    }
