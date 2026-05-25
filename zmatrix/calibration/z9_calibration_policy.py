#!/usr/bin/env python3
"""
☯️ Z9 Calibration Policy Preview v1.0 — Batch D-4

功能:
  1. 输入 Z9_OUTCOME_BACKFILL_TASK (含 outcome_fields 填充)，输出 CALIBRATION_POLICY_PREVIEW
  2. 分析 outcome 数据对 EV / R-Matrix / G18 rule 三域的校准方向
  3. 只生成校准建议预览，不真实调参

输入: Z9_OUTCOME_BACKFILL_TASK v1.0 (outcome_fields 可有值或用模拟预览)
输出: CALIBRATION_POLICY_PREVIEW v1.0

边界:
  - auto_calibration_allowed: False
  - 不真实写 Z9
  - 不真实修改评分权重
  - 不真实修改 R-Matrix 参数
  - 不真实修改 G18 规则
  - 不真实交易
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta
from typing import Any

# ── 常量 ──
ALLOWED_PREVIEW_STATUSES = [
    "AWAITING_BACKFILL",
    "READY_FOR_REVIEW",
    "POLICY_PREVIEW_GENERATED",
    "REJECTED",
]

# Z9 Calibration Engine 的维度定义（只读引用，不真实调参）
DIMENSION_NAMES = {
    "ISS": "行业板块强度",
    "BVS": "业务价值评分",
    "EVL": "估值合理性",
    "FQS": "财务质量",
    "VSS": "量价信号",
    "CFS": "现金流状态",
    "CTS": "催化剂时序",
    "RISK": "风险扣分",
}

# G18 可校准规则域
G18_CALIBRATABLE_RULES = [
    "G09_SELL_OVERRIDE",
    "G09_HARD_BLOCKS",
    "G11_STRONG_WARNING_ONLY",
    "Z16_PRICE_GATE",
    "G17_ACCOUNT_CONFIRMATION",
    "PROBABILITY_THRESHOLD",
]

# R-Matrix 可校准周期
R_MATRIX_HORIZONS = ["SHORT_TERM", "MEDIUM_TERM", "LONG_TERM"]

_FORBIDDEN_ACTIONS = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE",
                      "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def make_calibration_policy_key(backfill_task: dict) -> str:
    """生成 calibration 策略幂等 key

    基于: task_id + ticker + 所有 outcome 实际值
    """
    task_id = backfill_task.get("task_id", "")
    ticker = backfill_task.get("ticker", "")
    of = backfill_task.get("outcome_fields", {}) or {}
    # 用 outcome 实际值参与 hash，使得 outcome 变化后 key 重新生成
    outcome_raw = ""
    for k in sorted(of.keys()):
        v = of.get(k)
        if v is not None:
            outcome_raw += str(v)
    raw = task_id + ticker + outcome_raw
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def _check_forbidden_in_backfill_task(backfill_task: dict):
    """检查 backfill task 中是否有禁止交易字段"""
    fields_to_check = []

    # 检查 source_queue_item 中的 action 字段（通过 source_queue_item 追溯）
    # backfill task 本身没有 action 字段，但需扫描 outcome_fields 中可能的误填
    of = backfill_task.get("outcome_fields", {}) or {}
    if of.get("decision_outcome") and of["decision_outcome"] in _FORBIDDEN_ACTIONS:
        raise ValueError(f"forbidden real trade in backfill outcome: {of['decision_outcome']}")

    # 检查 required_market_data 中是否有禁忌指令
    rmd = backfill_task.get("required_market_data", {}) or {}
    if rmd.get("real_fetch_allowed") is True:
        raise ValueError("real_fetch_allowed must not be True in D-4")


def _simulate_outcome_statistics(outcome_fields: dict) -> dict:
    """对单个 backfill task 的 outcome_fields 做统计分析。

    如果字段为 None（未回填），返回预设的统计骨架。
    如果已填充，计算实际统计值。

    注意：D-4 不真实调参，仅生成预览。
    """
    t1 = outcome_fields.get("actual_return_T1")
    t5 = outcome_fields.get("actual_return_T5")
    t20 = outcome_fields.get("actual_return_T20")
    dd5 = outcome_fields.get("max_drawdown_T5")
    dd20 = outcome_fields.get("max_drawdown_T20")
    ru5 = outcome_fields.get("max_runup_T5")
    ru20 = outcome_fields.get("max_runup_T20")
    decision = outcome_fields.get("decision_outcome", "PENDING_BACKFILL")

    all_none = all(x is None for x in [t1, t5, t20])

    if all_none:
        # 尚未回填，只返回骨架
        return {
            "outcome_status": "NOT_BACKFILLED",
            "t1_return": None, "t5_return": None, "t20_return": None,
            "max_drawdown_t5": None, "max_drawdown_t20": None,
            "max_runup_t5": None, "max_runup_t20": None,
            "decision_outcome": decision,
            "is_positive_t5": None,
            "has_positive_trend": None,
        }

    is_positive = t5 is not None and t5 > 0 if t5 is not None else (t1 is not None and t1 > 0)
    # 趋势判断: T5 比 T1 差（热退潮）或更好（持续走强）
    trend = "neutral"
    if t1 is not None and t5 is not None:
        if t5 > t1 + 1:
            trend = "accelerating"
        elif t5 < t1 - 1:
            trend = "decelerating"

    return {
        "outcome_status": "BACKFILLED",
        "t1_return": t1, "t5_return": t5, "t20_return": t20,
        "max_drawdown_t5": dd5, "max_drawdown_t20": dd20,
        "max_runup_t5": ru5, "max_runup_t20": ru20,
        "decision_outcome": decision,
        "is_positive_t5": is_positive,
        "has_positive_trend": trend == "accelerating",
        "trend": trend,
    }


def _generate_ev_policy_preview(stats: dict) -> dict:
    """生成 Evidence Weight (EV) 校准方向预览

    基于 outcome 统计，对七大评分维度给出校准方向建议。
    不真实修改权重。
    """
    direction = "NO_OP"
    confidence = "LOW"
    recommendations = []
    explanation = ""

    if stats["outcome_status"] == "NOT_BACKFILLED":
        return {
            "domain": "EV_CALIBRATION",
            "status": "NO_DATA",
            "direction": "WAITING_FOR_OUTCOME",
            "confidence": "NONE",
            "recommendations": [],
            "explanation": "outcome_fields 尚未回填，无法生成 EV 校准方向。",
        }

    t5 = stats.get("t5_return")
    t1 = stats.get("t1_return")

    if t5 is not None and t1 is not None:
        # 基于 T5 收益生成建议
        if t5 > 3.0:
            direction = "STRENGTHEN_POSITIVE"
            confidence = "HIGH" if t5 > 5.0 else "MEDIUM"
            recommendations = [
                "FQS: 高正收益→财务质量维度保持当前权重或略升",
                "CTS: 催化剂时序维度验证为正→建议保持权重",
                "VSS: 量价信号—验证在正收益样本中是否有效",
            ]
            explanation = f"T5=+{t5:.1f}% 正收益，说明评分系统中部分维度具备预测力。建议保持 FQS/CTS 权重，检查 VSS 区分度。"
        elif t5 < -3.0:
            direction = "REVIEW_NEGATIVE"
            confidence = "HIGH" if t5 < -5.0 else "MEDIUM"
            recommendations = [
                "所有维度: 负收益占比过高→建议进入人工复审",
                "VSS: 负收益中量价信号是否误判为正？",
                "CFS: 现金流维度是否被负收益样本拉低？",
            ]
            explanation = f"T5={t5:.1f}% 负收益，评分系统可能对当前风格不适应。建议人工介入复审评分逻辑。"
        else:
            direction = "STABLE"
            confidence = "LOW"
            recommendations = [
                "当前 EV 校准无需紧急调整，建议积累更多样本再评估",
            ]
            explanation = f"T5={t5:+.1f}% 接近零轴，评分系统在当前样本上无明显偏差。"

    return {
        "domain": "EV_CALIBRATION",
        "status": "PREVIEW_GENERATED",
        "direction": direction,
        "confidence": confidence,
        "recommendations": recommendations,
        "explanation": explanation,
    }


def _generate_rmatrix_policy_preview(stats: dict) -> dict:
    """生成 R-Matrix 校准方向预览"""
    if stats["outcome_status"] == "NOT_BACKFILLED":
        return {
            "domain": "R_MATRIX_CALIBRATION",
            "status": "NO_DATA",
            "direction": "WAITING_FOR_OUTCOME",
            "confidence": "NONE",
            "recommendations": [],
            "explanation": "outcome_fields 尚未回填，无法生成 R-Matrix 校准方向。",
        }

    trend = stats.get("trend", "neutral")
    is_positive = stats.get("is_positive_t5", None)

    direction = "NO_OP"
    confidence = "LOW"
    recommendations = []
    explanation = ""

    if trend == "accelerating":
        direction = "MAINTAIN_OR_LIGHTEN"
        confidence = "MEDIUM"
        recommendations = [
            "SHORT_TERM: 加速趋势→维持当前轮动信号",
            "MEDIUM_TERM: 观察是否演变为持续性突破",
            "LONG_TERM: 无需调整",
        ]
        explanation = "T1→T5 加速走强，R-Matrix 短周期信号有参考价值。建议维持现状。"
    elif trend == "decelerating":
        direction = "TIGHTEN_EXIT"
        confidence = "MEDIUM"
        recommendations = [
            "SHORT_TERM: 热退潮→收紧卖出信号触发条件",
            "MEDIUM_TERM: 检查是否属正常回调还是趋势反转",
            "LONG_TERM: 保持基线",
        ]
        explanation = "T1→T5 减速，R-Matrix 短周期可能存在过度乐观。建议收紧卖出信号阈值。"
    else:
        if is_positive:
            direction = "MAINTAIN_OR_LIGHTEN"
            recommendations = ["各周期波动正常，无需调整"]
            explanation = "T5 正收益但趋势平稳，R-Matrix 信号在当前样本上表现正常。"
        else:
            direction = "REVIEW"
            recommendations = ["R-Matrix 信号可能失效，建议进入人工复审"]
            explanation = "T5 负收益且趋势中性，R-Matrix 可能未捕捉到下行风险。"

    return {
        "domain": "R_MATRIX_CALIBRATION",
        "status": "PREVIEW_GENERATED",
        "direction": direction,
        "confidence": confidence,
        "recommendations": recommendations,
        "explanation": explanation,
    }


def _generate_g18_policy_preview(stats: dict) -> dict:
    """生成 G18 Rule 校准方向预览"""
    if stats["outcome_status"] == "NOT_BACKFILLED":
        return {
            "domain": "G18_RULE_CALIBRATION",
            "status": "NO_DATA",
            "direction": "WAITING_FOR_OUTCOME",
            "confidence": "NONE",
            "recommendations": [],
            "explanation": "outcome_fields 尚未回填，无法生成 G18 规则校准方向。",
        }

    t5 = stats.get("t5_return")
    decision = stats.get("decision_outcome", "PENDING_BACKFILL")

    direction = "NO_OP"
    confidence = "LOW"
    recommendations = []
    explanation = ""

    if t5 is not None:
        if t5 > 0 and decision in ("CORRECT", "PENDING_BACKFILL"):
            direction = "MAINTAIN_PROBABILITY_THRESHOLD"
            confidence = "MEDIUM"
            recommendations = [
                "PROBABILITY_THRESHOLD: 当前阈值合理",
                "G09_SELL_OVERRIDE: 未触发错误卖出",
            ]
            explanation = f"T5={t5:+.1f}% 正收益且决策正确，G18 规则集在当前样本上有效。"
        elif t5 < -3.0 and decision in ("INCORRECT", "PENDING_BACKFILL"):
            direction = "REVIEW_RULES"
            confidence = "HIGH"
            recommendations = [
                "PROBABILITY_THRESHOLD: 考虑提高下限至 0.65",
                "G09_HARD_BLOCKS: 检查是否过度阻塞了正确信号",
                "G11_STRONG_WARNING_ONLY: 检查风控是否过度",
            ]
            explanation = f"T5={t5:.1f}% 负收益，G18 规则可能过于激进或保守。建议调高概率阈值并进入复审。"
        else:
            direction = "STABLE"
            confidence = "LOW"
            recommendations = ["G18 规则在当前样本上无显著偏差"]
            explanation = f"T5={t5:+.1f}% 且决策={decision}，G18 规则无紧急校准需求。"

    return {
        "domain": "G18_RULE_CALIBRATION",
        "status": "PREVIEW_GENERATED",
        "direction": direction,
        "confidence": confidence,
        "recommendations": recommendations,
        "explanation": explanation,
        "calibratable_rules": G18_CALIBRATABLE_RULES,
    }


def build_calibration_policy_preview(
    backfill_task: dict,
    *,
    preview_id: str | None = None,
    run_id: str | None = None,
) -> dict:
    """
    从 Z9_OUTCOME_BACKFILL_TASK 构建 CALIBRATION_POLICY_PREVIEW.

    参数:
      backfill_task: Z9_OUTCOME_BACKFILL_TASK dict (outcome_fields 可为 None 或已填充)
      preview_id: 可选预览 ID
      run_id: 可选运行批次 ID

    返回:
      符合 CALIBRATION_POLICY_PREVIEW v1.0 契约的 dict
    """
    now = datetime.now()
    ticker = backfill_task.get("ticker", "UNKNOWN")
    task_id = backfill_task.get("task_id", "UNKNOWN")
    run_id = run_id or now.strftime("%Y%m%d_%H%M%S")
    preview_id = preview_id or f"CP_{task_id}_{now.strftime('%Y%m%d_%H%M%S')}"

    # 禁止交易 + 安全检查
    _check_forbidden_in_backfill_task(backfill_task)

    # outcome 统计
    outcome_fields = backfill_task.get("outcome_fields", {}) or {}
    stats = _simulate_outcome_statistics(outcome_fields)

    # 三域校准方向预览
    ev_preview = _generate_ev_policy_preview(stats)
    rmatrix_preview = _generate_rmatrix_policy_preview(stats)
    g18_preview = _generate_g18_policy_preview(stats)

    # 幂等 key
    policy_key = make_calibration_policy_key(backfill_task)

    # 状态机
    if stats["outcome_status"] == "NOT_BACKFILLED":
        status = "AWAITING_BACKFILL"
        reason = "D4_PREVIEW_MODE_OUTCOME_NOT_BACKFILLED"
        ready = False
    else:
        status = "POLICY_PREVIEW_GENERATED"
        reason = "D4_PREVIEW_MODE"
        ready = True

    return {
        "preview_version": "v1.0",
        "preview_type": "CALIBRATION_POLICY_PREVIEW",
        "preview_id": preview_id,
        "run_id": run_id,
        "task_id": task_id,
        "ticker": ticker,
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "source_backfill_task": {
            "task_id": task_id,
            "task_version": backfill_task.get("task_version"),
            "task_type": backfill_task.get("task_type"),
            "backfill_task_key": backfill_task.get("idempotency", {}).get("backfill_task_key", ""),
        },
        "idempotency": {
            "calibration_policy_key": policy_key,
            "source_task_id": task_id,
            "same_preview_recreate_allowed": False,
        },
        "outcome_summary": stats,
        "policy_domains": {
            "ev_calibration": ev_preview,
            "r_matrix_calibration": rmatrix_preview,
            "g18_rule_calibration": g18_preview,
        },
        "state": {
            "status": status,
            "allowed_statuses": ALLOWED_PREVIEW_STATUSES,
            "reason": reason,
            "ready_for_calibration": ready,
        },
        "validation": {
            "backfill_task_valid": True,
            "reject_reasons": [],
            "auto_calibration_allowed": False,
        },
        "write_policy": {
            "ev_write_allowed": False,
            "r_matrix_write_allowed": False,
            "g18_write_allowed": False,
            "z9_write_allowed": False,
            "write_status": "DEFERRED_NOT_CONNECTED",
            "reason": "D4_CALIBRATION_POLICY_PREVIEW_ONLY_NO_REAL_WRITE",
        },
        "forbidden_real_trade_checked": True,
    }


def generate_calibration_report(previews: list[dict]) -> str:
    """生成人类可读的校准策略预览报告"""
    lines = []
    lines.append("═══ ☯️ Z9 Calibration Policy Preview Report v1.0 ═══")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST")
    lines.append(f"预览总数: {len(previews)}")
    lines.append("")

    ready = sum(1 for p in previews if p["state"]["ready_for_calibration"])
    awaiting = len(previews) - ready

    lines.append("## 一、概览")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总预览 | {len(previews)} |")
    lines.append(f"| 可生成建议(ready) | {ready} |")
    lines.append(f"| 等待回填(awaiting) | {awaiting} |")
    lines.append("")

    if ready > 0:
        lines.append("## 二、校准方向汇总")
        lines.append(f"| 标的 | EV方向 | R-Matrix方向 | G18方向 |")
        lines.append(f"|------|--------|-------------|--------|")
        for p in previews:
            if not p["state"]["ready_for_calibration"]:
                continue
            ev = p["policy_domains"]["ev_calibration"]["direction"]
            rm = p["policy_domains"]["r_matrix_calibration"]["direction"]
            g18 = p["policy_domains"]["g18_rule_calibration"]["direction"]
            lines.append(f"| {p['ticker']} | {ev} | {rm} | {g18} |")
        lines.append("")

    lines.append("## 三、D-4 边界")
    lines.append(f"- auto_calibration_allowed: 始终为 False")
    lines.append(f"- EV 权重: 预览模式，不真实修改")
    lines.append(f"- R-Matrix 参数: 预览模式，不真实修改")
    lines.append(f"- G18 规则: 预览模式，不真实修改")
    lines.append(f"- D-4 仅生成建议方向，实际调参需人工确认或后续 Batch")

    return "\n".join(lines)


# ═══ CLI ═══
def _main():
    import argparse, json, os, sys

    parser = argparse.ArgumentParser(description="☯️ Z9 Calibration Policy Preview v1.0 (Contract Only)")
    sub = parser.add_subparsers(dest="command")

    preview = sub.add_parser("preview", help="Generate calibration policy preview from a backfill task JSON")
    preview.add_argument("--backfill-task-file", required=True)
    preview.add_argument("--output", default=None)

    args = parser.parse_args()

    if args.command == "preview":
        if not os.path.exists(args.backfill_task_file):
            print(f"❌ 文件不存在: {args.backfill_task_file}")
            sys.exit(1)
        with open(args.backfill_task_file) as f:
            task = json.load(f)
        preview = build_calibration_policy_preview(task)
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        if args.output:
            with open(args.output, "w") as f:
                json.dump(preview, f, ensure_ascii=False, indent=2)
        print("\n" + generate_calibration_report([preview]))
    else:
        parser.print_help()


if __name__ == "__main__":
    _main()
