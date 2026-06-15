"""Position Context Provider — read-only position data loader.

Reads from ~/.zmatrix/private_position_context.json if available,
falls back to data/examples/position_context.example.json.
NEVER generates BUY/ADD/SELL.
"""
from pathlib import Path
import json

def load_position_context(ticker: str) -> dict:
    """Load position context for a ticker. Returns safe defaults if unavailable."""
    private = Path.home() / ".zmatrix" / "private_position_context.json"
    source = private if private.exists() else Path("data/examples/position_context.example.json")
    if not source.exists():
        return _default_position()
    try:
        data = json.loads(source.read_text())
        holdings = data.get("holdings", data) if isinstance(data, dict) else {}
        if ticker in holdings:
            return holdings[ticker]
        return _default_position()
    except (json.JSONDecodeError, KeyError, OSError):
        return _default_position()

def _default_position() -> dict:
    return {
        "shares": 0.0, "avg_cost": None, "planned_entry_price": None,
        "position_state": "NO_POSITION", "cost_line_source": "none",
        "ma60_deviation_pct": None, "oversold_zscore": None,
        "fundamental_deteriorated": False,
    }
