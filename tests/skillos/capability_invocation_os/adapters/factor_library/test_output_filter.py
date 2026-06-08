import pytest
from skillos.capability_invocation_os.adapters.factor_library.output_filter import (
    remove_forbidden_outputs, list_removed_forbidden_outputs,
)

def test_removes_alpha_claim():
    result = remove_forbidden_outputs({"alpha_claim": 0.5, "name": "test"})
    assert "alpha_claim" not in result
    assert result["name"] == "test"

def test_removes_position_weight():
    result = remove_forbidden_outputs({"position_weight": 0.3})
    assert "position_weight" not in result

def test_removes_buy_signal():
    result = remove_forbidden_outputs({"buy_signal": True})
    assert "buy_signal" not in result

def test_lists_removed():
    removed = list_removed_forbidden_outputs({"alpha_claim": 0.5, "safe": 1})
    assert "alpha_claim" in removed
    assert "safe" not in removed

def test_no_input_mutation():
    original = {"alpha_claim": 0.5, "name": "test"}
    remove_forbidden_outputs(original)
    assert "alpha_claim" in original
