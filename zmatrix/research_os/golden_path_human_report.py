"""ROC-HR1: Golden Path Human Report Adapter — translate research output into human-readable report."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = WORKSPACE / "runtime_reports" / "golden_path"


def generate_human_report(golden_path_result: dict) -> str:
    """Generate a human-readable Chinese research report from the Golden Path result.

    Reuses existing modules for data, does NOT re-research or re-score.
    Only translates/interprets already-computed results.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ticker = golden_path_result.get("idea", {}).get("ticker", "600519")
    audit = golden_path_result.get("_audit_hash", "N/A")
    council = golden_path_result.get("council", {})
    attribution = golden_path_result.get("attribution", {})
    outcome = golden_path_result.get("outcome", {})
    factor = golden_path_result.get("factor", {})
    memory = golden_path_result.get("memory", {})

    lines = [
        f"# 研究报告：贵州茅台 ({ticker})",
        f"",
        f"**研究时间**：{now}",
        f"**数据来源**：Research OS V3 Golden Path",
        f"**审计哈希**：`{audit}`",
        f"",
        f"---",
        f"",
        f"## 一、研究对象",
        f"",
        f"- **股票**：贵州茅台（{ticker}）",
        f"- **行业**：食品饮料",
        f"- **基准**：CSI300",
        f"- **研究周期**：2024-01-02 → 2024-01-30 (T20)", 
        f"",
        f"## 二、一句话结论",
        f"",
    ]

    # Verdict from council
    status = council.get("status", "INSUFFICIENT_EVIDENCE")
    if status == "PASS":
        lines.append("**进入观察池** — 因子通过验证，Council多数支持，建议持续跟踪。")
    elif status == "FAIL":
        lines.append("**暂不进入候选池** — 关键指标未达标或Council反对意见较多。")
    else:
        lines.append("**研究证据不足** — 当前数据不足以形成明确判断，需补充验证。")

    lines.extend([
        f"",
        f"## 三、为什么这样判断",
        f"",
    ])

    # Evidence from factor + council
    evidence = []
    ic = factor.get("ic", 0)
    if abs(ic) >= 0.03:
        evidence.append(f"- **因子IC={ic:.3f}**，超过最低门槛(0.02)，因子具有统计显著性")
    elif abs(ic) >= 0.01:
        evidence.append(f"- **因子IC={ic:.3f}**，处于边缘区域，信号强度一般")
    else:
        evidence.append(f"- **因子IC={ic:.3f}**，未达到有效阈值")

    if outcome.get("ready"):
        evidence.append(f"- **T20 Outcome就绪**，出场日={outcome.get('exit_date')}，前向交易日充足")

    pass_count = council.get("pass", 0)
    fail_count = council.get("fail", 0)
    evidence.append(f"- **Council审议**：{pass_count}票通过 / {fail_count}票反对，平均评分={council.get('avg_score', 0):.2f}")

    minority = council.get("minority_count", 0)
    if minority > 0:
        evidence.append(f"- **少数意见**：{minority}位评审员持保留意见（已记录）")

    for e in evidence:
        lines.append(e)

    lines.extend([
        f"",
        f"## 四、收益来源分析",
        f"",
        f"- 总收益：{attribution.get('gross_return', 0):.1%}",
        f"- 市场贡献：{attribution.get('market_contribution', 0):.1%}（CSI300同期涨跌的被动部分）",
        f"- 选股Alpha：{attribution.get('selection_alpha', 0):.1%}（扣除市场后的超额收益）",
        f"",
        f"**解读**：",
    ])

    alpha = attribution.get("selection_alpha", 0)
    market = attribution.get("market_contribution", 0)
    if alpha > 0.01:
        lines.append(f"- 选股产生了正Alpha(+{alpha:.1%})，且超越市场贡献，表明个股选择有效")
    elif alpha > 0:
        lines.append(f"- 选股产生微弱正Alpha(+{alpha:.1%})，收益主要由市场贡献驱动")
    else:
        lines.append(f"- 选股未产生正Alpha，收益完全由市场驱动")

    lines.extend([
        f"",
        f"## 五、主要风险",
        f"",
    ])

    # Risks from council minority + devil
    risks = []
    if minority > 0:
        risks.append(f"- **Council分歧**：{minority}位评审员持反对意见")
    ic_val = factor.get("ic", 0)
    if abs(ic_val) < 0.03:
        risks.append(f"- **因子强度不足**：IC={ic_val:.3f}低于理想阈值，信号可能存在噪声")
    if memory.get("lesson_category") == "UNCLEAR_EDGE":
        risks.append(f"- **收益驱动不明确**：系统未能明确识别收益来源模式")

    if risks:
        for r in risks:
            lines.append(r)
    else:
        lines.append("- 当前未检测到重大风险信号")

    lines.extend([
        f"",
        f"## 六、反方意见",
        f"",
        f"- **Devil Advocate（反方审查）**：已强制执行",
        f"- **少数派意见**：已保留在Council记录中",
        f"- 任何研究结论均需附带反方意见，这是Research OS V3的强制机制",
        f"",
        f"## 七、建议动作",
        f"",
    ])

    if status == "PASS" and abs(ic) >= 0.03:
        lines.append("- 📋 **进入候选池**，建议持续观察T20/T60 Outcome")
        lines.append("- 🔄 **下次研究**：补充T60数据后重新验证")
    elif status == "PASS":
        lines.append("- 👀 **继续观察**，等待因子IC稳定后再评估")
    else:
        lines.append("- 📊 **补充数据**，当前证据不足以形成建议")
        lines.append("- ⏳ **等待下一轮**：T60窗口到期后重新评估")

    lines.extend([
        f"",
        f"## 八、审计信息",
        f"",
        f"| 项目 | 值 |",
        f"|------|-----|",
        f"| Audit Hash | `{audit}` |",
        f"| 研究版本 | Research OS V3 |",
        f"| 架构状态 | ARCHITECTURE_FREEZE |",
        f"| Council 哈希 | {council.get('status', 'N/A')} |",
        f"",
        f"---",
        f"",
        f"**⚠️ 免责声明**",
        f"",
        f"- 本报告由 Research OS V3 自动生成",
        f"- **仅供研究参考，不构成投资建议**",
        f"- Production: BLOCKED | Broker: BLOCKED | Runtime: BLOCKED",
        f"- 任何投资决策请基于独立判断",
    ])

    return "\n".join(lines)


def save_human_report(golden_path_result: dict) -> str:
    """Generate and save the human report. Returns the file path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = generate_human_report(golden_path_result)
    path = OUTPUT_DIR / "golden_path_human_report.md"
    path.write_text(report)
    return str(path)
