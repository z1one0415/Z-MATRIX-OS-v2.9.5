"""Read-only history packet for the Z-MATRIX cockpit frontend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_HISTORY_PACKET = Path("runtime_reports/cockpit/history_packet.json")
REPORT_ROOTS = (
    Path("runtime_reports/audit"),
    Path("runtime_reports/cases"),
    Path("runtime_reports/research/factors"),
)


def build_history_packet(*, workspace_id: str = "ws_personal_z_prime") -> dict[str, Any]:
    files = _collect_report_files()
    audit_files = [p for p in files if "audit" in p.as_posix().lower()]
    case_files = [p for p in files if "cases" in p.as_posix()]
    factor_files = [p for p in files if "research/factors" in p.as_posix()]
    events = _events_from_files(files[:8])

    return {
        "workspaceId": workspace_id,
        "asOf": "2026-06-13",
        "source": "RUNTIME_REPORTS_READ_MODEL",
        "safety": {
            "paperOnly": True,
            "humanReviewRequired": True,
            "brokerRuntime": "BLOCKED",
            "realTrade": "BLOCKED",
            "agentDirectMutationAllowed": False,
            "dataScope": "WORKSPACE_SCOPED",
        },
        "kpis": [
            {"label": "累计报告", "value": f"{len(files):,}", "note": "runtime reports", "delta": "+0", "tone": "gold"},
            {"label": "实盘案例", "value": f"{len(case_files):,}", "note": "case chain assets", "delta": "+0", "tone": "gold"},
            {"label": "系统记忆", "value": f"{len(factor_files):,}", "note": "factor/research artifacts", "delta": "+0", "tone": "green"},
            {"label": "规则候选", "value": f"{len(audit_files):,}", "note": "audit artifacts", "delta": "+0", "tone": "gold"},
            {"label": "待清理记忆", "value": "0", "note": "not scheduled", "delta": "0", "tone": "muted"},
        ],
        "learningPipeline": [
            {"nodeId": "REPORT", "displayName": "分析报告", "count": len(files), "monthlyDelta": 0, "status": "READY"},
            {"nodeId": "CASE", "displayName": "实盘案例", "count": len(case_files), "monthlyDelta": 0, "status": "PARTIAL"},
            {"nodeId": "MEMORY", "displayName": "系统记忆", "count": len(factor_files), "monthlyDelta": 0, "status": "PARTIAL"},
            {"nodeId": "RULE_CANDIDATE", "displayName": "规则候选", "count": len(audit_files), "monthlyDelta": 0, "status": "PARTIAL"},
            {"nodeId": "FROZEN_RULE", "displayName": "固化规则", "count": 0, "monthlyDelta": 0, "status": "PENDING"},
        ],
        "monthlyStats": {
            "month": "2026-06",
            "newItems": len(files),
            "verified": _count_status(files, "CONFIRMED"),
            "falsified": _count_status(files, "BLOCKED"),
            "crystallized": _count_status(files, "PASS"),
            "promotable": _count_status(files, "ALLOWED"),
        },
        "events": events,
        "reportLibrary": _library_items(audit_files[:3], "审计报告"),
        "caseLibrary": _library_items(case_files[:3], "案例链"),
        "memoryRuleSummary": {
            "memories": [
                {"label": "核心永固记忆", "count": len(factor_files)},
                {"label": "时效性记忆", "count": len(case_files)},
                {"label": "待清理记忆", "count": 0},
            ],
            "rules": [
                {"label": "待验证", "count": 0},
                {"label": "验证中", "count": len(audit_files)},
                {"label": "待复核", "count": 0},
                {"label": "可晋级", "count": _count_status(files, "ALLOWED")},
            ],
        },
        "spaceTimeSeal": {
            "summary": [
                {"label": "报告", "value": str(len(files)), "detail": "已索引", "tone": "gold"},
                {"label": "案例", "value": str(len(case_files)), "detail": "只读复盘", "tone": "gold"},
                {"label": "记忆", "value": str(len(factor_files)), "detail": "研究资产", "tone": "green"},
                {"label": "规则候选", "value": str(len(audit_files)), "detail": "待验证", "tone": "gold"},
                {"label": "清理项", "value": "0", "detail": "未启用", "tone": "muted"},
            ],
            "alert": {"title": "时空预鉴", "level": "H3", "summary": "历史资产已完成只读索引，规则沉淀仍需人工复核。"},
            "bookmarks": [
                {"title": "可复现链", "body": "V11/V12/V13", "verdict": "标签", "tone": "green"},
                {"title": "审计资产", "body": "runtime audit", "verdict": "标签", "tone": "gold"},
                {"title": "待服务化", "body": "report drilldown", "verdict": "标签", "tone": "gold"},
            ],
        },
        "todos": [
            {"time": "09:30", "title": "刷新历史报告索引", "status": "待处理"},
            {"time": "10:00", "title": "复核可晋级规则候选", "status": "待处理"},
            {"time": "14:30", "title": "导出历史回溯审计包", "status": "待处理"},
        ],
        "systemStatus": {
            "reportIndex": "READY",
            "caseRegistry": "PARTIAL",
            "memoryRegistry": "PARTIAL",
            "ruleRegistry": "PARTIAL",
            "auditPack": "READY",
            "researchDb": "READY",
            "lastUpdatedAt": "2026-06-13",
        },
        "backendMapping": {
            "reportLibrary": "runtime_reports/*",
            "auditEvidence": "runtime_reports/audit",
            "evidenceChain": "runtime_reports/cases",
            "caseRegistry": "runtime_reports/cases",
            "replay": "historical_replay",
            "memoryDraft": "MemoryCandidate Preview",
            "ruleCandidate": "Rule Candidate Miner",
        },
    }


def export_history_packet(
    output_path: str | Path = DEFAULT_HISTORY_PACKET,
    *,
    workspace_id: str = "ws_personal_z_prime",
) -> dict[str, Any]:
    packet = build_history_packet(workspace_id=workspace_id)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return packet


def _collect_report_files() -> list[Path]:
    files: list[Path] = []
    for root in REPORT_ROOTS:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix in {".json", ".csv", ".md"})
    return sorted(files, key=lambda path: path.as_posix())


def _events_from_files(files: list[Path]) -> list[dict[str, Any]]:
    events = []
    for index, path in enumerate(files, start=1):
        title = path.stem.replace("_", " ")
        events.append(
            {
                "eventId": f"HE-RUNTIME-{index:03d}",
                "date": "2026-06-13",
                "targetName": title[:32],
                "targetCode": path.suffix.lstrip(".").upper() or "FILE",
                "eventType": "策略复盘",
                "conclusion": "已纳入驾驶舱只读历史索引",
                "outcomeStatus": "待验证",
                "memoryStatus": "时效性记忆",
                "ruleStatus": "观察中",
                "evidenceStatus": "审计包",
            }
        )
    return events


def _library_items(files: list[Path], item_type: str) -> list[dict[str, str]]:
    return [
        {
            "itemId": f"{item_type}-{index:03d}",
            "date": "2026-06-13",
            "title": path.stem.replace("_", " "),
            "type": item_type,
            "status": "已沉淀",
        }
        for index, path in enumerate(files, start=1)
    ]


def _count_status(files: list[Path], token: str) -> int:
    count = 0
    for path in files:
        try:
            if token in path.read_text(encoding="utf-8", errors="ignore"):
                count += 1
        except OSError:
            continue
    return count
