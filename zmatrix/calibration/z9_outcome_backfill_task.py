#!/usr/bin/env python3
"""
☯️ Z9 Outcome Backfill Task v1.0 — D-3: Contract freeze only

功能:
  1. 定义 outcome backfill task 契约结构
  2. 生成 Z9_OUTCOME_BACKFILL_TASK preview (不含真实行情回填)
  3. 定义 T1/T5/T20 回填任务字段
  4. 仍不写数据库，仍不自动校准参数

输入: Z9_INGESTION_QUEUE_ITEM
输出: Z9_OUTCOME_BACKFILL_TASK / PREVIEW

使用方式:
  python3 -m zmatrix.calibration.z9_outcome_backfill_task preview --sample-file sample.json
"""
from __future__ import annotations

import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKSPACE))

from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item

# ── 常量 ──
HORIZON_MAP = {
    "T1": 1,
    "T5": 5,
    "T20": 20,
}
ALLOWED_TASK_STATUSES = ["PENDING_BACKFILL", "BACKFILL_IN_PROGRESS", "BACKFILL_COMPLETE", "BACKFILL_FAILED"]
_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}


def build_z9_outcome_backfill_task(
    sample: dict,
    *,
    task_id: str | None = None,
    ticker: str | None = None,
    pred_date: str | None = None,
    horizons: list[str] | None = None,
) -> dict:
    """
    构建 outcome backfill task preview.

    输入: Z9_CALIBRATION_SAMPLE (或 Z9_INGESTION_QUEUE_ITEM)
    输出: Z9_OUTCOME_BACKFILL_TASK (不含真实行情回填)

    参数:
      sample: Z9样本dict
      ticker: 覆盖sample["ticker"]
      pred_date: 覆盖sample["created_at"]
      horizons: 回填期限列表, 默认["T1","T5","T20"]
    """
    ticker = ticker or sample.get("ticker", "")
    pred_date = pred_date or sample.get("created_at", "")[:10]
    if not pred_date and sample.get("pred_date"):
        pred_date = sample["pred_date"]
    horizons = horizons or ["T1", "T5", "T20"]

    sample_id = sample.get("sample_id", "UNKNOWN")
    task_id = task_id or f"BF_{sample_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    now = datetime.now()
    pred_dt = datetime.strptime(pred_date, "%Y-%m-%d") if pred_date and len(pred_date) >= 10 else now

    # ── 判定各horizon是否到期 ──
    horizon_statuses = {}
    all_matured = True
    for h in horizons:
        horizon_days = HORIZON_MAP[h]
        target_dt = pred_dt + timedelta(days=horizon_days)
        is_matured = target_dt <= now
        horizon_statuses[h] = {
            "horizon_days": horizon_days,
            "target_date": target_dt.strftime("%Y-%m-%d"),
            "is_matured": is_matured,
            "days_remaining": 0 if is_matured else (target_dt - now).days,
            "ready_for_backfill": is_matured,
            "field": f"actual_return_{h}",
        }
        if not is_matured:
            all_matured = False

    # ── 任务状态 ──
    if all_matured:
        task_status = "PENDING_BACKFILL"
        backfill_ready = True
    else:
        task_status = "WAITING_FOR_FUTURE_MARKET_DATA"
        backfill_ready = False

    # ── 派生字段 ──
    outcome_template = {}
    for h in horizons:
        outcome_template[f"actual_return_{h}"] = None
    outcome_template["max_drawdown_T5"] = None
    outcome_template["max_drawdown_T20"] = None
    outcome_template["decision_outcome"] = "PENDING_REVIEW"
    outcome_template["review_status"] = "WAITING_FOR_FUTURE_MARKET_DATA" if not all_matured else "PENDING_BACKFILL"

    # ── 禁止交易检查 ──
    _check_forbidden(sample)

    # ── 构造 queue preview（用于审计追溯） ──
    queue_preview = build_z9_ingestion_queue_item(sample)

    return {
        "task_version": "v1.0",
        "task_type": "Z9_OUTCOME_BACKFILL_TASK",
        "task_id": task_id,
        "sample_id": sample_id,
        "ticker": ticker,
        "pred_date": pred_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task_state": {
            "status": task_status,
            "allowed_statuses": ALLOWED_TASK_STATUSES,
            "reason": f"D3_CONTRACT_ONLY_NO_REAL_BACKFILL" if all_matured else
                      f"D3_CONTRACT_ONLY_HORIZON_NOT_MATURED",
            "all_horizons_matured": all_matured,
        },
        "backfill_spec": {
            "horizons": horizons,
            "horizon_details": horizon_statuses,
            "backfill_ready": backfill_ready,
            "data_source": "EASTMONEY_HISTORICAL_KLINE",
            "adjustment": "FORWARD_ADJUSTED",
        },
        "outcome_target": outcome_template,
        "provenance": {
            "source_queue_item": {
                "queue_id": queue_preview["queue_id"],
                "queue_type": queue_preview["queue_type"],
                "idempotency_key": queue_preview["idempotency"]["idempotency_key"],
                "source_record_ref": queue_preview["idempotency"]["source_record_ref"],
            },
            "source_sample": {
                "sample_id": sample_id,
                "sample_version": sample.get("sample_version"),
            },
        },
        "write_policy": {
            "backfill_write_allowed": False,
            "z9_write_allowed": False,
            "write_status": "DEFERRED_NOT_CONNECTED",
            "reason": "D3_CONTRACT_ONLY_NO_REAL_BACKFILL",
        },
        "forbidden_real_trade_checked": True,
    }


