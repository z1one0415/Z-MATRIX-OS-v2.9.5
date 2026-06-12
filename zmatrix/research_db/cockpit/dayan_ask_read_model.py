"""Read-only Dayan ask packet for the Z-MATRIX cockpit frontend."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_DAYAN_ASK_PACKET = Path("runtime_reports/cockpit/dayan_ask_packet.json")
DEFAULT_SKILL_REGISTRY = Path("data/research_db/agent/registry/skill_registry.generated.json")


def build_dayan_ask_packet(
    *,
    workspace_id: str = "ws_personal_z_prime",
    registry_path: str | Path = DEFAULT_SKILL_REGISTRY,
) -> dict[str, Any]:
    registry = _load_registry(Path(registry_path))
    risk_counts = Counter(str(item.get("risk_level", "")) for item in registry)
    domain_counts = Counter(str(item.get("domain", "UNKNOWN")) for item in registry)
    concrete_domains = len(domain_counts)
    registered_count = len(registry)

    return {
        "workspaceId": workspace_id,
        "asOf": "2026-06-13",
        "source": "SKILLOS_REGISTRY_READ_MODEL",
        "safety": _safety(),
        "altar": {
            "mode": "DEEP_RESEARCH",
            "modeLabel": "深度研究模式",
            "currentTopic": "从 SkillOS 能力图谱生成纸面研究链路",
            "researchScope": "ALL_MARKET",
            "researchScopeLabel": "A股全市场",
            "memoryContext": "LONG_MEMORY",
            "memoryContextLabel": "长链记忆",
            "safety": _safety(),
        },
        "formations": _formations(),
        "hermesGuidance": {
            "guidanceId": "HG-REGISTRY-20260613",
            "contextSummary": f"SkillOS 已注册 {registered_count} 个技能，覆盖 {concrete_domains} 个领域，当前只生成草案与审计参考。",
            "suggestions": [
                "优先选择研究链路编排，再补证据缺口。",
                "涉及组合与账户内容时只生成复核草案。",
                "所有能力调用保持人审与审计包约束。",
                "不触发券商、生产或真实交易链。",
            ],
            "missingInputs": ["研究主题", "观察周期", "证据材料"],
            "recommendedMethods": ["研究链路编排阵", "组合复核阵", "审计护法阵"],
            "quickQuestions": [
                "这个研究问题应该调用哪些技能？",
                "当前证据链还缺什么？",
                "帮我生成一条只读研究链路。",
                "把这次问答整理为人审草案。",
            ],
            "nextActionText": "生成研究链路草案",
            "hermesStatus": "常驻",
        },
        "advisoryGroups": [
            {"id": "research", "title": "研究编排", "description": "计划、检索、报告草案", "entries": ["研究计划", "证据缺口", "报告草案"]},
            {"id": "portfolio", "title": "组合复核", "description": "账户观察与风险预算草案", "entries": ["暴露模板", "风险预算", "复核草案"]},
            {"id": "governance", "title": "治理审计", "description": "规则、注册表与审计包", "entries": ["注册表", "硬门", "审计包"]},
            {"id": "memory", "title": "记忆沉淀", "description": "候选记忆与案例复盘", "entries": ["案例草案", "记忆候选", "复盘摘要"]},
        ],
        "forgeCandidates": [
            {
                "id": "forge-registry-001",
                "suggestedName": "SkillOS 研究链路框架 v0.1",
                "sourceCombination": ["研究链路编排阵", "审计护法阵"],
                "usageCount": risk_counts.get("R2_DRAFT", 0),
                "scenario": "研究草案",
                "status": "READY_TO_ADD",
                "safetyLevel": "PROPOSAL_REQUIRED",
            }
        ],
        "moveReview": [
            {
                "id": "move-registry-001",
                "date": "2026-06-13",
                "researchTopic": "SkillOS 合流后能力复核",
                "methodCombination": "研究链路编排阵 + 审计护法阵",
                "conclusion": "注册表可读，写入链仍需人审",
                "memoryStatus": "待人审",
            }
        ],
        "myMethods": [
            {
                "id": "my-registry-001",
                "name": "只读研究链路",
                "scenario": "系统复核",
                "promptTemplate": "请基于已注册技能生成研究链路草案，并列出证据缺口。",
                "composedSkills": ["workflow-plan", "audit-pack"],
                "status": "ACTIVE",
                "lastUsedAt": "2026-06-13",
                "usageCount": registered_count,
            }
        ],
        "skillCategories": _skill_categories(registry, domain_counts),
        "currentConversation": {
            "conversationId": "ask-registry-20260613-001",
            "topic": "研究主题：SkillOS 能力图谱复核",
            "selectedPromptFragments": ["研究链路编排阵", "审计护法阵"],
            "messages": [
                {
                    "id": "msg-registry-001",
                    "role": "HERMES",
                    "label": "问天",
                    "content": "已读取 SkillOS 注册表。当前建议先生成只读研究链路，再把证据缺口交给人审。",
                    "createdAt": "09:42",
                }
            ],
        },
        "latestHermesPlan": {
            "planId": "plan-registry-20260613-001",
            "userGoal": "从当前能力图谱生成研究链路",
            "interpretedTask": "技能选择 + 证据缺口 + 草案产出",
            "recommendedMethods": ["研究链路编排阵", "组合复核阵", "审计护法阵"],
            "executionSteps": [
                {
                    "order": 1,
                    "actionName": "选择技能组合",
                    "userVisiblePurpose": "确认研究路径",
                    "requiredInput": ["研究主题"],
                    "expectedOutput": "技能清单",
                },
                {
                    "order": 2,
                    "actionName": "生成证据缺口",
                    "userVisiblePurpose": "标记需要补证的材料",
                    "requiredInput": ["证据材料"],
                    "expectedOutput": "缺口清单",
                },
                {
                    "order": 3,
                    "actionName": "生成审计草案",
                    "userVisiblePurpose": "保留人审轨迹",
                    "requiredInput": ["前两步结论"],
                    "expectedOutput": "审计草案",
                },
            ],
            "missingInputs": ["研究主题", "观察周期"],
            "outputTarget": ["CHAT_ONLY", "REPORT_DRAFT", "AUDIT_CHECK"],
            "humanReviewRequired": True,
        },
        "voice": {"state": "READY", "label": "语音输入可用", "privacyNote": "仅转写到输入框，不写入正式库。"},
        "systemStatus": {
            "registeredMethodCount": registered_count,
            "concreteDomainCount": concrete_domains,
            "maxRiskLevel": "R2_DRAFT",
            "workflowMode": "DRY_RUN_ONLY",
            "registryMutation": "BLOCKED",
        },
        "backendMapping": {
            "registry": "skill_registry.generated.json",
            "contracts": "skill_contract_registry.json",
            "invocation": "invoke_skill(command_envelope, context_slice)",
            "workflow": "WORKFLOW.RUN_RESEARCH_DRY_CHAIN",
            "approval": "Proposal/Human Review",
        },
    }


def export_dayan_ask_packet(
    output_path: str | Path = DEFAULT_DAYAN_ASK_PACKET,
    *,
    workspace_id: str = "ws_personal_z_prime",
) -> dict[str, Any]:
    packet = build_dayan_ask_packet(workspace_id=workspace_id)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return packet


def _safety() -> dict[str, Any]:
    return {
        "paperOnly": True,
        "humanReviewRequired": True,
        "brokerRuntime": "BLOCKED",
        "realTrade": "BLOCKED",
        "productionAllowed": False,
        "agentDirectMutationAllowed": False,
        "registryDirectMutationAllowed": False,
        "memoryDirectWriteAllowed": False,
        "ruleDirectEnableAllowed": False,
        "dataScope": "WORKSPACE_SCOPED",
    }


def _formations() -> list[dict[str, Any]]:
    return [
        {
            "id": "research-chain",
            "name": "研究链路编排阵",
            "description": "计划、证据、报告草案",
            "promptTemplate": "请基于当前研究主题生成只读研究链路，并列出证据缺口。",
            "composedSkillIds": ["workflow-plan", "research-report", "audit-pack"],
            "safetyLevel": "PROPOSAL_REQUIRED",
        },
        {
            "id": "portfolio-review",
            "name": "组合复核阵",
            "description": "暴露模板与风险预算",
            "promptTemplate": "请生成组合复核草案，只输出观察、风险预算和待确认点。",
            "composedSkillIds": ["portfolio-schema", "portfolio-review"],
            "safetyLevel": "PROPOSAL_REQUIRED",
        },
        {
            "id": "history-memory",
            "name": "历史记忆阵",
            "description": "相似案例与记忆候选",
            "promptTemplate": "请检索历史相似案例，并提炼待确认记忆候选。",
            "composedSkillIds": ["similar-cases", "memory-draft"],
            "safetyLevel": "DRAFT_ONLY",
        },
        {
            "id": "audit-guard",
            "name": "审计护法阵",
            "description": "证据链与安全硬门",
            "promptTemplate": "请整理当前链路的审计包，保持只读并等待人工确认。",
            "composedSkillIds": ["audit-pack"],
            "safetyLevel": "READ_ONLY",
        },
        {
            "id": "factor-watch",
            "name": "因子观察阵",
            "description": "纸面观察与衰减复核",
            "promptTemplate": "请复核因子纸面观察项，区分有效、弱化与样本不足。",
            "composedSkillIds": ["factor-snapshot", "similar-cases"],
            "safetyLevel": "DRAFT_ONLY",
        },
        {
            "id": "governance-review",
            "name": "治理复核阵",
            "description": "注册表与硬门检查",
            "promptTemplate": "请检查 SkillOS 注册表与安全硬门，输出复核草案。",
            "composedSkillIds": ["audit-pack", "rule-draft"],
            "safetyLevel": "PROPOSAL_REQUIRED",
        },
    ]


def _skill_categories(registry: list[dict[str, Any]], domain_counts: Counter[str]) -> list[dict[str, Any]]:
    domains = [
        ("portfolio", "持仓问诊", "PORTFOLIO", "组合与账户观察"),
        ("stock-selection", "选股问策", "FACTOR", "因子与候选观察"),
        ("catalyst", "催化问因", "ZC35", "催化与复核草案"),
        ("chain-research", "链上研判", "RESEARCHDB", "研究库与证据材料"),
        ("advisory", "天官问策", "COUNCIL", "专家会审草案"),
        ("history", "历史问迹", "AUTOCASE", "案例与历史检索"),
        ("report", "报告落盘", "REPORT", "报告草案渲染"),
        ("case-replay", "案例复盘", "CASEFORGE", "案例候选草案"),
        ("memory", "记忆沉淀", "MEMORY", "记忆候选草案"),
        ("rule", "规则候选", "GOVERNANCE", "治理与规则复核"),
        ("compass", "罗盘问治", "COCKPIT", "驾驶舱状态草案"),
        ("audit", "审计护法", "SYSTEM_VERIFY", "硬门与审计检查"),
    ]
    return [
        {
            "id": category_id,
            "name": name,
            "description": description,
            "skillCount": domain_counts.get(domain, 0),
            "safetyLevel": _category_safety(registry, domain),
            "skills": [_skill_from_domain(registry, domain, category_id)],
        }
        for category_id, name, domain, description in domains
    ]


def _skill_from_domain(registry: list[dict[str, Any]], domain: str, category_id: str) -> dict[str, Any]:
    item = next((entry for entry in registry if entry.get("domain") == domain), {})
    skill_id = str(item.get("skill_id", f"{domain}.READ_STATUS"))
    risk_level = str(item.get("risk_level", "R0_READ"))
    return {
        "id": category_id.replace("-", "_"),
        "userVisibleName": _visible_name(domain),
        "description": "读取注册能力并生成待确认草案",
        "promptTemplate": "请基于该领域能力生成只读研究草案，并列出人审项。",
        "outputType": "REPORT_DRAFT" if risk_level == "R2_DRAFT" else "CHAT",
        "safetyLevel": "PROPOSAL_REQUIRED" if risk_level == "R2_DRAFT" else "READ_ONLY",
        "requiredInputs": ["研究主题", "证据材料"],
        "backendBinding": {
            "registrySkillIds": [skill_id],
            "domain": domain,
            "operation": "registry_read",
        },
    }


def _visible_name(domain: str) -> str:
    names = {
        "PORTFOLIO": "组合复核草案",
        "FACTOR": "因子观察摘要",
        "ZC35": "催化复核摘要",
        "RESEARCHDB": "研究库检索",
        "COUNCIL": "专家会审草案",
        "AUTOCASE": "相似案例检索",
        "REPORT": "报告草案渲染",
        "CASEFORGE": "案例候选草案",
        "MEMORY": "记忆候选草案",
        "GOVERNANCE": "治理审计草案",
        "COCKPIT": "驾驶舱状态草案",
        "SYSTEM_VERIFY": "硬门检查",
    }
    return names.get(domain, "领域能力草案")


def _category_safety(registry: list[dict[str, Any]], domain: str) -> str:
    risks = {str(item.get("risk_level")) for item in registry if item.get("domain") == domain}
    if "R2_DRAFT" in risks:
        return "PROPOSAL_REQUIRED"
    if "R1_ANNOTATE" in risks:
        return "DRAFT_ONLY"
    return "READ_ONLY"


def _load_registry(path: Path) -> list[dict[str, Any]]:
    data = _load_json(path, [])
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))
