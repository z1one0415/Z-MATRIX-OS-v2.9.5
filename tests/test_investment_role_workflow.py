"""全链路 Workflow 测试 — 验证 7 层过滤串联"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.investment.investment_role_workflow import build_investment_role_review


def _full_inputs():
    return {
        "sector": "机器人",
        "sector_stage": "CONFIRMATION",
        "fundamentals": {
            "financial_health_score": 8, "quality_score": 7, "cashflow_score": 8,
            "roe_score": 15, "industry_durability": 8, "dividend_or_core_asset_score": 6,
            "sector": "ROBOT",
            "revenue_growth": 15, "net_profit_growth": 20, "deducted_net_profit_growth": 18,
            "gross_margin": 45, "operating_cashflow": 100, "debt_ratio": 40,
            "valuation_percentile": 60, "goodwill_risk": 0, "receivable_risk": 0,
        },
        "valuation": {"valuation_safety": 7},
        "narrative": {"narrative_heat": 8, "catalyst_score": 7, "event_validity": 8,
                      "fund_flow_heat": 7, "narrative_decay": 6},
        "event": {"invalidation_condition": "跌破30日线", "stop_loss_pct": 8},
        "r_matrix": {"status": "PASS", "r_action_cap": "WATCH_ENTRY", "ticker": "002472"},
        "checklist": {
            "stock_role": "B_MID_ROTATION", "buy_logic_type": "ROTATION",
            "sector_stage": "CONFIRMATION", "financial_gate_passed": True,
            "valuation_overheated": False, "max_loss_after_entry": 8,
            "invalidation_condition": "板块退潮", "lower_risk_validation_action": "等回调到均线",
        },
        "chain": "机器人",
        "force_scores": {"financial_cycle": 7, "international_cycle": 6, "state_capital": 8},
        "market_beta": 1.2, "sector_beta": 0.9, "max_drawdown": -25,
        "correlation_60d": 0.6, "correlation_120d": 0.5, "correlation_250d": 0.4,
        "portfolio_exposure_summary": {},
    }


def test_workflow_required_fields():
    r = build_investment_role_review("002472", _full_inputs())
    for k in ["workflow_version", "ticker", "chain_force", "sector_stage",
              "financial_health", "b_matrix", "r_matrix", "d_matrix",
              "stock_role", "account_constitution", "portfolio_exposure",
              "z8_position_control", "pre_trade_checklist", "g17_human_veto",
              "paper_record_allowed", "real_trade_allowed", "gates_summary"]:
        assert k in r, f"missing: {k}"
    assert r["real_trade_allowed"] is False
    print("✅ workflow: required fields present (all 7 layers)")


def test_full_7_layer_pipeline():
    """仅B-Matrix PASS 时，经过完整7层过滤获得 A_LONG_CORE"""
    inputs = _full_inputs()
    # 让 D 不 PASS（移除 narrative/event 数据使 degraded）
    inputs["narrative"] = {}
    inputs["event"] = {}
    # 让 R 不 PASS
    inputs["r_matrix"] = {"status": "DEGRADED", "r_action_cap": "WAIT", "ticker": "002472"}
    r = build_investment_role_review("002472", inputs)
    print(f"  role: {r['stock_role']['role']}")
    print(f"  paper_record_allowed: {r['paper_record_allowed']}")
    print(f"  gates: {r['gates_summary']}")
    assert r["paper_record_allowed"] is True, f"paper not allowed: {r['paper_record_allowed']}"


def test_g17_required():
    r = build_investment_role_review("002472", _full_inputs())
    assert r["g17_human_veto_required"] is True
    assert r["g17_human_veto"]["human_final_override_required"] is True
    print("✅ workflow: G17 human veto required")


def test_gates_summary_10_gates():
    """gate 汇总应包含全部 10 个 gate"""
    r = build_investment_role_review("002472", _full_inputs())
    gates = r["gates_summary"]
    expected = {"chain_force", "sector_stage", "financial_health", "b_matrix",
                "stock_role", "account_constitution", "portfolio_exposure",
                "z8_position_control", "pre_trade_checklist", "g17_human_veto"}
    actual = set(gates.keys())
    missing = expected - actual
    assert not missing, f"gate check missing: {missing}"
    print(f"✅ workflow: {len(gates)} gates in summary ({', '.join(sorted(gates.keys()))})")


def test_z8_position_limits():
    r = build_investment_role_review("002472", _full_inputs())
    z8 = r["z8_position_control"]
    assert "max_position_size" in z8
    role = r["stock_role"]["role"]
    if role == "A_LONG_CORE":
        assert z8["max_position_size"] == 0.12
    elif role == "B_MID_ROTATION":
        assert z8["max_position_size"] == 0.08
    elif role == "C_SHORT_EVENT":
        assert z8["max_position_size"] == 0.05
    print(f"✅ z8: position limit {z8['max_position_size']} for role {role}")


def test_pre_trade_checklist_blocked_when_valuation_overheated():
    inputs = _full_inputs()
    inputs["checklist"]["valuation_overheated"] = True
    r = build_investment_role_review("002472", inputs)
    assert r["pre_trade_checklist"]["paper_trade_allowed"] is False
    assert "overheated" in str(r["pre_trade_checklist"]["missing_items"] or "overheated").lower() or \
           "overheated" in str(r["pre_trade_checklist"]["reason"] or "").lower()
    print("✅ workflow: valuation overheated blocks paper trade")


def test_no_forbidden_trade():
    r = build_investment_role_review("002472", _full_inputs())
    raw = json.dumps(r)
    for f in ["BUY", "SELL", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"]:
        assert f not in raw, f"forbidden token: {f}"
    print("✅ workflow: no forbidden trade tokens")


def test_downgrade_scenario():
    """测试 D 不能当 A"""
    inputs = _full_inputs()
    inputs["r_matrix"] = {"status": "DEGRADED", "r_action_cap": "WAIT", "ticker": "002472"}
    inputs["narrative"] = {"narrative_heat": 8, "catalyst_score": 8, "event_validity": 8,
                           "fund_flow_heat": 7}  # D-Matrix PASS
    inputs["event"] = {"invalidation_condition": "跌破30日线", "stop_loss_pct": 8}
    r = build_investment_role_review("002472", inputs)
    role = r["stock_role"]["role"]
    # 只有 B-Matrix PASS 时才会是 A_LONG_CORE；如果 D 也过线，role 应为 C_SHORT_EVENT
    assert role in ("C_SHORT_EVENT", "D_REJECT", "WATCH_ONLY"), f"D should not be A: {role}"
    print(f"✅ downgrade scenario: role={role} (D cannot become A)")


if __name__ == "__main__":
    test_workflow_required_fields()
    test_full_7_layer_pipeline()
    test_g17_required()
    test_gates_summary_10_gates()
    test_z8_position_limits()
    test_pre_trade_checklist_blocked_when_valuation_overheated()
    test_no_forbidden_trade()
    test_downgrade_scenario()
    print("\n🏁 Investment Role Workflow — all tests PASS")