def _check_forbidden(sample: dict):
    """检查sample中是否包含禁止交易字段"""
    ds = sample.get("decision_snapshot", {}) or {}
    for fld in [ds.get("entry_intent"), ds.get("exit_intent"), ds.get("paper_action"), ds.get("action_cap")]:
        if fld and fld in _FORBIDDEN:
            raise ValueError(f"forbidden real trade in backfill task: {fld}")
    op = sample.get("outcome_placeholder", {}) or {}
    if op.get("decision_outcome") and op["decision_outcome"] in _FORBIDDEN:
        raise ValueError(f"forbidden real trade in outcome: {op['decision_outcome']}")


def generate_backfill_task_report(tasks: list[dict]) -> str:
    """生成人类可读的任务报告"""
    lines = []
    lines.append("═══ ☯️ Z9 Outcome Backfill Task Report v1.0 ═══")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST")
    lines.append(f"任务总数: {len(tasks)}")
    lines.append("")

    ready = sum(1 for t in tasks if t["backfill_spec"]["backfill_ready"])
    waiting = len(tasks) - ready

    lines.append("## 一、概览")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总任务 | {len(tasks)} |")
    lines.append(f"| 可回填(ready) | {ready} |")
    lines.append(f"| 等待中(waiting) | {waiting} |")
    lines.append(f"| D-3模式 | CONTRACT_ONLY |")
    lines.append("")

    if tasks:
        lines.append("## 二、逐任务详情")
        lines.append(f"| 序号 | 标的 | 预测日 | 状态 | 到期horizon | 下个到期日 |")
        lines.append(f"|------|------|--------|------|-------------|------------|")
        for i, t in enumerate(tasks, 1):
            matured = [h for h, s in t["backfill_spec"]["horizon_details"].items() if s["is_matured"]]
            next_waiting = [s for h, s in t["backfill_spec"]["horizon_details"].items() if not s["is_matured"]]
            matured_str = ",".join(matured) if matured else "—"
            next_str = next_waiting[0]["target_date"] + f" (T+{next_waiting[0]['horizon_days']})" if next_waiting else "—"
            lines.append(f"| {i} | {t['ticker']} | {t['pred_date']} | {t['task_state']['status']} | {matured_str} | {next_str} |")

    lines.append("")
    lines.append("## 三、天师解读")
    if ready > 0:
        lines.append(f"**{ready}个任务可回填**: 市场数据已积累到足够的历史窗口。")
        lines.append(f"但D-3当前为CONTRACT_ONLY阶段，不执行真实数据拉取。")
        lines.append(f"待D-3 contract freeze确认后，才允许启用真实行情回填。")
    else:
        lines.append(f"**全部等待中**: 所有任务的T+N horizon均未到期。")
        lines.append(f"这是正常状态——D-3仅定义回填任务的契约结构，不执行行情回填。")
    lines.append(f"D-3产出为Z9_OUTCOME_BACKFILL_TASK preview，与Queue预览形成互为审计的闭环。")

    return "\n".join(lines)


# ═══ CLI ═══
def _main():
    import argparse

    parser = argparse.ArgumentParser(description="☯️ Z9 Outcome Backfill Task v1.0 (Contract Only)")
    sub = parser.add_subparsers(dest="command")

    preview = sub.add_parser("preview", help="Generate backfill task preview from a sample JSON")
    preview.add_argument("--sample-file", required=True)
    preview.add_argument("--ticker", default=None)
    preview.add_argument("--pred-date", default=None)
    preview.add_argument("--horizons", nargs="*", default=["T1", "T5", "T20"])
    preview.add_argument("--output", default=None)

    args = parser.parse_args()

    if args.command == "preview":
        if not os.path.exists(args.sample_file):
            print(f"❌ 文件不存在: {args.sample_file}")
            sys.exit(1)
        with open(args.sample_file) as f:
            sample = json.load(f)
        task = build_z9_outcome_backfill_task(
            sample,
            ticker=args.ticker,
            pred_date=args.pred_date,
            horizons=args.horizons,
        )
        print(json.dumps(task, ensure_ascii=False, indent=2))
        if args.output:
            with open(args.output, "w") as f:
                json.dump(task, f, ensure_ascii=False, indent=2)

        # 生成报告
        print("\n" + generate_backfill_task_report([task]))
    else:
        parser.print_help()


if __name__ == "__main__":
    _main()
