"""Tests for Z9 attribution."""
from skillos.capability_invocation_os.review_node.attribution import build_explanation_attribution

def test_explanation_attribution_returns_dict():
    result = build_explanation_attribution(None, None)
    assert isinstance(result, dict)

def test_attribution_readonly():
    result = build_explanation_attribution(None, None)
    assert result.get("readonly_only", False) is True

def test_attribution_explanation_type():
    result = build_explanation_attribution(None, None)
    assert "attribution_type" in result
