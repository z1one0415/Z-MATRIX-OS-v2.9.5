"""V4.0 Hardening-C3 Reviewer Test Suite

Tests all 12 independent reviewers:
- File existence
- Importability
- Deterministic scoring
- No real trade / broker order
- Missing evidence handling
- Loader correctness
- Output format consistency with BaseReviewer
"""
from __future__ import annotations
import sys
import os
import importlib
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("Z_MATRIX_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.research_council.reviewers import ReviewerOutput, BaseReviewer, REVIEWERS, load_independent_reviewers


# ── Expected reviewer IDs ──────────────────────────────────────────────
EXPECTED_IDS = [
    "R01_MACRO_STRATEGIST",
    "R02_MARGIN_OF_SAFETY",
    "R03_MOAT_OWNER_EARNINGS",
    "R04_QUALITY_GROWTH",
    "R05_SHORT_SELLER_FORENSIC",
    "R06_REFLEXIVITY_NARRATIVE",
    "R07_CHAIN_VALUE_CAPTURE",
    "R08_MACRO_LIQUIDITY",
    "R09_FACTOR_VALIDITY",
    "R10_STRATEGY_OVERFIT",
    "R11_EXECUTION_MICRO",
    "R12_ACCOUNT_SURVIVAL",
]

REVIEWERS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "zmatrix", "research_council", "reviewers"
)

# ── Complete facts for each reviewer (satisfying all required_evidence) ──
COMPLETE_FACTS = {
    "R01_MACRO_STRATEGIST": {
        "source": "test", "macro_cycle_phase": "late_cycle",
        "consensus_view": "soft_landing", "extra1": "bonus", "extra2": "bonus2",
    },
    "R02_MARGIN_OF_SAFETY": {
        "source": "test", "intrinsic_value_est": 100,
        "market_price": 60, "mos_pct": 40,
    },
    "R03_MOAT_OWNER_EARNINGS": {
        "source": "test", "moat_type": "network_effects",
        "moat_durability_years": 15, "owner_earnings_yield": 10,
    },
    "R04_QUALITY_GROWTH": {
        "source": "test", "lifecycle_stage": "growth",
        "roe_5yr_avg": 25, "reinvestment_rate": 0.6,
    },
    "R05_SHORT_SELLER_FORENSIC": {
        "source": "test", "receivables_quality": "clean",
        "cashflow_match": "clean", "related_party_check": "clean",
    },
    "R06_REFLEXIVITY_NARRATIVE": {
        "source": "test", "narrative_strength": "high",
        "fundamental_trend": "improving", "sentiment_divergence": "aligned",
    },
    "R07_CHAIN_VALUE_CAPTURE": {
        "source": "test", "chain_position": "core_tech",
        "value_add_pct": 50, "pricing_power": "high",
    },
    "R08_MACRO_LIQUIDITY": {
        "source": "test", "liquidity_cycle_phase": "expansion",
        "credit_spread": 1.2, "capital_flow_direction": "inflow",
    },
    "R09_FACTOR_VALIDITY": {
        "source": "test", "factor_ic_recent": 0.07,
        "factor_ic_decay_rate": "low", "regime_alignment": True,
    },
    "R10_STRATEGY_OVERFIT": {
        "source": "test", "train_test_split_ratio": 0.7,
        "contamination_score": "clean", "lookahead_bias_check": "pass",
    },
    "R11_EXECUTION_MICRO": {
        "source": "test", "avg_daily_volume": 5_000_000,
        "bid_ask_spread_bps": 3, "fill_probability": 0.98,
    },
    "R12_ACCOUNT_SURVIVAL": {
        "source": "test", "risk_budget_remaining_pct": 80,
        "max_drawdown_pct": 5, "survival_probability": 0.97,
    },
}


# ── Tests ───────────────────────────────────────────────────────────────

def test_12_reviewer_files_exist():
    """Verify all 12 independent reviewer .py files exist in reviewers/."""
    for rid in EXPECTED_IDS:
        # r01_macro_strategist.py etc.
        num = rid[1:3]
        rest = rid[4:].lower()
        fname = f"r{num}_{rest}.py"
        path = os.path.join(REVIEWERS_DIR, fname)
        assert os.path.isfile(path), f"Missing: {path}"
    assert len(os.listdir(REVIEWERS_DIR)) >= 14  # 12 + __init__ + __pycache__ possibly
    print("✅ test_12_reviewer_files_exist PASSED")


def test_each_reviewer_imports():
    """Each reviewer module can be imported and has review() and REVIEWER_CONFIG."""
    for rid in EXPECTED_IDS:
        num = rid[1:3]
        rest = rid[4:].lower()
        mod_name = f"zmatrix.research_council.reviewers.r{num}_{rest}"
        mod = importlib.import_module(mod_name)
        assert hasattr(mod, "REVIEWER_CONFIG"), f"{mod_name} missing REVIEWER_CONFIG"
        assert hasattr(mod, "review"), f"{mod_name} missing review()"
        assert callable(mod.review), f"{mod_name}.review is not callable"
        assert mod.REVIEWER_CONFIG["reviewer_id"] == rid, \
            f"{mod_name} config: expected {rid}, got {mod.REVIEWER_CONFIG['reviewer_id']}"
    print("✅ test_each_reviewer_imports PASSED")


