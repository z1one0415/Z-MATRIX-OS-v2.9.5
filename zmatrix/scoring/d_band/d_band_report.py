from __future__ import annotations

import json
from .d_band_contracts import DBandReport


def report_to_json(report: DBandReport, *, indent: int = 2) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=indent)


def report_to_markdown(report: DBandReport) -> str:
    d = report.to_dict()
    lines = [
        f"# D-Band v2.1 Report — {d['name']} {d['code']}",
        "",
        f"- 阶段：`{d['d_lifecycle_stage']}` / `{d['d_stage_variant']}`",
        f"- D-Early：`{d['d_early_score']}` / ceiling `{d['d_early_score_ceiling']}`",
        f"- 执行模式：`{d['execution_mode']}`",
        f"- 允许动作：`{d['allowed_action']}`",
        f"- 真实交易允许：`{d['real_trade_allowed']}`",
        "",
        "## 下一触发器",
    ]
    for item in d["next_triggers"]:
        lines.append(f"- {item}")
    lines.extend(["", "## 禁止动作"])
    for item in d["forbidden"]:
        lines.append(f"- {item}")
    lines.extend(["", "## 数据完整度", "```json", json.dumps(d["data_completeness"], ensure_ascii=False, indent=2), "```"])
    return "\n".join(lines) + "\n"
