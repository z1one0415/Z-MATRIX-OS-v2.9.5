"""V4.0 Hardening-C3: IRF Chain Integration Tests

Tests for IRF-02/05/06/07/08 chain functions plus full-chain safety checks.
"""
import pytest


# ───────────────────────────────────────────────────────────
# Individual chain tests
# ───────────────────────────────────────────────────────────

def test_irf02_chain():
    """Verify irf02_monthly_selection_chain returns correct structure."""
    from zmatrix.irf.irf_chain import irf02_monthly_selection_chain

    result = irf02_monthly_selection_chain()

    # Required keys
    assert "card" in result
    assert "store_size" in result
    assert "r01_review" in result
    assert "r07_review" in result
    assert "report_len" in result
    assert "envelope" in result
    assert "audit" in result
    assert "export_manifest" in result

    # Envelope safety
    envelope = result["envelope"]
    assert envelope["pipeline_id"] == "IRF-02"
    assert envelope["status"] == "INTEGRATION_SMOKE"
    assert envelope["human_review_required"] is True
    assert envelope["real_trade_allowed"] is False
    assert envelope["broker_order_allowed"] is False

    # Audit safety
    audit = result["audit"]
    assert audit["event_id"] == "IRF-02-evt-001"
    assert audit["real_trade_allowed"] is False
    assert audit["safety_gate_passed"] is True

    # Export safety
    assert result["export_manifest"]["manifest"]["real_trade_allowed"] is False

    # Fact store populated
    assert result["store_size"] >= 1

    # Reviews done
    assert result["r01_review"].review_status != ""
    assert result["r07_review"].review_status != ""


def test_irf05_chain():
    """Verify irf05_account_review_chain returns correct structure."""
    from zmatrix.irf.irf_chain import irf05_account_review_chain

    result = irf05_account_review_chain()

    # Required keys
    assert "curve_result" in result
    assert "gate_result" in result
    assert "envelope" in result
    assert "audit" in result
    assert "export_manifest" in result

    # Envelope safety
    envelope = result["envelope"]
    assert envelope["pipeline_id"] == "IRF-05"
    assert envelope["status"] == "INTEGRATION_SMOKE"
    assert envelope["human_review_required"] is True
    assert envelope["real_trade_allowed"] is False

    # Curve safety
    curve = result["curve_result"]
    assert curve["real_trade_allowed"] is False
    assert curve["production_allowed"] is False

    # Gate safety
    gate = result["gate_result"]
    assert gate["action"] == "PAPER_ONLY"
    assert gate["real_trade_allowed"] is False
    assert gate["broker_order_allowed"] is False
    assert gate["human_review_required"] is True

    # Curve computed correctly
    assert curve["start_capital"] == 100000
    assert curve["end_capital"] == 108000


def test_irf06_chain():
    """Verify irf06_portfolio_alpha_chain returns correct structure."""
    from zmatrix.irf.irf_chain import irf06_portfolio_alpha_chain

    result = irf06_portfolio_alpha_chain()

    # Required keys
    assert "horizon_result" in result
    assert "net_return_result" in result
    assert "report_len" in result
    assert "envelope" in result
    assert "audit" in result
    assert "export_manifest" in result

    # Envelope safety
    envelope = result["envelope"]
    assert envelope["pipeline_id"] == "IRF-06"
    assert envelope["status"] == "INTEGRATION_SMOKE"
    assert envelope["human_review_required"] is True
    assert envelope["real_trade_allowed"] is False

    # Horizon integrity
    horizon = result["horizon_result"]
    assert horizon["horizon_ready"] is True
    assert horizon["horizon"] == "T20"
    assert horizon["required_days"] == 20

    # Net return safety
    net = result["net_return_result"]
    assert net["production_allowed"] is False
    assert net["net_return_pct"] < net["gross_return_pct"]  # costs applied

    # Report rendered
    assert result["report_len"] > 0


