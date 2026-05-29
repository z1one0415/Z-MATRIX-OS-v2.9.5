# allowlist: forbidden-token-definition
"""BMO Risk Isolation Unit — preview isolation of a ticker under tail risk"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY

ISOLATION_VERSION = "BMO_RISK_ISOLATION_PREVIEW_V10"


def build_risk_isolation_preview(
    *,
    source_result: dict,
    position_context: dict | None = None,
) -> dict:
    seed = f"{source_result.get('gate_id','')}|{source_result.get('decision','')}"
    isolate_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    ticker = (position_context or {}).get("ticker", "")
    role = (position_context or {}).get("role", "")
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "isolation_id": isolate_id,
        "isolation_version": ISOLATION_VERSION,
        "source_gate_id": source_result.get("gate_id", ""),
        "ticker": ticker,
        "role": role,
        "isolation_reason": source_result.get("reason", ""),
        "net_value_markdown_preview": None,
        "allow_balance_add": False,
        "allow_revenge_trade": False,
        "allow_average_down": False,
        "requires_human_review": True,
        "created_at": created_at,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "auto_sell_allowed": False,
        "auto_position_close_allowed": False,
        "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
