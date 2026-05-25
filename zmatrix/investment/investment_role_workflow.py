"""☯️ Investment Role Workflow v1.0 — 7层过滤硬门 (v2.9.8-dev)"""
from __future__ import annotations
from datetime import datetime
from zmatrix.investment.chain_force import evaluate_chain_force_10x5
from zmatrix.investment.sector_stage import detect_sector_stage
from zmatrix.investment.financial_health_gate import check_financial_health
from zmatrix.investment.b_matrix import evaluate_b_matrix
from zmatrix.investment.d_matrix import evaluate_d_matrix
from zmatrix.investment.stock_role_classifier import classify_stock_role
from zmatrix.investment.account_constitution import check_account_constitution
from zmatrix.investment.portfolio_exposure import analyze_portfolio_exposure
from zmatrix.investment.z8_position_control import evaluate_z8_position_control
from zmatrix.investment.pre_trade_checklist import validate_pre_trade_checklist
from zmatrix.investment.g17_human_veto import build_g17_human_veto_preview


def build_investment_role_review(ticker: str, inputs: dict | None = None) -> dict:
    now = datetime.now(); inputs = inputs or {}
    # ── 1: 10链×5力 ──
    chain_result = evaluate_chain_force_10x5({
        "ticker": ticker, "chain": inputs.get("chain"),
        "force_scores": inputs.get("force_scores", {}),
    })
    # ── 2: 板块阶段 ──
    stage_result = detect_sector_stage({"ticker": ticker, "sector": inputs.get("sector"), "sector_stage": inputs.get("sector_stage")})
    # ── 3: 个股健康硬门 ──
    health_result = check_financial_health({"ticker": ticker}, fundamentals=inputs.get("fundamentals"))
    # ── 4a: B-Matrix ──
    b_result = evaluate_b_matrix(ticker, fundamentals=inputs.get("fundamentals"), valuation=inputs.get("valuation"))
    # ── 4b: R-Matrix ──
    r_result = inputs.get("r_matrix", {"status": "DEGRADED", "r_action_cap": "WAIT", "ticker": ticker})
    # ── 4c: D-Matrix ──
    d_result = evaluate_d_matrix(ticker, narrative=inputs.get("narrative"), event=inputs.get("event"))
    # ── 4d: Stock Role ──
    role_result = classify_stock_role(ticker, b_matrix=b_result, r_matrix=r_result, d_matrix=d_result,
                                      account=inputs.get("account_state"), exposure=inputs.get("portfolio_exposure_summary"))
    # ── 5: Account ──
    account_result = check_account_constitution(role_result, account_state=inputs.get("account_state"))
    # ── 6: Exposure ──
    exposure_candidate = {
        "ticker": ticker,
        "chain": inputs.get("chain"),
        "sector": inputs.get("sector"),
        "style_factor": inputs.get("style_factor"),
        "market_beta": inputs.get("market_beta"),
        "sector_beta": inputs.get("sector_beta"),
        "max_drawdown": inputs.get("max_drawdown"),
        "drawdown_overlap": inputs.get("drawdown_overlap"),
        "correlation_60d": inputs.get("correlation_60d"),
        "correlation_120d": inputs.get("correlation_120d"),
        "correlation_250d": inputs.get("correlation_250d"),
    }
    exposure_result = analyze_portfolio_exposure(exposure_candidate, portfolio=inputs.get("portfolio"))
    # ── 7a: Z8 ──
    z8_result = evaluate_z8_position_control(role_result, account=account_result, exposure=exposure_result)
    # ── 7b: Pre-Trade Checklist（自动补 stock_role） ──
    checklist_input = {**inputs.get("checklist", {}), **role_result,
                       "stock_role": role_result.get("role"),
                       "sector_stage": stage_result.get("sector_stage"),
                       "financial_gate_passed": health_result.get("financial_gate_passed"),
                       "sector": inputs.get("sector")}
    checklist_result = validate_pre_trade_checklist(checklist_input)
    # ── 7c: G17 ──
    g17_result = build_g17_human_veto_preview(role_result)

    # ── 7层硬门判定 ──
    all_gates_passed = all([
        chain_result.get("chain_gate_passed") is True and chain_result.get("degraded") is not True,
        stage_result.get("new_position_allowed") is True and stage_result.get("sector_stage") not in ("CLIMAX","RETREAT","DIVERGENCE","UNKNOWN"),
        health_result.get("financial_gate_passed") is True,
        role_result.get("role") not in ("D_REJECT","WATCH_ONLY"),
        role_result.get("paper_record_allowed") is True,
        account_result.get("account_gate_passed") is True,
        exposure_result.get("exposure_gate_passed") is True and not exposure_result.get("degraded", False),
        z8_result.get("position_allowed") is True,
        checklist_result.get("paper_trade_allowed") is True,
        g17_result.get("human_final_override_required") is True,
    ])

    return {
        "workflow_version": "v1.0", "ticker": ticker,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "chain_force": chain_result, "sector_stage": stage_result,
        "financial_health": health_result,
        "b_matrix": b_result, "r_matrix": r_result, "d_matrix": d_result,
        "stock_role": role_result,
        "account_constitution": account_result,
        "portfolio_exposure": exposure_result,
        "z8_position_control": z8_result,
        "pre_trade_checklist": checklist_result,
        "g17_human_veto": g17_result,
        "paper_record_allowed": all_gates_passed,
        "real_trade_allowed": False,
        "next_allowed_action": "PAPER_TRACK" if all_gates_passed else "WAIT",
        "gates_summary": {
            "chain_force": "PASS" if chain_result.get("chain_gate_passed") and not chain_result.get("degraded") else "FAIL",
            "sector_stage": "PASS" if stage_result.get("new_position_allowed") and stage_result.get("sector_stage") not in ("CLIMAX","RETREAT","DIVERGENCE","UNKNOWN") else "FAIL",
            "financial_health": "PASS" if health_result.get("financial_gate_passed") else "FAIL",
            "b_matrix": b_result.get("status", "DEGRADED"),
            "stock_role": role_result.get("role", "D_REJECT"),
            "account_constitution": "PASS" if account_result.get("account_gate_passed") else "FAIL",
            "portfolio_exposure": "PASS" if exposure_result.get("exposure_gate_passed") and not exposure_result.get("degraded") else "FAIL",
            "z8_position_control": "PASS" if z8_result.get("position_allowed") else "FAIL",
            "pre_trade_checklist": "PASS" if checklist_result.get("paper_trade_allowed") else "FAIL",
            "g17_human_veto": "REQUIRED",
        },
        "paper_ledger_required": True,
        "outcome_backfill_required": True,
        "data_fact_required": True,
        "next_required_workflow": "paper_trade_ledger" if all_gates_passed else None,
        "g17_human_veto_required": True,
        "forbidden_real_trade_checked": True,
    }
