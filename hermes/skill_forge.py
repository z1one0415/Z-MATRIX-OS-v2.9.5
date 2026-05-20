"""
Z2天师 Hermes — 研究技能熔炉
研究模板的创建/沉淀/进化。
"""
from __future__ import annotations

from typing import Any
from contracts.research_contracts import ResearchSkillCandidate


class ResearchSkillForge:
    """研究技能沉淀工坊"""

    def __init__(self):
        self._templates: dict[str, dict[str, Any]] = {
            "target_deep": {
                "steps": [
                    "industry_position", "fundamental_quality",
                    "business_model", "technology_ecosystem",
                    "valuation_scenario", "risk_factors"
                ],
                "min_evidence_sources": 3,
            },
            "industry_chain": {
                "steps": [
                    "chain_positioning", "upstream_dynamics",
                    "downstream_demand", "competitive_landscape",
                    "policy_environment", "cross_chain_correlation"
                ],
                "min_evidence_sources": 2,
            },
            "event_scenario": {
                "steps": [
                    "event_nature", "transmission_chain",
                    "scenario_bull", "scenario_base", "scenario_bear",
                    "probability_assignment"
                ],
                "min_evidence_sources": 2,
            },
        }

    def get_template(self, task_type: str) -> dict[str, Any] | None:
        return self._templates.get(task_type)

    def propose_skill(self, candidate: ResearchSkillCandidate) -> bool:
        """提交技能候选 (不会自动注册, 需要审批)"""
        if not candidate.approval_required:
            return False
        return True  # pending approval

    def register_skill(self, skill_name: str, steps: list[str], trigger: str) -> None:
        """注册已审批的技能 (由 Z9 调用)"""
        self._templates[skill_name] = {
            "steps": steps,
            "trigger": trigger,
            "approved": True,
        }

    def evolve_template(self, task_type: str, new_step: str) -> bool:
        """向现有模板追加步骤"""
        tmpl = self._templates.get(task_type)
        if tmpl and new_step not in tmpl["steps"]:
            tmpl["steps"].append(new_step)
            return True
        return False

    def list_templates(self) -> list[str]:
        return list(self._templates.keys())


_forge: ResearchSkillForge | None = None


def get_skill_forge() -> ResearchSkillForge:
    global _forge
    if _forge is None:
        _forge = ResearchSkillForge()
    return _forge
