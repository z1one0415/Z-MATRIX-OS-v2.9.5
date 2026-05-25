"""☯️ Stock Role Classifier v1.0 (v2.9.8-dev) — B/R/D → A/B/C/D"""
from __future__ import annotations
from datetime import datetime

ROLES = frozenset({"A_LONG_CORE", "B_MID_ROTATION", "C_SHORT_EVENT", "D_REJECT", "WATCH_ONLY"})

def classify_stock_role(ticker, b_matrix, r_matrix, d_matrix, account=None, exposure=None):
    now = datetime.now()
    account = account or {}; exposure = exposure or {}
    b_pass = b_matrix.get("status") == "PASS" and b_matrix.get("base_role_eligible") is True
    r_pass = r_matrix.get("status") == "PASS" and r_matrix.get("r_action_cap") not in ("WAIT", "BLOCKED", None)
    d_pass = d_matrix.get("status") == "PASS" and d_matrix.get("short_event_eligible") is True
    blocked_by_account = len(account.get("violation_reasons", []) or []) + len(exposure.get("warnings", []) or []) > 0
    downgrade_reasons = []

    # 多矩阵冲突检测
    matrix_count = sum([b_pass, r_pass, d_pass])
    if matrix_count >= 2:
        # B + R 可允许 A 或 B
        if b_pass and r_pass and not d_pass:
            role = "A_LONG_CORE"; src = "B-MATRIX"; period = "long_term"
            allowed = ["PAPER_TRACK", "HOLD"]; must = ["b_matrix.base_valid","r_matrix.cycle_valid","account.constitution.valid"]
            disallowed = ["SHORT_TERM_TRADE","EVENT_BET"]
        # D 与任何其他矩阵冲突 → WATCH_ONLY
        elif d_pass:
            role = "WATCH_ONLY"; src = "MULTI_MATRIX_CONFLICT"; period = None
            allowed = ["WATCH"]; must = []; disallowed = ["ANY_TRADE","PAPER_TRACK"]
            downgrade_reasons.append("MULTI_MATRIX_CONFLICT_REQUIRES_G17")
        else:
            role = "WATCH_ONLY"; src = "MULTIPLE"; period = None
            allowed = ["WATCH"]; must = []; disallowed = ["ANY_TRADE"]
    elif b_pass and not blocked_by_account:
        role = "A_LONG_CORE"; src = "B-MATRIX"; period = "long_term"
        allowed = ["PAPER_TRACK", "HOLD"]; must = ["b_matrix.base_valid","account.constitution.valid","portfolio.exposure.valid"]
        disallowed = ["SHORT_TERM_TRADE","EVENT_BET"]
    elif r_pass and not blocked_by_account:
        role = "B_MID_ROTATION"; src = "R-MATRIX"; period = "mid_term"
        allowed = ["PAPER_TRACK", "WATCH"]; must = ["r_matrix.cycle_valid","account.constitution.valid"]
        disallowed = ["LONG_HOLD","EVENT_BET"]
    elif d_pass and not blocked_by_account:
        role = "C_SHORT_EVENT"; src = "D-MATRIX"; period = "short_term"
        allowed = ["PAPER_PROBE"]; must = ["d_matrix.event_valid","pre_trade.checklist.complete"]
        disallowed = ["LONG_HOLD","CONVERT_TO_BASE"]
        downgrade_reasons.append("D-MATRIX: cannot_convert_to_base=True")
    elif b_pass or r_pass or d_pass:
        role = "WATCH_ONLY"; src = "MULTIPLE"; period = None
        allowed = ["WATCH"]; must = []; disallowed = ["ANY_TRADE"]
        if blocked_by_account: downgrade_reasons.append("BLOCKED_BY_ACCOUNT")
    else:
        role = "D_REJECT"; src = "NONE"; period = None
        allowed = []; must = []; disallowed = ["ANY_TRADE","PAPER_TRACK","PAPER_PROBE"]
        downgrade_reasons.append("ALL_MATRICES_REJECTED")

    paper_record_allowed = role not in ("D_REJECT", "WATCH_ONLY")
    return {
        "classifier_version": "v1.0", "ticker": ticker,
        "role": role, "role_source_matrix": src, "holding_period": period,
        "allowed_actions": allowed, "must_pass_gates": must,
        "disallowed_actions": disallowed, "downgrade_reasons": downgrade_reasons,
        "paper_record_allowed": paper_record_allowed, "real_trade_allowed": False,
        "b_matrix_pass": b_pass, "r_matrix_pass": r_pass, "d_matrix_pass": d_pass,
        "blocked_by_account": blocked_by_account,
        "forbidden_real_trade_checked": True,
    }
