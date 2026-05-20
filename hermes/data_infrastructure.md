# 📡 Z2 数据采集架构 v4.0 — Tushare主源 + 多通道灾备

> **升级**: 2026-05-19 01:55 | **原因**: Tushare升级至2000积分, 7接口全通  
> **架构**: Tushare首选 → 其他通道灾备降级  
> **前版**: v3.0 (腾讯/Sina/baostock并列)

---

## 一、数据源优先级

```
Tier 1 (首选): Tushare Pro 2000pt — 统一SDK, 7接口, 日限额充足
Tier 2 (灾备): 原有通道 — 仅Tushare不可用时激活
Tier 3 (实时): Broker/Exchange — 仅执行价
```

## 二、每层映射

### 实时行情
```yaml
首选: 腾讯API (不可替代 — Tushare无实时推送)
灾备: 新浪API
说明: 实时行情层不能用Tushare替代(daily_basic是日终数据)
```

### 历史K线 + 估值
```yaml
首选: Tushare daily + daily_basic (PE/PB/换手/量比)
灾备: baostock (前复权K线)
说明: daily_basic日终数据覆盖VSS+FQS需求
```

### 财务数据
```yaml
首选: Tushare income + fina_indicator (营收/净利/扣非/ROE/毛利率)
灾备: 公开财报 web_fetch
说明: FQS从手动逐个拉→5秒自动化, DQ从70→85+
```

### 资金流向
```yaml
首选: Tushare moneyflow (主力/大单/小单净流入) + margin (融资融券)
灾备: 腾讯API量比换手 (CFS近似)
说明: CFS精度从65%→85%, 最大缺口关闭
```

### 筹码/股东
```yaml
首选: Tushare stk_holdernumber (股东人数, 73条历史)
灾备: 东方财富 push2his (间歇, IP反爬)
说明: D-Matrix Micro因子数据源补齐
```

### 机构持仓
```yaml
首选: Tushare top_inst (需trade_date参数)
灾备: 东方财富龙虎榜网页
说明: CFS龙虎榜(10%权重)补齐
```

### 研报/催化
```yaml
首选: tavily_extract + web_search (不可替代)
说明: 非结构化数据, Tushare不覆盖
```

---

## 三、Tushare接口清单 (2000积分)

| 接口 | 频率 | 字段 | 覆盖模块 |
|------|:--:|------|------|
| daily | 日 | 日K线 | 历史收益, 3/5/20日RS |
| daily_basic | 日 | PE/PB/换手/量比/总市值 | VSS估值安全边际 |
| moneyflow | 日 | 主力/大单/中单/小单净流入 | CFS资金强度 |
| income | 季 | 营收/净利/扣非 | FQS财务质量 |
| fina_indicator | 季 | ROE/毛利率/净利率/EPS | FQS子维度 |
| margin | 日 | 融资余额/融资买入/融券 | CFS融资变化(5%) |
| stk_holdernumber | 季 | 股东人数 | D-Matrix Micro因子 |

---

## 四、灾备切换逻辑

```yaml
fallback_rules:
  tushare_unavailable:
    daily: baostock
    daily_basic: 腾讯API (PE/PB/换手)
    moneyflow: 腾讯API量比换手 (CFS降级)
    income: 公开财报 web_fetch
    fina_indicator: 公开财报 web_fetch
    margin: 不可用 (CFS降权)
    stk_holdernumber: 不可用 (D-Matrix Micro丢失)

  tushare_available:
    所有灾备通道仅作交叉验证, 不替代主源
```

---

## 五、数据采集管线更新

```
collect_market_data:
  实时: 腾讯API (不可替)
  K线+估值: Tushare daily+daily_basic → baostock灾备

collect_financial_data:
  Q1财报: Tushare income+fina_indicator → web_fetch灾备
  净利润增速/扣非增速: 自动计算

collect_flow_and_catalyst:
  资金流: Tushare moneyflow+margin → 腾讯API量比灾备
  筹码: Tushare stk_holdernumber → 无灾备
  催化: web_search+tavily_extract (不可替)
```

---

**签章**: Z2数据采集架构 v4.0 | Tushare 2000pt首选
