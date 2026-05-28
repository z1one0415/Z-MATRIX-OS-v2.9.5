# Z-MATRIX-OS v4.0-FINAL-HARDGATES｜6 批次 OpenClaw 执行文件包

生成时间：2026-05-28T04:29:13

## 本版核心变化

本版在 ZC35 + ZC45 全局融合版基础上，正式吸收 G 提出的三个阿喀琉斯之踵，升级为 v4.0 上线前最终硬门：

```text
1. ZC40 LimitBoardFillabilityGate
   解决一字板、连续涨停、涨停后开板接力不可成交 / 追高接盘问题。

2. ZC45 ProxyHedgeStressTest
   解决代理对冲在极端流动性危机下相关性崩塌、伪中性化问题。

3. Runtime LLMProviderFailoverPolicy + OfflineDegradedMode
   解决 LLM/API 宕机、限流、网络失败时系统胡编或崩溃问题。
```

## 6 批次结构

1. Batch 0：Baseline Freeze + Final Hard Gates Scope Lock
2. Batch 1：Architecture + Contracts + Parser-Scorer + Failover Runtime
3. Batch 2：Research Council + Report Library + Hard Gates Report Blocks
4. Batch 3：DataForge + FactorFactory + ZC35 + ZC45 + ProxyHedgeStressTest + MultiStrategy
5. Batch 4：ExecutionQuality + AccountGovernance + LimitBoard + Catalyst/Beta Integration
6. Batch 5：System Cockpit + Audit + IRF + Final Hard Gates + v4.0-RC1

## 五条必须全部通过的验证线

```bash
bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

Batch 5 额外：

```bash
bash scripts/verify_v40_full_upgrade.sh
```

## 不可破坏的硬边界

```text
No real trade
No broker order
No auto buy
No auto sell
No LLM subjective float score
No catalyst direct buy/sell
No proxy hedge real execution
No market neutral claim
No limit-up auto buy
No fresh judgement during LLM/API failure
No production-ready regime candidate before v3.5.7 pass
```

## 一句话定位

```text
v4.0-FINAL-HARDGATES 是机构化投研与纸面执行工厂，不是自动交易机器。
```