def test_irf07_chain():
    """Verify irf07_multi_strategy_chain returns correct structure."""
    from zmatrix.irf.irf_chain import irf07_multi_strategy_chain

    result = irf07_multi_strategy_chain()

    # Required keys
    assert "promotion_result" in result
    assert "cost_result" in result
    assert "preview_result" in result
    assert "report_len" in result
    assert "envelope" in result
    assert "audit" in result
    assert "export_manifest" in result

    # Envelope safety
    envelope = result["envelope"]
    assert envelope["pipeline_id"] == "IRF-07"
    assert envelope["status"] == "INTEGRATION_SMOKE"
    assert envelope["human_review_required"] is True
    assert envelope["real_trade_allowed"] is False

    # Promotion gate: production must be blocked
    assert result["promotion_result"]["promotion_allowed"] is False
    assert result["promotion_result"]["production_allowed"] is False
    assert result["promotion_result"]["research_validated"] is True  # with all inputs True

    # Cost model safety
    assert result["cost_result"]["real_trade_allowed"] is False
    assert result["cost_result"]["broker_order_allowed"] is False

    # Paper preview safety
    assert result["preview_result"]["real_trade_allowed"] is False
    assert result["preview_result"]["paper_only"] is True
    assert result["preview_result"]["human_review_required"] is True

    # Report rendered
    assert result["report_len"] > 0


def test_irf08_chain():
    """Verify irf08_factor_data_chain returns correct structure."""
    from zmatrix.irf.irf_chain import irf08_factor_data_chain

    result = irf08_factor_data_chain()

    # Required keys
    assert "quality_result" in result
    assert "horizon_result" in result
    assert "promotion_result" in result
    assert "envelope" in result
    assert "audit" in result
    assert "export_manifest" in result

    # Envelope safety
    envelope = result["envelope"]
    assert envelope["pipeline_id"] == "IRF-08"
    assert envelope["status"] == "INTEGRATION_SMOKE"
    assert envelope["human_review_required"] is True
    assert envelope["real_trade_allowed"] is False

    # Data quality
    quality = result["quality_result"]
    assert quality["final_score"] > 0
    assert quality["usable_for_production"] is False

    # Horizon integrity (t60)
    horizon = result["horizon_result"]
    assert horizon["horizon"] == "T60"
    assert horizon["horizon_ready"] is True
    assert horizon["required_days"] == 60

    # Promotion gate: production blocked
    assert result["promotion_result"]["promotion_allowed"] is False
    assert result["promotion_result"]["production_allowed"] is False


# ───────────────────────────────────────────────────────────
# Cross-chain safety tests
# ───────────────────────────────────────────────────────────

_ALL_CHAIN_FUNCTIONS = []


def _lazy_import_all_chains():
    """Import all 8 chain functions once."""
    global _ALL_CHAIN_FUNCTIONS
    if not _ALL_CHAIN_FUNCTIONS:
        from zmatrix.irf.irf_chain import (
            irf01_full_chain,
            irf02_monthly_selection_chain,
            irf03_factor_chain,
            irf04_execution_chain,
            irf05_account_review_chain,
            irf06_portfolio_alpha_chain,
            irf07_multi_strategy_chain,
            irf08_factor_data_chain,
        )
        _ALL_CHAIN_FUNCTIONS = [
            ("IRF-01", irf01_full_chain),
            ("IRF-02", irf02_monthly_selection_chain),
            ("IRF-03", irf03_factor_chain),
            ("IRF-04", irf04_execution_chain),
            ("IRF-05", irf05_account_review_chain),
            ("IRF-06", irf06_portfolio_alpha_chain),
            ("IRF-07", irf07_multi_strategy_chain),
            ("IRF-08", irf08_factor_data_chain),
        ]
    return _ALL_CHAIN_FUNCTIONS


def test_all_8_chains_no_trade():
    """All 8 chain outputs must enforce real_trade_allowed=False."""
    chains = _lazy_import_all_chains()
    for chain_id, chain_fn in chains:
        try:
            result = chain_fn()
        except Exception as e:
            pytest.fail(f"{chain_id} chain raised: {e}")

        # The envelope must block real trade
        envelope = result.get("envelope", {})
        assert envelope.get("real_trade_allowed") is False, (
            f"{chain_id}: envelope.real_trade_allowed must be False"
        )

        # Audit events must block real trade
        audit = result.get("audit", {})
        assert audit.get("real_trade_allowed") is False, (
            f"{chain_id}: audit.real_trade_allowed must be False"
        )

        # Export manifest must block real trade
        export = result.get("export_manifest", {})
        if isinstance(export, dict) and "manifest" in export:
            assert export["manifest"].get("real_trade_allowed") is False, (
                f"{chain_id}: export_manifest.real_trade_allowed must be False"
            )

        # No returned dict value should directly allow real trade
        _assert_no_nested_real_trade(result, chain_id)