def test_each_reviewer_scoring():
    """Each reviewer returns a positive score with complete facts."""
    for rid in EXPECTED_IDS:
        num = rid[1:3]
        rest = rid[4:].lower()
        mod_name = f"zmatrix.research_council.reviewers.r{num}_{rest}"
        mod = importlib.import_module(mod_name)
        facts = COMPLETE_FACTS[rid]
        result = mod.review(facts)
        assert isinstance(result, ReviewerOutput), f"{rid}: expected ReviewerOutput, got {type(result)}"
        assert result.review_status == "RESEARCH_SUPPORT", \
            f"{rid}: expected RESEARCH_SUPPORT, got {result.review_status}"
        assert result.deterministic_score > 0, \
            f"{rid}: score should be > 0, got {result.deterministic_score}"
    print("✅ test_each_reviewer_scoring PASSED")


def test_each_reviewer_no_trade():
    """All reviewers must have real_trade_allowed=False, broker_order_allowed=False."""
    for rid in EXPECTED_IDS:
        num = rid[1:3]
        rest = rid[4:].lower()
        mod_name = f"zmatrix.research_council.reviewers.r{num}_{rest}"
        mod = importlib.import_module(mod_name)
        facts = COMPLETE_FACTS[rid]
        result = mod.review(facts)
        assert result.real_trade_allowed is False, f"{rid}: real_trade_allowed should be False"
        assert result.broker_order_allowed is False, f"{rid}: broker_order_allowed should be False"
        # Also check DATA_INSUFFICIENT case
        empty_result = mod.review({})
        assert empty_result.real_trade_allowed is False, f"{rid} (empty): real_trade_allowed should be False"
        assert empty_result.broker_order_allowed is False, f"{rid} (empty): broker_order_allowed should be False"
    print("✅ test_each_reviewer_no_trade PASSED")


def test_missing_evidence_per_reviewer():
    """Each reviewer returns DATA_INSUFFICIENT when required evidence is missing."""
    for rid in EXPECTED_IDS:
        num = rid[1:3]
        rest = rid[4:].lower()
        mod_name = f"zmatrix.research_council.reviewers.r{num}_{rest}"
        mod = importlib.import_module(mod_name)
        # Provide only "source" — should miss the rest
        partial = {"source": "test"}
        result = mod.review(partial)
        assert result.review_status == "DATA_INSUFFICIENT", \
            f"{rid}: partial facts should be DATA_INSUFFICIENT, got {result.review_status}"
        assert len(result.missing_evidence) > 0, \
            f"{rid}: should have missing_evidence"
        # Empty facts should also be DATA_INSUFFICIENT
        empty_result = mod.review({})
        assert empty_result.review_status == "DATA_INSUFFICIENT", \
            f"{rid}: empty facts should be DATA_INSUFFICIENT"
    print("✅ test_missing_evidence_per_reviewer PASSED")


def test_independent_loader():
    """load_independent_reviewers() returns 12 review functions."""
    independent = load_independent_reviewers()
    assert len(independent) == 12, f"Expected 12, got {len(independent)}"
    for rid in EXPECTED_IDS:
        assert rid in independent, f"Missing {rid} from loader"
        assert callable(independent[rid]), f"{rid} review is not callable"
    print("✅ test_independent_loader PASSED")


def test_all_independent_reviewers_consistent():
    """All independent reviewers produce output compatible with BaseReviewer format."""
    # Base reviewer reference
    base = BaseReviewer("TEST", "test_method")
    base.required_evidence = ["source"]
    base_out = base.review({"source": "test"})

    for rid in EXPECTED_IDS:
        num = rid[1:3]
        rest = rid[4:].lower()
        mod_name = f"zmatrix.research_council.reviewers.r{num}_{rest}"
        mod = importlib.import_module(mod_name)
        result = mod.review(COMPLETE_FACTS[rid])

        # Same field types
        assert isinstance(result.reviewer_id, str)
        assert isinstance(result.facts, dict)
        assert isinstance(result.evidence_refs, list)
        assert isinstance(result.deterministic_score, float)
        assert isinstance(result.score_trace, dict)
        assert isinstance(result.risk_flags, list)
        assert isinstance(result.missing_evidence, list)
        assert isinstance(result.review_status, str)
        assert isinstance(result.real_trade_allowed, bool)
        assert isinstance(result.broker_order_allowed, bool)

        # score_trace should contain methodology info
        assert "reviewer" in result.score_trace
        assert "method" in result.score_trace
        assert "calculation" in result.score_trace

        # facts dict preserved
        assert result.facts == COMPLETE_FACTS[rid]

    print("✅ test_all_independent_reviewers_consistent PASSED")


# ── Score trace details (extra coverage) ────────────────────────────────

def test_score_traces_are_deterministic():
    """Running the same facts twice produces identical scores."""
    for rid in EXPECTED_IDS:
        num = rid[1:3]
        rest = rid[4:].lower()
        mod_name = f"zmatrix.research_council.reviewers.r{num}_{rest}"
        mod = importlib.import_module(mod_name)
        facts = COMPLETE_FACTS[rid]
        r1 = mod.review(facts)
        r2 = mod.review(facts)
        assert r1.deterministic_score == r2.deterministic_score, \
            f"{rid}: non-deterministic! {r1.deterministic_score} != {r2.deterministic_score}"
        assert r1.score_trace == r2.score_trace, f"{rid}: score_trace differs"
    print("✅ test_score_traces_are_deterministic PASSED")


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_12_reviewer_files_exist()
    test_each_reviewer_imports()
    test_each_reviewer_scoring()
    test_each_reviewer_no_trade()
    test_missing_evidence_per_reviewer()
    test_independent_loader()
    test_all_independent_reviewers_consistent()
    test_score_traces_are_deterministic()
    print("\n🏁 Hardening-C3: All 12 reviewers — tests PASS")
