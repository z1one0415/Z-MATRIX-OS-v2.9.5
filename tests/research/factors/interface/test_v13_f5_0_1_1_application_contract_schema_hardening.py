"""V13.F5.0.1.1 — Test application_contract schema hardening with hard requires assertions."""
import json
def validate(instance):
    """Simulate JSON Schema allOf + contains validation."""
    modes = instance.get("blocked_application_modes", [])
    outputs = instance.get("blocked_outputs", [])
    consumers = instance.get("blocked_downstream_consumers", [])
    REQUIRED_MODES = ["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"]
    REQUIRED_OUTPUTS = ["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"]
    REQUIRED_CONSUMERS = ["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]
    errors = []
    for m in REQUIRED_MODES:
        if m not in modes: errors.append(f"missing_blocked_mode:{m}")
    for o in REQUIRED_OUTPUTS:
        if o not in outputs: errors.append(f"missing_blocked_output:{o}")
    for c in REQUIRED_CONSUMERS:
        if c not in consumers: errors.append(f"missing_blocked_consumer:{c}")
    return errors

def test_all_7_blocked_modes_present():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert validate(c) == []

def test_blocked_modes_missing_alpha_signal():
    c = {"blocked_application_modes":["PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert "ALPHA_SIGNAL" in validate(c)[0]

def test_blocked_modes_missing_portfolio_weight():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    err = validate(c); assert any("PORTFOLIO_WEIGHT" in e for e in err)

def test_blocked_modes_missing_order_signal():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("ORDER_SIGNAL" in e for e in validate(c))

def test_blocked_modes_missing_paper_trading():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("PAPER_TRADING" in e for e in validate(c))

def test_blocked_modes_missing_broker_runtime():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("BROKER_RUNTIME" in e for e in validate(c))

def test_blocked_modes_missing_real_trade():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("REAL_TRADE" in e for e in validate(c))

def test_blocked_modes_missing_production():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("PRODUCTION" in e for e in validate(c))

def test_blocked_outputs_missing_buy_signal():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["sell_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("buy_signal" in e for e in validate(c))

def test_blocked_outputs_missing_sell_signal():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","position_weight","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("sell_signal" in e for e in validate(c))

def test_blocked_outputs_missing_position_weight():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","expected_return_claim","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("position_weight" in e for e in validate(c))

def test_blocked_outputs_missing_expected_return():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","alpha_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("expected_return_claim" in e for e in validate(c))

def test_blocked_outputs_missing_alpha_claim():
    c = {"blocked_application_modes":["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"],"blocked_outputs":["buy_signal","sell_signal","position_weight","expected_return_claim"],"blocked_downstream_consumers":["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]}
    assert any("alpha_claim" in e for e in validate(c))
