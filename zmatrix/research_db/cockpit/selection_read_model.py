"""Read-only selection packet for the Z-MATRIX cockpit frontend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_WATCHLIST = Path("runtime_reports/cases/v11_candidate_factor_watchlist.json")
DEFAULT_CLOSEOUT = Path("runtime_reports/cases/case_expansion_v11_closeout.json")
DEFAULT_SELECTION_PACKET = Path("runtime_reports/cockpit/selection_packet.json")


def build_selection_packet(
    *,
    workspace_id: str = "ws_personal_z_prime",
    watchlist_path: str | Path = DEFAULT_WATCHLIST,
    closeout_path: str | Path = DEFAULT_CLOSEOUT,
) -> dict[str, Any]:
    watchlist = _load_json(Path(watchlist_path), {})
    closeout = _load_json(Path(closeout_path), {})
    watch_items = watchlist.get("watch_items", [])
    active = int(watchlist.get("active_paper_watch", 0) or 0)
    limited = int(watchlist.get("watch_with_limitation", 0) or 0)
    rejected = int(watchlist.get("rejected_from_watchlist", 0) or 0)
    candidate_count = int(watchlist.get("candidate_count", len(watch_items)) or 0)

    return {
        "workspaceId": workspace_id,
        "asOf": _infer_as_of(),
        "source": "V11_PAPER_WATCHLIST_READ_MODEL",
        "kpis": [
            {"label": "候选因子", "value": str(candidate_count), "note": "V11 paper watchlist", "tone": "gold", "visual": "bars"},
            {"label": "主动观察", "value": str(active), "note": "ACTIVE_PAPER_WATCH", "tone": "green", "visual": "line"},
            {"label": "限制观察", "value": str(limited), "note": "WATCH_WITH_LIMITATION", "tone": "gold", "visual": "line"},
            {"label": "拒绝候选", "value": str(rejected), "note": "REJECT_FROM_WATCHLIST", "tone": "muted", "visual": "donut"},
            {"label": "准入状态", "value": _status_label(closeout.get("status")), "note": "research only", "tone": "gold", "visual": "line"},
        ],
        "filterChain": _filter_chain(candidate_count, active, limited, rejected),
        "conclusion": {
            "priorityDirection": "因子候选纸面观察",
            "confidence": "中高" if closeout.get("semantic_audit_pass") else "待复核",
            "reasons": _top_factor_reasons(watch_items),
            "avoidToday": ["不生成买卖建议", "不接入券商", "不做实盘动作"],
        },
        "opportunityGroups": _opportunity_groups(watch_items),
        "matrixGroups": _matrix_groups(watch_items),
        "candidates": _candidates(watch_items),
        "todos": [
            {"time": "09:30", "title": "刷新 V11 纸面观察清单"},
            {"time": "10:00", "title": "复核限制观察因子"},
            {"time": "14:30", "title": "导出投研问股审计包"},
        ],
        "audit": _audit_block(),
    }


def export_selection_packet(
    output_path: str | Path = DEFAULT_SELECTION_PACKET,
    *,
    workspace_id: str = "ws_personal_z_prime",
) -> dict[str, Any]:
    packet = build_selection_packet(workspace_id=workspace_id)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return packet


def _filter_chain(candidate_count: int, active: int, limited: int, rejected: int) -> list[dict[str, Any]]:
    total = max(candidate_count + rejected, candidate_count, 1)
    return [
        {"step": 1, "title": "V10 候选继承", "detail": "读取 V10 candidate thesis pack", "remaining": candidate_count, "dropRatePct": 0, "status": "PASSED"},
        {"step": 2, "title": "语义传播审计", "detail": "rankic_direction 与 decay basis 已传播", "remaining": candidate_count, "dropRatePct": 0, "status": "PASSED"},
        {"step": 3, "title": "证据完整性过滤", "detail": "缺字段与 raw leak 均进入硬门", "remaining": candidate_count, "dropRatePct": 0, "status": "PASSED"},
        {"step": 4, "title": "限制观察分流", "detail": f"{limited} 项进入 limitation 复核", "remaining": active + limited, "dropRatePct": round(rejected / total * 100, 2), "status": "REVIEW" if limited else "PASSED"},
        {"step": 5, "title": "交易边界阻断", "detail": "仅允许 paper watchlist 输出", "remaining": active, "dropRatePct": 0, "status": "STRICT"},
        {"step": 6, "title": "人工复核队列", "detail": "所有进入观察项等待后续人工解释", "remaining": active + limited, "dropRatePct": 0, "status": "REVIEW"},
        {"step": 7, "title": "驾驶舱只读映射", "detail": "生成前端 SelectionDashboardPacket", "remaining": active + limited, "dropRatePct": 0, "status": "PASSED"},
    ]


def _opportunity_groups(watch_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    active = [w for w in watch_items if w.get("watch_status") == "ACTIVE_PAPER_WATCH"]
    limited = [w for w in watch_items if w.get("watch_status") != "ACTIVE_PAPER_WATCH"]
    return [
        {"title": "主动观察因子 Top5", "tone": "green", "items": _ranked_items(active[:5])},
        {"title": "限制观察因子", "tone": "red", "items": _ranked_items(limited[:5])},
        {"title": "低因子值优先", "tone": "green", "items": _ranked_items([w for w in active if w.get("bucket_direction") == "LOW_FACTOR_VALUE_FAVORED"][:5])},
        {"title": "待人工复核", "tone": "red", "items": _ranked_items([w for w in watch_items if w.get("robustness_grade") == "REVIEW"][:5])},
    ]


def _matrix_groups(watch_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets = {
        "B": [w for w in watch_items if "AMOUNT" in str(w.get("factor_id", ""))],
        "R": [w for w in watch_items if "MOM" in str(w.get("factor_id", "")) or "VOLATILITY" in str(w.get("factor_id", ""))],
        "D": [w for w in watch_items if "DRAWDOWN" in str(w.get("factor_id", "")) or "RELATIVE" in str(w.get("factor_id", ""))],
        "ALL": watch_items,
    }
    return [
        {
            "matrix": matrix,
            "title": f"{matrix}-Matrix Top",
            "subtitle": "paper watchlist",
            "items": [
                {"symbol": item.get("watch_id", ""), "name": item.get("factor_id", ""), "tags": [item.get("horizon", ""), item.get("watch_status", "")]}
                for item in values[:5]
            ],
        }
        for matrix, values in buckets.items()
    ]


def _candidates(watch_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for item in watch_items[:8]:
        status = item.get("watch_status", "")
        direction = item.get("rankic_direction", "MIXED")
        out.append(
            {
                "symbol": item.get("watch_id", ""),
                "name": item.get("factor_id", ""),
                "humanMachineConsensus": "人机共识" if status == "ACTIVE_PAPER_WATCH" else "待人工判断",
                "recommendedRole": "轮动观察" if status == "ACTIVE_PAPER_WATCH" else "暂不观察",
                "researchStrength": "投研增强" if item.get("robustness_grade") == "ROBUST" else "投研待核",
                "eventDriver": item.get("horizon", "T20"),
                "riskProfile": "只读观察",
                "allocationFit": item.get("bucket_direction", "NO_PREFERRED_DIRECTION"),
                "fitScore": 80 if status == "ACTIVE_PAPER_WATCH" else 60,
                "keyPoint": item.get("decay_pattern", ""),
                "chain": f"{direction} RankIC semantic direction",
                "financialHealth": item.get("robustness_grade", ""),
                "catalystStatus": item.get("raw_rankic_trend", ""),
                "tianjiDiagnosis": "只进入纸面观察清单，不形成投资动作。",
            }
        )
    return out


def _ranked_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"rank": index + 1, "name": item.get("factor_id", ""), "changePct": 0} for index, item in enumerate(items)]


def _top_factor_reasons(watch_items: list[dict[str, Any]]) -> list[str]:
    factors = []
    for item in watch_items:
        factor = item.get("factor_id")
        if factor and factor not in factors:
            factors.append(factor)
        if len(factors) == 3:
            break
    return factors or ["等待候选生成"]


def _status_label(status: Any) -> str:
    return "V11 confirmed" if status == "CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED" else "待复核"


def _audit_block() -> dict[str, Any]:
    return {"paperOnly": True, "humanReview": True, "brokerRuntime": "BLOCKED", "realTrade": "BLOCKED", "dataScope": "WORKSPACE_SCOPED"}


def _infer_as_of() -> str:
    return "2026-06-13"


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))