def _assert_no_nested_real_trade(data, chain_id, path=""):
    """Recursively check no nested structure has real_trade_allowed=True."""
    if isinstance(data, dict):
        for key, val in data.items():
            if key == "real_trade_allowed" and val is True:
                nested_path = f"{path}.{key}" if path else key
                raise AssertionError(
                    f"{chain_id}: found real_trade_allowed=True at {nested_path}"
                )
            if isinstance(val, (dict, list)):
                _assert_no_nested_real_trade(val, chain_id, f"{path}.{key}" if path else key)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            _assert_no_nested_real_trade(item, chain_id, f"{path}[{i}]")


def test_all_8_chains_human_review():
    """All 8 chain outputs must enforce human_review_required=True."""
    chains = _lazy_import_all_chains()
    for chain_id, chain_fn in chains:
        result = chain_fn()

        envelope = result.get("envelope", {})
        assert envelope.get("human_review_required") is True, (
            f"{chain_id}: envelope.human_review_required must be True"
        )


def test_chain_coverage():
    """Verify irf_chain.py defines 8 functions whose names start with 'irf'."""
    from zmatrix.irf import irf_chain

    irf_functions = [
        name
        for name in dir(irf_chain)
        if name.startswith("irf") and callable(getattr(irf_chain, name))
    ]
    assert len(irf_functions) == 8, (
        f"Expected 8 irf* functions in irf_chain.py, found {len(irf_functions)}: {irf_functions}"
    )


def test_init_exports_all_8():
    """Verify __init__.py exports all 8 chain functions."""
    from zmatrix.irf import __all__ as irf_all

    exported = [name for name in irf_all if name.startswith("irf") and "chain" in name]
    assert len(exported) == 8, (
        f"Expected 8 irf*_chain exports in __init__.py, found {len(exported)}: {exported}"
    )


def test_broker_order_blocked_all_chains():
    """All 8 chains: broker_order_allowed=False in envelope."""
    chains = _lazy_import_all_chains()
    for chain_id, chain_fn in chains:
        result = chain_fn()
        envelope = result.get("envelope", {})
        assert envelope.get("broker_order_allowed") is False, (
            f"{chain_id}: broker_order_allowed must be False"
        )


def test_production_blocked_all_chains():
    """All 8 chains: production_allowed=False in all nested outputs."""
    chains = _lazy_import_all_chains()
    for chain_id, chain_fn in chains:
        result = chain_fn()
        _assert_no_nested_production(result, chain_id)


def _assert_no_nested_production(data, chain_id, path=""):
    """Check no nested structure has production_allowed=True."""
    if isinstance(data, dict):
        for key, val in data.items():
            if key == "production_allowed" and val is True:
                nested_path = f"{path}.{key}" if path else key
                raise AssertionError(
                    f"{chain_id}: found production_allowed=True at {nested_path}"
                )
            if isinstance(val, (dict, list)):
                _assert_no_nested_production(val, chain_id, f"{path}.{key}" if path else key)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            _assert_no_nested_production(item, chain_id, f"{path}[{i}]")


def test_human_review_required_all_outputs():
    """Any human_review_required field in outputs must be True."""
    chains = _lazy_import_all_chains()
    for chain_id, chain_fn in chains:
        result = chain_fn()
        _assert_human_review_true(result, chain_id)


def _assert_human_review_true(data, chain_id, path=""):
    """Check human_review_required is never False in nested outputs."""
    if isinstance(data, dict):
        for key, val in data.items():
            if key == "human_review_required" and val is False:
                nested_path = f"{path}.{key}" if path else key
                raise AssertionError(
                    f"{chain_id}: found human_review_required=False at {nested_path}"
                )
            if isinstance(val, (dict, list)):
                _assert_human_review_true(val, chain_id, f"{path}.{key}" if path else key)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            _assert_human_review_true(item, chain_id, f"{path}[{i}]")
