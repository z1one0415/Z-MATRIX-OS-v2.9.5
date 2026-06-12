"""Read-only holdings packet for the Z-MATRIX cockpit frontend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_HOLDINGS_SNAPSHOT = Path(
    "data/research_db/account/raw/z_prime_holdings_snapshot_2026-06-04.json"
)
SAMPLE_HOLDINGS_SNAPSHOT = Path("data/samples/z_prime_holdings_snapshot_2026-06-04.json")
DEFAULT_HOLDINGS_PACKET = Path("runtime_reports/cockpit/holdings_packet.json")


def load_holdings_snapshot(path: str | Path = DEFAULT_HOLDINGS_SNAPSHOT) -> dict[str, Any]:
    snapshot_path = _resolve_snapshot_path(Path(path))
    if not snapshot_path.exists():
        return {
            "workspace_id": "ws_personal_z_prime",
            "as_of": "",
            "account": {},
            "positions": [],
            "data_status": "DATA_INSUFFICIENT",
            "blocked_reason": f"missing holdings snapshot: {snapshot_path}",
        }
    return json.loads(snapshot_path.read_text(encoding="utf-8"))


def _resolve_snapshot_path(path: Path) -> Path:
    if path.exists():
        return path
    if path == DEFAULT_HOLDINGS_SNAPSHOT and SAMPLE_HOLDINGS_SNAPSHOT.exists():
        return SAMPLE_HOLDINGS_SNAPSHOT
    return path


def build_holdings_packet(
    *,
    workspace_id: str = "ws_personal_z_prime",
    snapshot_path: str | Path = DEFAULT_HOLDINGS_SNAPSHOT,
) -> dict[str, Any]:
    snapshot = load_holdings_snapshot(snapshot_path)
    account = snapshot.get("account") or {}
    positions = snapshot.get("positions") or []

    if not account:
        return _empty_packet(workspace_id, snapshot.get("blocked_reason", "account snapshot is missing"))

    market_value = _num(account.get("market_value"))
    total_assets = _num(account.get("total_assets"))
    cash = _num(account.get("cash"))
    day_reference_pnl = _num(account.get("day_reference_pnl"))

    packet_positions = [_position_packet(row, market_value) for row in positions]
    review_count = sum(1 for row in packet_positions if row["reviewStatus"] == "待复核")

    return {
        "workspaceId": workspace_id,
        "asOf": snapshot.get("as_of", ""),
        "source": snapshot.get("source", "ACCOUNT_SNAPSHOT"),
        "account": {
            "totalAssets": total_assets,
            "floatingPnl": _num(account.get("floating_pnl")),
            "dayReferencePnl": day_reference_pnl,
            "marketValue": market_value,
            "cash": cash,
            "withdrawable": _num(account.get("withdrawable")),
            "currency": account.get("currency", "CNY"),
            "accountMask": account.get("account_mask", ""),
        },
        "kpi": {
            "todayPnl": day_reference_pnl,
            "todayPnlPct": _pct(day_reference_pnl, total_assets),
            "totalAsset": total_assets,
            "holdingAlphaAnnualized": None,
            "cashRatio": _pct(cash, total_assets),
            "maxDrawdownRecentYear": None,
            "dataFreshness": "FRESH" if positions else "PARTIAL",
        },
        "curveStats": [
            {"label": "累计收益", "value": "待导入", "tone": "muted"},
            {"label": "年化收益", "value": "待归因", "tone": "muted"},
            {"label": "波动率", "value": "待计算", "tone": "muted"},
            {"label": "夏普比率", "value": "待计算", "tone": "muted"},
            {"label": "最大回撤", "value": "待计算", "tone": "muted"},
        ],
        "positions": packet_positions,
        "observationWarehouses": _observation_warehouses(packet_positions),
        "todos": _todos(packet_positions, review_count),
        "audit": _audit_block(),
    }


def export_holdings_packet(
    output_path: str | Path = DEFAULT_HOLDINGS_PACKET,
    *,
    workspace_id: str = "ws_personal_z_prime",
    snapshot_path: str | Path = DEFAULT_HOLDINGS_SNAPSHOT,
) -> dict[str, Any]:
    packet = build_holdings_packet(workspace_id=workspace_id, snapshot_path=snapshot_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return packet


def _empty_packet(workspace_id: str, reason: str) -> dict[str, Any]:
    return {
        "workspaceId": workspace_id,
        "asOf": "",
        "blockedReason": reason,
        "account": {
            "totalAssets": 0,
            "floatingPnl": 0,
            "dayReferencePnl": 0,
            "marketValue": 0,
            "cash": 0,
            "withdrawable": 0,
            "currency": "CNY",
            "accountMask": "",
        },
        "kpi": {
            "todayPnl": 0,
            "todayPnlPct": 0,
            "totalAsset": 0,
            "holdingAlphaAnnualized": None,
            "cashRatio": 0,
            "maxDrawdownRecentYear": None,
            "dataFreshness": "PARTIAL",
        },
        "curveStats": [],
        "positions": [],
        "observationWarehouses": [],
        "todos": [{"time": "--:--", "title": "等待账户快照导入", "tone": "gold"}],
        "audit": _audit_block(),
    }


def _position_packet(row: dict[str, Any], portfolio_market_value: float) -> dict[str, Any]:
    market_value = _num(row.get("market_value"))
    return {
        "symbol": str(row.get("symbol", "")),
        "name": str(row.get("name", "")),
        "role": row.get("role", "DEFENSIVE"),
        "marketValue": market_value,
        "weightPct": _pct(market_value, portfolio_market_value),
        "floatingPnl": _num(row.get("floating_pnl")),
        "floatingPnlPct": _num(row.get("floating_pnl_pct")),
        "alphaContributionPct": row.get("alpha_contribution_pct"),
        "signalStrength": row.get("signal_strength", "LOW"),
        "thesisStatus": row.get("thesis_status", "WATCH"),
        "catalystStatus": row.get("catalyst_status", "NONE"),
        "nextAction": row.get("next_action", "DATA_INSUFFICIENT"),
        "quantity": int(row.get("quantity", 0) or 0),
        "available": int(row.get("available", 0) or 0),
        "costPrice": _num(row.get("cost_price")),
        "currentPrice": _num(row.get("current_price")),
        "reviewStatus": row.get("review_status", "只读观察"),
        "riskTag": row.get("risk_tag", "正收益观察"),
    }


def _observation_warehouses(positions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    core = [p for p in positions if p["role"] in {"CORE", "DEFENSIVE"}]
    rotation = [p for p in positions if p["role"] == "ROTATION"]
    return [
        _warehouse("CORE_OBSERVATION", "底仓观察", core, "稳定", "green"),
        _warehouse("ROTATION_OBSERVATION", "轮动观察", rotation, "关注", "gold"),
        {
            "warehouseType": "DARK_HORSE_OBSERVATION",
            "title": "黑马观察",
            "count": 0,
            "pendingActionCount": 0,
            "todayChange": "无新增",
            "outcomeStatus": "空仓",
            "tone": "gold",
            "topCandidates": [
                {
                    "ticker": "PENDING",
                    "name": "等待投研问股输入",
                    "oneLineReason": "由候选池进入观察",
                    "validationStatus": "PENDING",
                }
            ],
        },
    ]


def _warehouse(
    warehouse_type: str,
    title: str,
    positions: list[dict[str, Any]],
    outcome_status: str,
    tone: str,
) -> dict[str, Any]:
    pending = [p for p in positions if p["reviewStatus"] == "待复核"]
    return {
        "warehouseType": warehouse_type,
        "title": title,
        "count": len(positions),
        "pendingActionCount": len(pending),
        "todayChange": f"新增复核 {len(pending)} 项" if pending else "无新增",
        "outcomeStatus": outcome_status,
        "tone": tone,
        "topCandidates": [_candidate_from_position(p) for p in positions[:3]],
    }


def _candidate_from_position(position: dict[str, Any]) -> dict[str, str]:
    return {
        "ticker": position["symbol"],
        "name": position["name"],
        "oneLineReason": position["riskTag"],
        "validationStatus": "NEED_REVIEW" if position["reviewStatus"] == "待复核" else "OUTPERFORMING",
    }


def _todos(positions: list[dict[str, Any]], review_count: int) -> list[dict[str, str]]:
    if not positions:
        return [{"time": "--:--", "title": "等待账户快照导入", "tone": "gold"}]
    review_items = [
        {"time": "09:30", "title": f"复核{p['name']}研究路径", "tone": "red"}
        for p in positions
        if p["reviewStatus"] == "待复核"
    ]
    review_items.append({"time": "14:30", "title": f"生成持仓只读审计包（{review_count} 项）", "tone": "gold"})
    return review_items


def _audit_block() -> dict[str, Any]:
    return {
        "paperOnly": True,
        "humanReview": True,
        "brokerRuntime": "BLOCKED",
        "realTrade": "BLOCKED",
        "dataScope": "WORKSPACE_SCOPED",
    }


def _num(value: Any) -> float:
    try:
        return round(float(value), 4)
    except (TypeError, ValueError):
        return 0.0


def _pct(part: float, whole: float) -> float:
    if not whole:
        return 0.0
    return round(part / whole * 100, 2)
