# allowlist: forbidden-token-definition
"""Tests for expert_domain_contract — create, validate, aggregate"""
from __future__ import annotations

from zmatrix.agent.expert_domain_contract import (
    create_review_output,
    validate_review_output,
    aggregate_review_results,
)


class TestCreateReviewOutput:
    def test_create_review_output_returns_valid_dict(self):
        result = create_review_output(
            reviewer_id="REVIEWER.DATA_QUALITY",
            target_ref="case-1",
            verdict="PASS",
            confidence=0.95,
            reason_short="Data quality checks passed",
        )
        assert isinstance(result, dict)
        assert result["reviewer_id"] == "REVIEWER.DATA_QUALITY"
        assert result["target_ref"] == "case-1"
        assert result["verdict"] == "PASS"
        assert result["confidence"] == 0.95
        assert result["reason_short"] == "Data quality checks passed"
        assert result["production_allowed"] is False


class TestValidateReviewOutput:
    def test_valid_output_passes(self):
        output = create_review_output(
            reviewer_id="REVIEWER.DATA_QUALITY",
            target_ref="case-1",
            verdict="PASS",
            confidence=0.95,
            reason_short="All checks passed",
        )
        result = validate_review_output(output)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_output_with_buy_token_returns_error(self):
        output = create_review_output(
            reviewer_id="REVIEWER.DATA_QUALITY",
            target_ref="case-1",
            verdict="PASS",
            confidence=0.95,
            reason_short="Recommend BUY action",
        )
        result = validate_review_output(output)
        assert result["valid"] is False
        assert any("forbidden token" in e.lower() for e in result["errors"])

    def test_confidence_out_of_range_returns_error(self):
        output = create_review_output(
            reviewer_id="REVIEWER.DATA_QUALITY",
            target_ref="case-1",
            verdict="PASS",
            confidence=1.5,
            reason_short="Overconfident",
        )
        result = validate_review_output(output)
        assert result["valid"] is False
        assert any("confidence" in e for e in result["errors"])

    def test_confidence_below_zero_returns_error(self):
        output = create_review_output(
            reviewer_id="REVIEWER.DATA_QUALITY",
            target_ref="case-1",
            verdict="PASS",
            confidence=-0.1,
            reason_short="Negative confidence",
        )
        result = validate_review_output(output)
        assert result["valid"] is False
        assert any("confidence" in e for e in result["errors"])

    def test_invalid_verdict_returns_error(self):
        output = {
            "reviewer_id": "REVIEWER.DATA_QUALITY",
            "target_ref": "case-1",
            "verdict": "INVALID_VERDICT",
            "confidence": 0.8,
            "reason_short": "Bad verdict",
            "production_allowed": False,
        }
        result = validate_review_output(output)
        assert result["valid"] is False
        assert any("verdict" in e for e in result["errors"])


class TestAggregateReviewResults:
    def test_aggregate_review_results_computes_consensus(self):
        outputs = [
            create_review_output("R1", "case-1", "PASS", 0.9, "ok"),
            create_review_output("R2", "case-1", "PASS", 0.85, "ok"),
            create_review_output("R3", "case-1", "WATCH", 0.6, "caution"),
        ]
        result = aggregate_review_results(outputs)
        assert result["consensus_verdict"] == "PASS"
        assert result["pass_count"] == 2
        assert result["block_count"] == 0

    def test_aggregate_with_blocks_computes_consensus(self):
        outputs = [
            create_review_output("R1", "case-1", "BLOCK", 0.9, "danger"),
            create_review_output("R2", "case-1", "BLOCK", 0.85, "danger"),
            create_review_output("R3", "case-1", "PASS", 0.6, "ok"),
        ]
        result = aggregate_review_results(outputs)
        assert result["consensus_verdict"] == "BLOCK"
        assert result["pass_count"] == 1
        assert result["block_count"] == 2

    def test_aggregate_with_conflicts(self):
        outputs = [
            create_review_output("R1", "case-1", "PASS", 0.9, "ok"),
            create_review_output("R2", "case-1", "BLOCK", 0.85, "danger"),
        ]
        result = aggregate_review_results(outputs)
        assert result["consensus_verdict"] in ("PASS", "BLOCK", "CONFLICTED")
        assert result["pass_count"] == 1
        assert result["block_count"] == 1
        assert len(result["conflicts"]) == 1

    def test_aggregate_empty_returns_data_insufficient(self):
        result = aggregate_review_results([])
        assert result["consensus_verdict"] == "DATA_INSUFFICIENT"
        assert result["pass_count"] == 0
        assert result["block_count"] == 0
        assert result["conflicts"] == []

    def test_output_has_production_allowed_false(self):
        output = create_review_output(
            reviewer_id="REVIEWER.DATA_QUALITY",
            target_ref="case-1",
            verdict="PASS",
            confidence=0.95,
            reason_short="ok",
        )
        assert output["production_allowed"] is False
