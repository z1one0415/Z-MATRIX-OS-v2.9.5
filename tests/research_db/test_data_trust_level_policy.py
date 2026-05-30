#!/usr/bin/env python3
"""ResearchDB Phase 0: Data Trust Level Policy Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zmatrix.research_db.trust_level import DataTrustLevel, can_enter_factor_validation, can_enter_research_report, can_enter_promotion


def test_all_levels_defined():
    levels = [DataTrustLevel.T0_RAW_IMPORT, DataTrustLevel.T1_FORMAT_VALIDATED,
              DataTrustLevel.T2_SOURCE_VALIDATED, DataTrustLevel.T3_CROSS_SOURCE_VALIDATED,
              DataTrustLevel.T4_OUTCOME_VALIDATED, DataTrustLevel.T5_RESEARCH_ACCEPTED]
    assert len(levels) == 6


def test_t0_t1_blocked_from_factor_validation():
    assert can_enter_factor_validation(DataTrustLevel.T0_RAW_IMPORT) is False
    assert can_enter_factor_validation(DataTrustLevel.T1_FORMAT_VALIDATED) is False


def test_t4_t5_allowed_factor_validation():
    assert can_enter_factor_validation(DataTrustLevel.T4_OUTCOME_VALIDATED) is True
    assert can_enter_factor_validation(DataTrustLevel.T5_RESEARCH_ACCEPTED) is True


def test_t2_allowed_research_report():
    assert can_enter_research_report(DataTrustLevel.T2_SOURCE_VALIDATED) is True
    assert can_enter_research_report(DataTrustLevel.T0_RAW_IMPORT) is False


def test_t0_blocked_promotion():
    assert can_enter_promotion(DataTrustLevel.T0_RAW_IMPORT) is False
    assert can_enter_promotion(DataTrustLevel.T5_RESEARCH_ACCEPTED) is True


if __name__ == "__main__":
    test_all_levels_defined()
    test_t0_t1_blocked_from_factor_validation()
    test_t4_t5_allowed_factor_validation()
    test_t2_allowed_research_report()
    test_t0_blocked_promotion()
    print("✅ ResearchDB Phase 0 Trust Level Policy tests PASS")
