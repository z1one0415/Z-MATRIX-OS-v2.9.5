"""Account Position Provider v1.0 — single source for portfolio positions.

All pipelines (G09/G11/G13/G17/G18) must use this instead of parsing MEMORY.md directly.
"""
from __future__ import annotations
from pathlib import Path
import re, os


def load_positions(memory_path: str | None = None) -> dict:
    """Load positions from MEMORY.md. Returns standardized position dict."""
    if memory_path is None:
        memory_path = os.environ.get(
            "Z_MATRIX_MEMORY_FILE",
            str(Path.home() / ".openclaw" / "agents" / "z2-analyst" / "workspace" / "MEMORY.md")
        )
    mem = Path(memory_path)
    if not mem.exists():
        return _empty_positions()

    text = mem.read_text()
    positions = []
    for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|\s*([\d.]+)\s*\|', text):
        positions.append({
            "ticker": m.group(2),
            "name": m.group(1).strip(),
            "shares": int(m.group(3).replace("股", "").replace(",", "")),
            "cost": float(m.group(4)),
            "source": "MEMORY_MD_REGEX",
            "confidence": "LOW_ACCOUNT_TRUTH",
        })

    return {
        "positions": positions,
        "cash": {"connected": False, "cash_source": "NOT_CONNECTED"},
        "account_truth": {"connected": False, "confidence": "LOW_ACCOUNT_TRUTH"},
        "count": len(positions),
    }


def _empty_positions() -> dict:
    return {
        "positions": [],
        "cash": {"connected": False, "cash_source": "NOT_CONNECTED"},
        "account_truth": {"connected": False, "confidence": "LOW_ACCOUNT_TRUTH"},
        "count": 0,
    }
