import pytest
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeEvidence,
    A1FactorBridgeContext,
    A1FactorBridgeRequest,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import (
    FORBIDDEN_BRIDGE_OUTPUTS,
)


def test_model_defaults_safe():
    resp = A1FactorBridgeResponse()
    assert resp.bridge_enabled is False
    assert resp.runtime_enabled is False
    assert resp.adapter_execution_enabled is False
    assert resp.capability_execution_enabled is False
    assert resp.degraded is True
    assert resp.mode == "DISABLED_DEFAULT_P0"
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"


def test_no_real_source_flag_defaults_true():
    evidence = A1FactorBridgeEvidence()
    assert evidence.no_real_source_flag is True
    ctx = A1FactorBridgeContext()
    assert ctx.no_real_source_flag is True


def test_forbidden_outputs_removed_includes_all():
    resp = A1FactorBridgeResponse()
    removed = set(resp.forbidden_outputs_removed)
    assert FORBIDDEN_BRIDGE_OUTPUTS == removed


def test_runtime_adapter_capability_flags_all_default_false():
    resp = A1FactorBridgeResponse()
    assert resp.runtime_enabled is False
    assert resp.adapter_execution_enabled is False
    assert resp.capability_execution_enabled is False


def test_no_alpha_trade_weight_fields_on_any_model():
    """Scan all model class fields for forbidden trading fields."""
    from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge import models
    forbidden_fields = {
        "alpha_claim", "expected_return_claim", "position_weight",
        "buy_signal", "sell_signal", "order_signal",
        "broker_runtime", "real_trade", "production",
    }
    import dataclasses
    import inspect
    for name, obj in inspect.getmembers(models):
        if not inspect.isclass(obj):
            continue
        if not hasattr(obj, "__dataclass_fields__"):
            continue
        fields = set(obj.__dataclass_fields__.keys())
        overlap = fields & forbidden_fields
        assert not overlap, f"Model {name} contains forbidden fields: {overlap}"
