"""ROC-HR1: Golden Path Human Report Adapter — reads from _case metadata."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = WORKSPACE / "runtime_reports" / "golden_path"


def generate_human_report(golden_path_result: dict) -> str:
    """Generate a human-readable Chinese research report from the Golden Path result.

    Now reads ticker/name/industry/sector/chain from _case metadata (V2 parameterization).
    """
    case = golden_path_result.get("_case", {})
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ticker = case.get("ticker", golden_path_result.get("idea", {}).get("ticker", "600519"))
    name = case.get("name", ticker)
    industry = case.get("industry", "UNKNOWN")
    sector = case.get("sector", "")
    chain_name = case.get("chain", "")
    benchmark = case.get("benchmark_id", "CSI300")
    start = case.get("start_date", golden_path_result.get("idea", {}).get("start_date", "2024-01-02"))
    end = golden_path_result.get("outcome", {}).get("exit_date", "2024-01-30")

    audit = golden_path_result.get("_audit_hash", "N/A")
    council = golden_path_result.get("council", {})
    attribution = golden_path_result.get("attribution", {})
    outcome = golden_path_result.get("outcome", {})
    factor = golden_path_result.get("factor", {})
    memory = golden_path_result.get("memory", {})

    lines = [
        f"# 研究报告：{name} ({ticker})",
        f"",
        f"**研究时间**：{now}",
        f"**数据来源**：Research OS V3 Golden Path (parameterized)",
        f"**审计哈希**：`{audit}`",
        f"",
        f"---",
        f"",
        f"## 一、研究对象",
        f"",
        f"- **股票**：{name}（{ticker}）",
        f"- **行业**：{industry}",
        f"- **板块**：{sector}",
        f"- **产业链**：{chain_name}",
        f"- **基准**：{benchmark}",
        f"- **研究周期**：{start} → {end}",
        f"",
        f"## 二、一句话结论",
        f"",
    ]

    status = council.get("status", "INSUFFICIENT_EVIDENCE")
    if status == "PASS":
        lines.append("**进入观察池** — 因子通过验证，Council多数支持，建议持续跟踪。")
    elif status == "FAIL":
        lines.append("**暂不进入候选池** — 关键指标未达标或Council反对意见较多。")
    else:
        lines.append("**研究证据不足** — 当前数据不足以形成明确判断，需补充验证。")

    lines.extend([
        f"", f"## 三、为什么这样判断", f"",
    ])
    ic = factor.get("ic", 0)
    if abs(ic) >= 0.03: lines.append(f"- **因子IC={ic:.3f}**，超过最低门槛，具有统计显著性")
    elif abs(ic) >= 0.01: lines.append(f"- **因子IC={ic:.3f}**，处于边缘区域")
    else: lines.append(f"- **因子IC={ic:.3f}**，未达到有效阈值")
    if outcome.get("ready"): lines.append(f"- **T20 Outcome就绪**，出场日={outcome.get('exit_date')}")
    pass_count = council.get("pass", 0); fail_count = council.get("fail", 0)
    lines.append(f"- **Council审议**：{pass_count}票通过 / {fail_count}票反对，平均评分={council.get('avg_score', 0):.2f}")
    minority = council.get("minority_count", 0)
    if minority > 0: lines.append(f"- **少数意见**：{minority}位评审员持保留意见（已记录）")

    lines.extend([
        f"", f"## 四、收益来源分析", f"",
        f"- 总收益：{attribution.get('gross_return', 0):.1%}",
        f"- 市场贡献：{attribution.get('market_contribution', 0):.1%}",
        f"- 选股Alpha：{attribution.get('selection_alpha', 0):.1%}",
        f"", f"## 五、主要风险", f"",
    ])
    risks = []
    if minority > 0: risks.append(f"- **Council分歧**：{minority}位评审员持反对意见")
    if abs(ic) < 0.03: risks.append(f"- **因子强度不足**：IC={ic:.3f}低于理想阈值")
    if memory.get("lesson_category") == "UNCLEAR_EDGE": risks.append(f"- **收益驱动不明确**")
    lines.extend(risks if risks else ["- 当前未检测到重大风险信号"])

    lines.extend([
        f"", f"## 六、反方意见", f"",
        f"- **Devil Advocate（反方审查）**：已强制执行",
        f"- 少数派意见：已保留在Council记录中",
        f"", f"## 七、建议动作", f"",
    ])
    if status == "PASS" and abs(ic) >= 0.03: lines.append("- 📋 **进入候选池**，建议持续观察T20/T60 Outcome")
    elif status == "PASS": lines.append("- 👀 **继续观察**，等待因子IC稳定后再评估")
    else: lines.append("- 📊 **补充数据**，当前证据不足")

    lines.extend([
        f"", f"## 八、审计信息", f"",
        f"| 项目 | 值 |", f"|------|-----|",
        f"| Audit Hash | `{audit}` |", f"| 架构状态 | ARCHITECTURE_FREEZE |",
        f"", f"---", f"",
        f"**⚠️ 免责声明**",
        f"- 本报告由 Research OS V3 自动生成",
        f"- **仅供研究参考，不构成投资建议**",
        f"- Production: BLOCKED | Broker: BLOCKED | Runtime: BLOCKED",
    ])
    return "\n".join(lines)


def save_human_report(golden_path_result: dict) -> str:
    """Generate and save the human report with case-specific path."""
    case = golden_path_result.get("_case", {})
    case_id = case.get("case_id", "UNKNOWN")
    ticker = case.get("ticker", "UNKNOWN")
    out_dir = WORKSPACE / "runtime_reports" / "cases" / "core_12" / f"{case_id}_{ticker}"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = generate_human_report(golden_path_result)
    path = out_dir / f"{case_id}_{ticker}_human_report.md"
    path.write_text(report)
    return str(path)
