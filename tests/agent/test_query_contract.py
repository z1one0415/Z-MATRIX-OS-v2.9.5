# allowlist: forbidden-token-definition
"""Tests for query_contract — all query functions"""
from __future__ import annotations

from zmatrix.agent.query_contract import (
    get_research_summary,
    get_layer_versions,
    get_changed_layers,
    get_layer_slice,
    query_case,
    query_event_window,
    query_factor,
    query_hypotheses,
)


class TestGetResearchSummary:
    def test_get_research_summary_returns_dict_with_system_version(self):
        result = get_research_summary()
        assert isinstance(result, dict)
        assert "system_version" in result
        assert result["system_version"] == "0.5.0-stub"
        assert "token_estimate" in result
        assert result["token_estimate"] > 0


class TestGetLayerVersions:
    def test_get_layer_versions_returns_dict(self):
        result = get_layer_versions()
        assert isinstance(result, dict)
        assert "research_summary" in result
        assert "token_estimate" in result


class TestLayerSlice:
    def test_get_layer_slice_respects_limit(self):
        result = get_layer_slice(["research_summary", "case_data", "tests"], limit=2)
        assert "layers" in result
        assert len(result["layers"]) == 2
        assert "token_estimate" in result

    def test_get_layer_slice_with_limit_0_returns_need_narrower_query(self):
        result = get_layer_slice(["research_summary"], limit=0)
        assert "error" in result
        assert result["error"] is True
        assert result["code"] == "NEED_NARROWER_QUERY"

    def test_get_layer_slice_with_limit_over_1000_returns_error(self):
        result = get_layer_slice(["research_summary"], limit=1001)
        assert "error" in result
        assert result["error"] is True
        assert result["code"] == "NEED_NARROWER_QUERY"


class TestResultContainsTokenEstimate:
    def test_query_result_contains_token_estimate_field(self):
        results = [
            query_case("case-1"),
            query_event_window("target-1", "2026-01-01", "2026-01-02"),
            query_factor("factor-1"),
            query_hypotheses({"status": "active"}),
        ]
        for r in results:
            assert "token_estimate" in r, f"Missing token_estimate in {r}"
            assert isinstance(r["token_estimate"], int)
            assert r["token_estimate"] > 0


class TestGetLayerVersions2:
    def test_get_layer_versions_returns_dict(self):
        result = get_layer_versions()
        assert isinstance(result, dict)
        assert "layer_versions" in result or "research_summary" in result


class TestGetChangedLayers:
    def test_get_changed_layers_returns_changes(self):
        result = get_changed_layers({"research_summary": "sha256:old"})
        assert "changes" in result
        assert "research_summary" in result["changes"]
        assert result["changes"]["research_summary"]["changed"] is True
        assert "token_estimate" in result
