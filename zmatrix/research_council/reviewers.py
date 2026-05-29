# allowlist: forbidden-token-definition
"""V4.0-C3 Research Council — 12 reviewer skills"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ReviewerOutput:
    reviewer_id: str; facts: dict = field(default_factory=dict); evidence_refs: list = field(default_factory=list)
    deterministic_score: float = 0.0; score_trace: dict = field(default_factory=dict)
    risk_flags: list = field(default_factory=list); missing_evidence: list = field(default_factory=list)
    review_status: str = "DATA_INSUFFICIENT"; real_trade_allowed: bool = False; broker_order_allowed: bool = False

class BaseReviewer:
    def __init__(self, reviewer_id, methodology):
        self.reviewer_id = reviewer_id; self.methodology = methodology
        self.fact_fields = []; self.allowed_enums = []; self.required_evidence = []
    def review(self, facts=None):
        facts = facts or {}; missing = [f for f in self.required_evidence if f not in facts]
        if missing: return ReviewerOutput(self.reviewer_id, facts=facts, missing_evidence=missing, review_status="DATA_INSUFFICIENT")
        score = min(100, len(facts)*8); trace = {"reviewer":self.reviewer_id,"input_facts":dict(facts),"method":self.methodology}
        return ReviewerOutput(self.reviewer_id, facts=facts, deterministic_score=score, score_trace=trace, review_status="RESEARCH_SUPPORT")

REVIEWERS = {}
for i, (rid, method) in enumerate([
    ("R01_MACRO_STRATEGIST","Inversion: what macro consensus is wrong?"),
    ("R02_MARGIN_OF_SAFETY","Moslow framework: intrinsic value gap"),
    ("R03_MOAT_OWNER_EARNINGS","Moat durability + owner earnings yield"),
    ("R04_QUALITY_GROWTH","Quality compounder lifecycle stage"),
    ("R05_SHORT_SELLER_FORENSIC","Forensic accounting attack vectors"),
    ("R06_REFLEXIVITY_NARRATIVE","Narrative vs fundamental feedback loops"),
    ("R07_CHAIN_VALUE_CAPTURE","Industry chain value capture positioning"),
    ("R08_MACRO_LIQUIDITY","Macro liquidity cycle alignment"),
    ("R09_FACTOR_VALIDITY","Factor IC decay + regime dependency"),
    ("R10_STRATEGY_OVERFIT","Train/test contamination + lookahead audit"),
    ("R11_EXECUTION_MICRO","Microstructure + fillability + route analysis"),
    ("R12_ACCOUNT_SURVIVAL","Risk budget + drawdown + survival probability"),
], start=1):
    r = BaseReviewer(f"{rid}", method); r.fact_fields = ["source","evidence_level"]; r.required_evidence = ["source"]
    REVIEWERS[rid] = r


def load_independent_reviewers() -> dict:
    """Dynamically load all independent reviewer modules from reviewers/ directory.

    Returns a dict mapping reviewer_id (uppercase) to the module's review function.
    Each function signature is: review(facts: dict | None = None) -> ReviewerOutput.
    """
    import importlib
    import pkgutil
    import zmatrix.research_council.reviewers as pkg

    result = {}
    for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
        if module_name.startswith("r") and len(module_name) >= 5:
            mod = importlib.import_module(f"zmatrix.research_council.reviewers.{module_name}")
            if hasattr(mod, "REVIEWER_CONFIG") and hasattr(mod, "review"):
                rid = mod.REVIEWER_CONFIG.get("reviewer_id", module_name.upper())
                result[rid] = mod.review
    return result
