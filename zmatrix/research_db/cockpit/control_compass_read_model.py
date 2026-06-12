"""Read-only control compass packet for the Z-MATRIX cockpit frontend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_CONTROL_COMPASS_PACKET = Path("runtime_reports/cockpit/control_compass_packet.json")
DEFAULT_SKILL_REGISTRY = Path("data/research_db/agent/registry/skill_registry.generated.json")
CASE_REPORTS = (
    Path("runtime_reports/cases/case_expansion_v11_closeout.json"),
    Path("runtime_reports/cases/v11_paper_watchlist_audit.json"),
    Path("runtime_reports/cases/v12_research_only_closeout.json"),
    Path("runtime_reports/cases/v12_5_multicycle_feedback_closeout.json"),
    Path("runtime_reports/cases/v13_0_research_restart_closeout.json"),
    Path("runtime_reports/cases/v13_5_13_tactical_monitoring_closeout.json"),
)


def build_control_compass_packet(
    *,
    workspace_id: str = "ws_personal_z_prime",
    registry_path: str | Path = DEFAULT_SKILL_REGISTRY,
) -> dict[str, Any]:
    reports = {path.stem: _load_json(path, {}) for path in CASE_REPORTS}
    registry = _load_json(Path(registry_path), [])
    registry_count = len(registry) if isinstance(registry, list) else 0
    domain_count = len({item.get("domain") for item in registry if isinstance(item, dict) and item.get("domain")})
    latest_status = _latest_status(reports)
    blocked_reports = _blocked_report_count(reports)
    audit_score = _audit_score(reports)

    return {
        "workspaceId": workspace_id,
        "asOf": "2026-06-13",
        "source": "RUNTIME_GOVERNANCE_READ_MODEL",
        "safety": {
            "paperOnly": True,
            "humanReviewRequired": True,
            "realTradeAllowed": False,
            "brokerOrderAllowed": False,
            "productionAllowed": False,
            "agentDirectMutationAllowed": False,
        },
        "kpi": {
            "governanceDomainCount": 8,
            "healthyDomainCount": max(0, 8 - blocked_reports),
            "healthScore": max(0, audit_score),
            "latestPaperHitRatePct": _number(reports["v12_5_multicycle_feedback_closeout"], "cycle2_hit_rate", 0.0),
            "weakenedSignalCount": _number(reports["v12_5_multicycle_feedback_closeout"], "weakened_after_second_cycle_count", 0),
            "pendingAdjudicationCount": blocked_reports,
            "optimizationSnapshotStatus": "READY",
            "pendingChangeCount": max(0, domain_count - 17),
            "blockedChangeCount": blocked_reports,
            "monthlyInternalizationPct": 56,
            "auditCompletenessPct": audit_score,
            "configVersion": "v13.5.13",
            "dataFreshness": "FRESH",
        },
        "governanceDomains": _governance_domains(reports),
        "selectedDomain": {
            "selectedDomainId": "FACTOR_SIGNAL",
            "selectedDomainName": "因子信号门",
            "currentValue": {"label": "当前阶段", "value": latest_status},
            "suggestedValue": {"label": "系统建议", "value": "等待新增 OOS 数据后复核"},
            "impactScope": {
                "relatedParameterCount": registry_count,
                "affectedModuleCount": domain_count,
                "affectedPages": ["投研选股", "历史回溯", "天机罗盘", "大衍天问"],
            },
            "validationStatus": {
                "paperValidationPassed": blocked_reports == 0,
                "confidencePct": audit_score,
                "method": "runtime reports + SkillOS registry",
            },
            "auditStatus": {"status": "PENDING_EXPERT_REVIEW", "expectedFinishAt": "2026-06-14 14:00"},
        },
        "sandbox": {
            "draft": {
                "draftId": "CC-RUNTIME-20260613",
                "domainId": "FACTOR_SIGNAL",
                "affectedParameterCount": registry_count,
                "version": "runtime-governance v13.5.13",
            },
            "impact": {
                "impactLevel": "MID",
                "coverage": "HIGH",
                "strategyImpact": "研究链保持只读，新增样本后再复核",
                "internalizationImpactPct": 4,
            },
            "risk": {
                "riskLevel": "MID" if blocked_reports else "LOW",
                "potentialImpact": "若新增样本不足，因子晋级继续延后",
                "varianceRange": [-1.2, 0.8],
                "blockingCount": blocked_reports,
            },
            "paperValidation": {
                "method": "多轮纸面跟踪与审计",
                "sampleSize": _number(reports["v13_0_research_restart_closeout"], "accepted_candidate_count", 0),
                "passRatePct": audit_score,
                "conclusion": "PASSED" if blocked_reports == 0 else "INSUFFICIENT",
            },
            "humanReview": {"status": "PENDING", "requiredReviewerCount": 2, "estimatedMinutes": 90},
        },
        "ruling": {
            "draftId": "CC-RUNTIME-20260613",
            "evidenceChain": {"linkedEvidenceCount": len([data for data in reports.values() if data]), "completenessPct": audit_score},
            "expertReview": {"required": 2, "passed": 0, "expectedFinishAt": "2026-06-14 14:00"},
            "auditResult": {"status": "PENDING", "completenessPct": audit_score},
            "rulingStatus": {"status": "PENDING", "changeWindowOpen": False},
        },
        "optimizationSummary": {
            "systemVersion": "Z-MATRIX v13.5.13",
            "suggestedVersion": "v13.5.13 review draft",
            "latestCycleId": "V13.5.13",
            "headline": "等待真实新增样本，研究链继续停在只读监控。",
            "evidence": f"SkillOS registry {registry_count} skills / {domain_count} domains",
            "snapshotId": "CC-SNAP-20260613-01",
            "snapshotStatus": "READY",
            "restoreAvailable": True,
        },
        "parameterFamilies": _parameter_families(reports),
        "calibrationDisputes": [
            {
                "disputeId": "DISPUTE-OOS-001",
                "domainId": "FACTOR_SIGNAL",
                "title": "新增样本不足",
                "reason": "V13.5.13 未取得真实新增 OOS 月份，因子链保持复核态。",
                "severity": "MID",
                "humanReviewRequired": True,
            },
            {
                "disputeId": "DISPUTE-REGISTRY-001",
                "domainId": "EXPERIENCE_INTERNALIZATION",
                "title": "SkillOS 合流后需压平审计",
                "reason": "注册表已扩展，需要保持驾驶舱只读映射。",
                "severity": "LOW",
                "humanReviewRequired": True,
            },
        ],
        "derivationPanel": {
            "dashboard": {
                "configVersion": "v13.5.13",
                "pendingApprovalCount": blocked_reports,
                "blockedCount": blocked_reports,
                "internalizationPct": 56,
                "doNotChangeTodayCount": 3,
            },
            "riftAlerts": [
                {
                    "alertId": "RIFT-OOS-20260613",
                    "level": "L3",
                    "title": "新增 OOS 数据不足",
                    "summary": "当前候选保留，等待下一轮真实样本。",
                    "affectedDomainIds": ["FACTOR_SIGNAL", "SAMPLE_POOL"],
                    "actionRequired": True,
                }
            ],
            "seals": [
                {
                    "sealType": "STABLE",
                    "title": "稳定印",
                    "summary": "SkillOS 注册与只读域保持稳定",
                    "targetDomainIds": ["DATA_QUALITY", "EXPERIENCE_INTERNALIZATION"],
                },
                {
                    "sealType": "CALIBRATION",
                    "title": "校准印",
                    "summary": "因子与样本池等待新增样本",
                    "targetDomainIds": ["FACTOR_SIGNAL", "SAMPLE_POOL"],
                },
                {
                    "sealType": "FORBIDDEN",
                    "title": "禁改印",
                    "summary": "券商、生产与真实交易链保持锁定",
                    "targetDomainIds": ["D_MATRIX", "R_MATRIX"],
                },
            ],
        },
        "todos": [
            {"todoId": "cc-refresh-01", "sourceType": "AUDIT_REVIEW", "priority": "HIGH", "title": "复核 V13.5.13 样本状态", "dueTime": "09:30", "status": "PENDING"},
            {"todoId": "cc-registry-01", "sourceType": "MONTHLY_INTERNALIZATION", "priority": "MID", "title": "核对 SkillOS 注册表映射", "dueTime": "10:30", "status": "PENDING"},
            {"todoId": "cc-export-01", "sourceType": "AUDIT_REVIEW", "priority": "MID", "title": "导出天机罗盘审计包", "dueTime": "14:30", "status": "PENDING"},
        ],
        "systemStatus": {
            "marketData": "READY",
            "financialData": "READY",
            "macroData": "READY",
            "strategyEngine": "READY",
            "riskEngine": "READY",
            "dataService": "READY",
            "configRegistry": "READY",
            "auditService": "READY",
            "lastUpdatedAt": "2026-06-13",
        },
    }


def export_control_compass_packet(
    output_path: str | Path = DEFAULT_CONTROL_COMPASS_PACKET,
    *,
    workspace_id: str = "ws_personal_z_prime",
) -> dict[str, Any]:
    packet = build_control_compass_packet(workspace_id=workspace_id)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return packet


def _governance_domains(reports: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _domain("DATA_QUALITY", 1, "数据质量门", 8, "STABLE", 0, "LOW"),
        _domain("SAMPLE_POOL", 2, "样本池韧性", 7, "NEED_CALIBRATION", _blocked_report_count(reports), "MID"),
        _domain("FACTOR_SIGNAL", 3, "因子信号门", 6, "UNDER_REVIEW", _blocked_report_count(reports), "MID"),
        _domain("CATALYST_CYCLE", 4, "催化周期门", 5, "STABLE", 0, "LOW"),
        _domain("B_MATRIX", 5, "B-Matrix 底仓", 4, "STABLE", 0, "LOW"),
        _domain("R_MATRIX", 6, "R-Matrix 轮动", 3, "NEED_CALIBRATION", 1, "MID"),
        _domain("D_MATRIX", 7, "D-Matrix 黑马", 2, "UNDER_REVIEW", 1, "MID"),
        _domain("EXPERIENCE_INTERNALIZATION", 8, "经验内化", 1, "STABLE", 0, "LOW"),
    ]


def _domain(
    domain_id: str,
    index: int,
    name: str,
    ring_index: int,
    status: str,
    pending_changes: int,
    risk_level: str,
) -> dict[str, Any]:
    return {
        "domainId": domain_id,
        "index": index,
        "displayName": name,
        "ringIndex": ring_index,
        "status": status,
        "pendingChanges": pending_changes,
        "riskLevel": risk_level,
        "lastReviewedAt": "2026-06-13 09:42",
    }


def _parameter_families(reports: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    blocked = _blocked_report_count(reports)
    return [
        _family("PF-DATA-QUALITY", "DATA_QUALITY", "数据健康与泄漏门", "数据新鲜度、覆盖率、泄漏审计", "data gate", "STABLE", "保持当前门槛"),
        _family("PF-SAMPLE-POOL", "SAMPLE_POOL", "样本池韧性与矩阵时钟", "池规模、月份覆盖、样本有效性", "sample gate", "DRIFTING" if blocked else "STABLE", "等待新增 OOS 样本"),
        _family("PF-FACTOR-SIGNAL", "FACTOR_SIGNAL", "因子信号与晋级门", "RankIC、decay、horizon、纸面跟踪", "factor gate", "WEAKENED" if blocked else "STABLE", "延后因子晋级"),
        _family("PF-CATALYST-CYCLE", "CATALYST_CYCLE", "催化周期门", "叙事水温、催化半衰期、事件回链", "catalyst cycle", "STABLE", "保持复核节奏"),
        _family("PF-B-MATRIX", "B_MATRIX", "B-Matrix 底仓质量门", "评级 cap、估值上下文、Thesis Stop", "b matrix", "STABLE", "保持底仓质量门"),
        _family("PF-R-MATRIX", "R_MATRIX", "R-Matrix 轮动门", "Hurst、半衰期、波动衰减", "r matrix", "DRIFTING", "复核轮动参数"),
        _family("PF-D-MATRIX", "D_MATRIX", "D-Matrix 黑马源点门", "黑马基因、主题种子、M1 覆盖", "d matrix", "LOW_SAMPLE", "补充 M1 覆盖证据"),
        _family("PF-EXPERIENCE-INTERNALIZATION", "EXPERIENCE_INTERNALIZATION", "经验内化", "安全硬门、Z9 反馈、月度内化", "memory gate", "STABLE", "保持人审门"),
    ]


def _family(
    family_id: str,
    domain_id: str,
    label: str,
    scope: str,
    backend_mapping: str,
    drift_status: str,
    advice: str,
) -> dict[str, Any]:
    return {
        "familyId": family_id,
        "domainId": domain_id,
        "label": label,
        "scope": scope,
        "backendMapping": backend_mapping,
        "currentVersion": "runtime v13.5.13",
        "systemOptimizedVersion": "runtime v13.5.13-review",
        "currentSignal": drift_status,
        "optimizationAdvice": advice,
        "paperReview": "只读审计，人审后再入下一阶段",
        "driftStatus": drift_status,
        "editableMode": "DRAFT_ONLY",
        "snapshotRequired": True,
        "restoreAvailable": True,
    }


def _latest_status(reports: dict[str, dict[str, Any]]) -> str:
    for key in ("v13_5_13_tactical_monitoring_closeout", "v13_0_research_restart_closeout", "v12_research_only_closeout"):
        status = reports.get(key, {}).get("status")
        if status:
            return str(status)
    return "WAITING_FOR_RUNTIME_REPORT"


def _blocked_report_count(reports: dict[str, dict[str, Any]]) -> int:
    count = 0
    for report in reports.values():
        if not report:
            count += 1
            continue
        if report.get("blocking_reasons") or "BLOCKED" in str(report.get("status", "")):
            count += 1
    return count


def _audit_score(reports: dict[str, dict[str, Any]]) -> float:
    total = max(len(reports), 1)
    passed = total - _blocked_report_count(reports)
    return round(passed / total * 100, 1)


def _number(data: dict[str, Any], key: str, default: float | int) -> float | int:
    value = data.get(key, default)
    if isinstance(value, (int, float)):
        return value
    return default


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))
