#!/usr/bin/env python3
"""
☯️ Z9 Calibration Engine v1.0 — 后验校准核心
功能:
  backtest_at(N): 对calibration_db.json中所有预测做T+N回验
  adjust_weights(): 当累计校准≥3次, 自动分析各维度预测力并修正评分权重
输出: 校准报告 → stdout + 更新calibration_db.json
"""
from __future__ import annotations

import json, os, sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from collections import defaultdict
import urllib.request

# ── 路径 ──
WORKSPACE = Path(os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace"))
CALIBRATION_DB = WORKSPACE / "hermes" / "calibration_db.json"
CACHE_DIR = WORKSPACE / "cache"
REPORT_DIR = WORKSPACE / "记忆宫殿" / "Z2信息熔炉" / "超级预测系统" / "预测记录"

# ── T+0 验证价格(收盘快照, 用作backtest基准) ──
# 按日期索引 {date_str: {code: {"price": float, "pct": float}}}
VERIFICATION_SNAPSHOTS: dict[str, dict] = {}

# ── 评分维度说明 ──
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


class Z9CalibrationEngine:
    """后验校准引擎 — T+N回验 + 权重自适应修正"""

    def __init__(self):
        self.db = self._load_db()
        self.results: list[dict] = []
        self.all_ticker_returns: dict[str, dict] = {}  # code -> {pred_date, pred_price, actual_price, return_pct}

    def _load_db(self) -> dict:
        if CALIBRATION_DB.exists():
            with open(CALIBRATION_DB) as f:
                return json.load(f)
        return {"predictions": [], "weights": {
            "ISS": 0.15, "BVS": 0.15, "EVL": 0.15,
            "FQS": 0.20, "VSS": 0.15, "CFS": 0.10, "CTS": 0.05
        }, "weight_history": [], "calibration_log": []}

    def _save_db(self):
        CALIBRATION_DB.parent.mkdir(parents=True, exist_ok=True)
        with open(CALIBRATION_DB, "w") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

    # ═══ 实时价格获取 ═══

    def _fetch_live_prices(self, codes: list[str]) -> dict:
        """拉取东方财富实时/收盘行情"""
        def secid(c):
            return f"1.{c}" if c[0] in "569" else f"0.{c}"
        secids = [secid(c) for c in codes]
        url = ("https://push2.eastmoney.com/api/qt/ulist.np/get"
               f"?fltt=2&fields=f2,f3,f12,f14&secids={','.join(secids)}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
            results = {}
            for item in data.get("data", {}).get("diff", []):
                results[item.get("f12", "")] = {
                    "name": item.get("f14", "?"),
                    "price": item.get("f2"),
                    "pct": item.get("f3"),
                }
            return results
        except Exception as e:
            print(f"  ⚠️ API拉取失败: {e}")
            return {}

    # ═══ 主入口: T+N 回验 ═══

    def backtest_at(self, days: int = 5, live_prices: dict | None = None):
        """
        对calibration_db中所有预测做T+days回验。

        流程:
          1. 加载所有预测
          2. 对于每条预测, 获取预测日期+价格 → 查找T+days实际价格
          3. 计算: 方向准确率 / 总分与实际收益相关性 / 各维度预测力
          4. 写入calibration_log
          5. 如累计≥3次校准, 触发adjust_weights()
        """
        predictions = self.db.get("predictions", [])
        if not predictions:
            print("⚠️ calibration_db中无预测记录, 跳过回验。")
            return {"error": "no_predictions", "calibrations": 0}

        # 获取实时价格(当前T+0价格作为最新验证点)
        all_codes = set()
        for pred in predictions:
            for code in pred.get("tickers", {}):
                all_codes.add(code)
        if live_prices is None:
            live_prices = self._fetch_live_prices(list(all_codes))
        print(f"  📡 获取到 {len(live_prices)} 只标的最新价格")

        # 统计所有预测中每个ticker的价格历史
        # 由于calibration_db按预测批次存储, 我们需要建立: code → [(pred_date, pred_price, total_score, action)]
        ticker_predictions: dict[str, list[dict]] = defaultdict(list)
        for pred in predictions:
            pred_date = pred.get("report_date", "unknown")
            for code, info in pred.get("tickers", {}).items():
                ticker_predictions[code].append({
                    "pred_date": pred_date,
                    "pred_price": info.get("price", 0),
                    "total_score": info.get("total", 0),
                    "action": info.get("action", "UNKNOWN"),
                    "cf_state": info.get("cf_state", "UNKNOWN"),
                    "scores": info.get("scores", {}),
                    "name": info.get("name", code),
                })

        # ── 对每只标的, 计算T+days实际收益 ──
        cal_entries = []
        for code, preds in ticker_predictions.items():
            live = live_prices.get(code, {})
            live_price = live.get("price")
            if live_price is None:
                continue

            for p in preds:
                pred_price = p["pred_price"]
                if pred_price <= 0:
                    continue

                # 计算实际收益
                actual_return = (live_price / pred_price - 1) * 100

                # 计算预测日期到现在的日历天数(用于标注实际间隔)
                try:
                    pred_dt = datetime.strptime(p["pred_date"], "%Y-%m-%d")
                    actual_days = (datetime.now() - pred_dt).days
                except:
                    actual_days = days  # fallback

                # 方向判定: action映射
                action_map = {
                    "WATCH": "bullish",
                    "TRACK_ONLY": "neutral",
                    "EXCLUDE": "bearish",
                    "UNKNOWN": "neutral",
                }
                predicted_direction = action_map.get(p["action"], "neutral")

                # 实际方向
                if actual_return > 1.0:
                    actual_direction = "bullish"
                elif actual_return < -1.0:
                    actual_direction = "bearish"
                else:
                    actual_direction = "neutral"

                # 方向准确?
                direction_correct = (predicted_direction == actual_direction)

                # 评分与实际收益的Spearman近似(简单比较总分排位 vs 收益排位)
                cal_entries.append({
                    "code": code,
                    "name": p["name"],
                    "pred_date": p["pred_date"],
                    "pred_price": pred_price,
                    "actual_price": live_price,
                    "actual_days": actual_days,
                    "target_days": days,
                    "actual_return_pct": round(actual_return, 2),
                    "predicted_action": p["action"],
                    "predicted_direction": predicted_direction,
                    "actual_direction": actual_direction,
                    "direction_correct": direction_correct,
                    "total_score": p["total_score"],
                    "cf_state": p["cf_state"],
                    "scores": p["scores"],
                })

        if not cal_entries:
            print("⚠️ 无有效回验数据(缺少价格)。")
            return {"error": "no_price_data", "calibrations": 0}

        # ── 汇总统计 ──
        direction_correct_count = sum(1 for e in cal_entries if e["direction_correct"])
        total_entries = len(cal_entries)
        direction_accuracy = direction_correct_count / total_entries * 100 if total_entries > 0 else 0

        # 按action分组统计
        action_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        for e in cal_entries:
            action_stats[e["predicted_action"]]["total"] += 1
            if e["direction_correct"]:
                action_stats[e["predicted_action"]]["correct"] += 1

        # 总分与实际收益的相关性(简化为: 高分组 vs 低分组的平均收益差异)
        sorted_entries = sorted(cal_entries, key=lambda x: x["total_score"], reverse=True)
        n = len(sorted_entries)
        top_third = sorted_entries[:max(1, n // 3)]
        bottom_third = sorted_entries[-max(1, n // 3):]
        top_avg_return = sum(e["actual_return_pct"] for e in top_third) / len(top_third)
        bottom_avg_return = sum(e["actual_return_pct"] for e in bottom_third) / len(bottom_third)
        score_return_spread = top_avg_return - bottom_avg_return

        # 各维度与收益的相关系数(近似)
        dimension_correlations = {}
        for dim in ["ISS", "BVS", "EVL", "FQS", "VSS", "CFS", "CTS"]:
            dim_scores = []
            returns_list = []
            for e in cal_entries:
                s = e["scores"].get(dim)
                if s is not None:
                    dim_scores.append(s)
                    returns_list.append(e["actual_return_pct"])
            if len(dim_scores) >= 5:
                # Pearson近似(简化, 用排序相关)
                corr = self._approx_correlation(dim_scores, returns_list)
                dimension_correlations[dim] = round(corr, 3)

        # ── 构建校准记录 ──
        calibration_record = {
            "calibration_id": f"cal_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "target_days": days,
            "actual_data_note": f"T+{days}目标, 实际使用T+{min(e['actual_days'] for e in cal_entries)}~T+{max(e['actual_days'] for e in cal_entries)}数据",
            "total_predictions": total_entries,
            "direction_accuracy": round(direction_accuracy, 1),
            "score_return_spread": round(score_return_spread, 2),
            "action_accuracy": {k: {"correct": v["correct"], "total": v["total"],
                                     "accuracy": round(v["correct"] / v["total"] * 100, 1)}
                               for k, v in action_stats.items()},
            "dimension_correlations": dimension_correlations,
            "ticker_details": cal_entries,
        }

        # 写入DB
        self.db["calibration_log"].append(calibration_record)
        self._save_db()

        # 存储供adjust_weights使用
        self._last_calibration = calibration_record

        print(f"\n  ✅ T+{days}回验完成: {total_entries}条预测")
        print(f"  📊 方向准确率: {direction_accuracy:.1f}%")
        print(f"  📈 高-低分组收益差: {score_return_spread:+.2f}%")
        print(f"  🔢 维度相关性: {dimension_correlations}")

        # 累计校准次数
        cal_count = len(self.db["calibration_log"])
        print(f"  📋 累计校准次数: {cal_count}")

        # ≥3次则触发权重修正
        if cal_count >= 3:
            print(f"\n  ⚡ 累计{cal_count}次校准 → 触发 adjust_weights()")
            weight_report = self.adjust_weights()
            calibration_record["weight_adjustment"] = weight_report
            self._save_db()

        return calibration_record

    # ═══ 权重自适应修正 ═══

    def adjust_weights(self) -> dict:
        """
        基于历史校准数据, 分析各维度的预测力, 自动修正评分权重。

        策略:
          - 对每个维度, 汇总所有校准中的correlation
          - 正相关→保留/提升权重; 负相关→降权/标记
          - RISK维度特殊处理(作为惩罚项)
          - 权重变化不超±0.05(单次调整上限, 防过拟合)
        """
        cal_log = self.db.get("calibration_log", [])
        if len(cal_log) < 3:
            return {"status": "skipped", "reason": f"仅{len(cal_log)}次校准, 需≥3次"}

        # 汇总所有校准的维度相关性
        dim_corrs: dict[str, list[float]] = defaultdict(list)
        for cal in cal_log:
            for dim, corr in cal.get("dimension_correlations", {}).items():
                dim_corrs[dim].append(corr)

        # 计算每个维度的平均相关性
        dim_avg: dict[str, float] = {}
        for dim, corrs in dim_corrs.items():
            if corrs:
                dim_avg[dim] = sum(corrs) / len(corrs)

        # 基于相关性信号修正权重
        current_weights = self.db.get("weights", {}).copy()
        new_weights = current_weights.copy()

        adjustments = []
        for dim, avg_corr in sorted(dim_avg.items(), key=lambda x: x[1], reverse=True):
            old_w = current_weights.get(dim, 0.10)
            signal = "🟢 正相关" if avg_corr > 0.10 else ("🟡 弱相关" if avg_corr > -0.10 else "🔴 负相关")

            if avg_corr > 0.15:
                # 强正相关 → 提升权重
                delta = min(0.05, avg_corr * 0.1)
                new_weights[dim] = round(min(old_w + delta, 0.30), 3)
            elif avg_corr < -0.10:
                # 负相关 → 降低权重
                delta = min(0.05, abs(avg_corr) * 0.1)
                new_weights[dim] = round(max(old_w - delta, 0.02), 3)
            else:
                # 弱相关 → 微调
                new_weights[dim] = old_w

            adjustments.append({
                "dimension": dim,
                "name": DIMENSION_NAMES.get(dim, dim),
                "avg_correlation": round(avg_corr, 3),
                "signal": signal,
                "old_weight": old_w,
                "new_weight": new_weights[dim],
                "delta": round(new_weights[dim] - old_w, 3),
            })

        # RISK维度不变(扣分项)
        if "RISK" in current_weights:
            new_weights["RISK"] = current_weights["RISK"]

        # 归一化(不含RISK)
        non_risk_dims = [d for d in new_weights if d != "RISK"]
        total = sum(new_weights[d] for d in non_risk_dims)
        if total > 0:
            for d in non_risk_dims:
                new_weights[d] = round(new_weights[d] / total, 3)

        # 记录权重历史
        self.db["weight_history"].append({
            "timestamp": datetime.now().isoformat(),
            "calibration_count": len(cal_log),
            "old_weights": current_weights.copy(),
            "new_weights": new_weights.copy(),
            "adjustments": adjustments,
        })
        self.db["weights"] = new_weights
        self._save_db()

        weight_report = {
            "status": "adjusted",
            "calibration_count": len(cal_log),
            "adjustments": adjustments,
            "old_weights": current_weights,
            "new_weights": new_weights,
        }

        print(f"\n  🔧 权重修正完成:")
        for adj in adjustments:
            print(f"     {adj['dimension']}({adj['name']}): {adj['old_weight']:.3f}→{adj['new_weight']:.3f} "
                  f"({adj['delta']:+.3f}) [{adj['signal']}]")

        return weight_report

    # ═══ 辅助 ═══

    def _approx_correlation(self, xs: list, ys: list) -> float:
        """简化Pearson相关系数"""
        n = len(xs)
        if n < 3:
            return 0.0
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        std_x = (sum((x - mean_x) ** 2 for x in xs) / n) ** 0.5
        std_y = (sum((y - mean_y) ** 2 for y in ys) / n) ** 0.5
        if std_x == 0 or std_y == 0:
            return 0.0
        return cov / (n * std_x * std_y)

    def generate_report(self, calibration: dict) -> str:
        """生成人类可读的校准报告"""
        lines = []
        lines.append("═══ ☯️ Z9后验校准报告 ═══")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST")
        lines.append(f"目标回验: T+{calibration.get('target_days', '?')}")
        lines.append(f"实际数据: {calibration.get('actual_data_note', '?')}")
        lines.append("")

        # 1. 总体准确率
        lines.append("## 一、方向准确率")
        lines.append(f"| 指标 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 总预测数 | {calibration['total_predictions']} |")
        lines.append(f"| 方向正确 | {calibration['direction_accuracy']}% |")
        lines.append(f"| 高-低分组收益差 | {calibration['score_return_spread']:+.2f}% |")
        lines.append("")

        # 2. 按Action分类
        lines.append("## 二、按操作分类准确率")
        lines.append(f"| Action | 正确 | 总数 | 准确率 |")
        lines.append(f"|--------|------|------|--------|")
        for action, stats in sorted(calibration.get("action_accuracy", {}).items()):
            lines.append(f"| {action} | {stats['correct']} | {stats['total']} | {stats['accuracy']}% |")
        lines.append("")

        # 3. 维度预测力
        lines.append("## 三、评分维度预测力(与实际收益相关性)")
        dim_corrs = calibration.get("dimension_correlations", {})
        if dim_corrs:
            lines.append(f"| 维度 | 名称 | 相关性 | 信号 |")
            lines.append(f"|------|------|--------|------|")
            for dim, corr in sorted(dim_corrs.items(), key=lambda x: x[1], reverse=True):
                icon = "🟢" if corr > 0.10 else ("🟡" if corr > -0.10 else "🔴")
                lines.append(f"| {dim} | {DIMENSION_NAMES.get(dim, dim)} | {corr:+.3f} | {icon} |")
        lines.append("")

        # 4. 各标的详情
        lines.append("## 四、标的回验明细")
        details = calibration.get("ticker_details", [])
        if details:
            lines.append(f"| 代码 | 名称 | 预测日 | 预测价 | 现价 | 实际收益 | Action | 方向 |")
            lines.append(f"|------|------|--------|--------|------|----------|--------|------|")
            for e in sorted(details, key=lambda x: x["actual_return_pct"], reverse=True):
                dir_icon = "✅" if e["direction_correct"] else "❌"
                lines.append(
                    f"| {e['code']} | {e['name']} | {e['pred_date']} | "
                    f"{e['pred_price']:.2f} | {e['actual_price']:.2f} | "
                    f"{e['actual_return_pct']:+.2f}% | {e['predicted_action']} | {dir_icon} |"
                )
        lines.append("")

        # 5. 权重修正(如有)
        wa = calibration.get("weight_adjustment")
        if wa and wa.get("status") == "adjusted":
            lines.append("## 五、权重自适应修正 ⚡")
            lines.append(f"累计校准: {wa['calibration_count']}次")
            lines.append("")
            lines.append(f"| 维度 | 旧权重 | 新权重 | 变化 | 信号 |")
            lines.append(f"|------|--------|--------|------|------|")
            for adj in wa["adjustments"]:
                lines.append(
                    f"| {adj['dimension']}({adj['name']}) | "
                    f"{adj['old_weight']:.3f} | {adj['new_weight']:.3f} | "
                    f"{adj['delta']:+.3f} | {adj['signal']} |"
                )
            lines.append("")

        # 6. 天师解读
        lines.append("## 六、天师解读 ☯️")
        lines.append(self._generate_interpretation(calibration))

        return "\n".join(lines)

    def _generate_interpretation(self, cal: dict) -> str:
        """生成天师风格的三段解读"""
        acc = cal.get("direction_accuracy", 0)
        spread = cal.get("score_return_spread", 0)
        dim_corrs = cal.get("dimension_correlations", {})

        parts = []

        # 段落1: 方向准确率解读
        if acc >= 70:
            parts.append(f"**整体评定**: 方向准确率{acc:.1f}%, 处于合理区间。")
            parts.append(f"评分系统对标的的方向判定具备统计显著性, 但需关注具体的误判模式。")
        elif acc >= 50:
            parts.append(f"**整体评定**: 方向准确率{acc:.1f}%, 处于边缘区间。")
            parts.append(f"评分系统有一定预测力但噪声较大, 建议结合L3交叉验证和TruthGate二次确认。")
        else:
            parts.append(f"**整体评定**: ⚠️ 方向准确率{acc:.1f}%, 低于随机水平。")
            parts.append(f"评分系统可能对当前市场环境不适应。建议暂停自动决策, 回退到手工研判。")

        # 段落2: 收益差解读
        parts.append("")
        if spread > 2:
            parts.append(f"**评分区分度**: 高分组-低分组收益差{spread:+.2f}%, 正分离——")
            parts.append(f"说明评分系统能有效区分强势标的与弱势标的, 总分排位有参考价值。")
        elif spread > -2:
            parts.append(f"**评分区分度**: 高-低分组收益差{spread:+.2f}%, 区分度不足。")
            parts.append(f"当前评分对各标的的区分能力弱, 总分绝对值参考价值有限。")
            parts.append(f"建议: 更关注单个标的的内部评分结构而非排位。")
        else:
            parts.append(f"**评分区分度**: ⚠️ 高-低分组收益差{spread:+.2f}%, 倒挂！")
            parts.append(f"高评分标的反而跑输低评分标的——这是最危险的信号。")
            parts.append(f"可能原因: (1)评分过度拟合历史数据 (2)市场风格切换 (3)踩中了前夜宏观雷。")
            parts.append(f"紧急建议: 暂停依赖总分排序, 回归基本面逐票研判。")

        # 段落3: 维度分析
        parts.append("")
        if dim_corrs:
            strong_dims = [(d, c) for d, c in dim_corrs.items() if c > 0.10]
            weak_dims = [(d, c) for d, c in dim_corrs.items() if c < -0.10]
            if strong_dims:
                strong_names = ", ".join(f"{d}({c:+.2f})" for d, c in strong_dims)
                parts.append(f"**正向维度**: {strong_names} 与后续收益正相关。这些维度在当下市场是有效的选股信号。")
            if weak_dims:
                weak_names = ", ".join(f"{d}({c:+.2f})" for d, c in weak_dims)
                parts.append(f"**反向/弱维度**: {weak_names} 与后续收益负相关。这些维度可能在当下市场构成误导。")
                parts.append(f"建议: 降低负相关维度的权重, 或在选股时将这些维度作为反向过滤器。")
            if not strong_dims and not weak_dims:
                parts.append(f"**维度分析**: 各维度与后续收益相关性均弱, 当前市场无单一信号维度突出。")
                parts.append(f"这通常出现在:(1)政策市/情绪市 (2)财报空窗期 (3)宏观不确定性极高时。")

        # 段落4: 数据时效警告
        parts.append("")
        actual_days = min((e.get("actual_days", 5) for e in cal.get("ticker_details", [{"actual_days": 5}])), default=5)
        target_days = cal.get("target_days", 5)
        if actual_days < target_days:
            parts.append(f"⚠️ **数据时效**: 实际使用T+{actual_days}数据, 未达到T+{target_days}目标。")
            parts.append(f"T+{target_days}完整回验需等待至预测日+{target_days}个自然日后。")
            parts.append(f"当前报告为部分回验(preliminary), 建议在T+{target_days}时重新运行以获得完整结果。")

        return "\n".join(parts)


# ═══ CLI ═══
if __name__ == "__main__":
    engine = Z9CalibrationEngine()

    # 解析参数
    days = 5
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print(f"用法: python3 Z9_Calibration_Engine.py [days=5] [--live-prices=FILE]")
            sys.exit(1)

    # 可选: 从文件加载价格快照(替代API)
    live_prices = None
    for arg in sys.argv:
        if arg.startswith("--live-prices="):
            price_file = arg.split("=", 1)[1]
            with open(price_file) as f:
                live_prices = json.load(f)
            print(f"  📂 从文件加载价格: {price_file}")

    print(f"☯️ Z9 Calibration Engine v1.0")
    print(f"  目标: T+{days} 回验 | 累计校准: {len(engine.db['calibration_log'])}次")
    print()

    calibration = engine.backtest_at(days=days, live_prices=live_prices)

    if "error" in calibration:
        print(f"\n❌ 回验失败: {calibration['error']}")
        sys.exit(1)

    # 生成并保存报告
    report = engine.generate_report(calibration)
    print("\n" + report)

    # 落盘
    report_date = datetime.now().strftime("%Y-%m-%d")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{report_date}_Z9校准报告_T+{days}.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"\n📁 报告已落盘: {report_path}")
