#!/usr/bin/env python3
"""ResearchDB Phase 0: Promotion Policy Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zmatrix.research_db.promotion_policy import (
    PromotionLevel, case_to_rule_level, can_promote,
)


def test_single_case_lesson_only():
    assert case_to_rule_level(1) == "LESSON_ONLY"


def test_three_cases_rule_candidate():
    assert case_to_rule_level(3) == "RULE_CANDIDATE"


def test_ten_cases_research_rule():
    assert case_to_rule_level(10, cross_ticker=True) == "RESEARCH_RULE"


def test_twenty_cases_paper_rule():
    assert case_to_rule_level(20, cross_ticker=True, cross_regime=True) == "PAPER_RULE"


def test_zero_cases_lesson_only():
    assert case_to_rule_level(0) == "LESSON_ONLY"


def test_can_promote_one_step():
    assert can_promote(PromotionLevel.RAW_DATA, PromotionLevel.FORMAT_VALIDATED) is True


def test_cannot_skip_levels():
    assert can_promote(PromotionLevel.RAW_DATA, PromotionLevel.SOURCE_VALIDATED) is False


def test_cannot_demote():
    assert can_promote(PromotionLevel.FORMAT_VALIDATED, PromotionLevel.RAW_DATA) is False


if __name__ == "__main__":
    test_single_case_lesson_only()
    test_three_cases_rule_candidate()
    test_ten_cases_research_rule()
    test_twenty_cases_paper_rule()
    test_zero_cases_lesson_only()
    test_can_promote_one_step()
    test_cannot_skip_levels()
    test_cannot_demote()
    print("✅ ResearchDB Phase 0 Promotion Policy tests PASS")
