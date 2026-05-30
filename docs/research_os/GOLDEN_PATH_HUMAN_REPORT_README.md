# Golden Path Human Report — Reader's Guide

## What This Is

The Human Report adapter translates machine research output into human-readable Chinese. It does NOT re-score, re-decision, or generate trading advice.

## 8-Section Structure

| Section | Content | Source |
|---------|---------|--------|
| 一、研究对象 | Ticker, industry, benchmark, period | Idea stage |
| 二、一句话结论 | Observe/Continue/Wait (no BUY/SELL) | Council verdict |
| 三、为什么判断 | 3-5 evidence items | Factor IC + Council votes |
| 四、收益来源分析 | Market vs Industry vs Selection alpha | Attribution Engine |
| 五、主要风险 | Risk flags from Council + Devil | Council minority |
| 六、反方意见 | Mandatory counter-argument | Devil Advocate |
| 七、建议动作 | Observe/Track/Re-evaluate only | Council status |
| 八、审计信息 | Audit hash + version + disclaimer | System metadata |

## Safety Statement

This report is **research-only**. It does not constitute investment advice. Production, broker, runtime, and real trade execution are permanently blocked.

## Important Notes

- The adapter reuses existing modules; it does NOT re-compute anything
- The adapter does NOT add new research capabilities
- The adapter does NOT generate BUY/SELL/AUTO_EXECUTE instructions
- Architecture freeze is maintained (160 modules unchanged)
