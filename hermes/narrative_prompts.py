"""
Z2天师 Hermes — 叙事分析 Prompt 模板
Z2天师自己提取, 不依赖外部模型
"""

NARRATIVE_ANALYSIS_PROMPT = """你是A股市场叙事分析师。请分析以下从多个渠道采集的文本片段，提取市场情绪和叙事状态。

## 输入文本
{sources_text}

## 分析要求

对以下5个维度进行量化分析，输出严格JSON格式：

1. **slogan_repetition_ratio** (0.0-1.0)
   - 相同口号/套话/短语在文本中的重复比例
   - 高值 (≥0.7): "涨停""龙头""妖股""十倍股""起飞""梭哈"等词汇频繁出现
   - 低值 (≤0.3): 讨论分散，无统一口号
   - 举例: 50条文本中"龙头"出现30次 → 0.6

2. **marginal_buyer_exhaustion** (0.0-1.0) 
   - 新增参与者是否在减少，最后一波买家是否已进场
   - 高值 (≥0.6): "我已经满仓了""还能涨吗""不敢追""太高了"
   - 低值 (≤0.3): "刚刚发现""正在研究""还没上车""准备入"

3. **narrative_diversity** (0.0-1.0)
   - 有多少个不同叙事/话题在争夺注意力
   - 0=单一叙事 (极危险，所有人都挤在一个故事里)
   - 1=百花齐放 (健康，多个方向都有讨论)

4. **narrative_acceleration** (-1.0 ~ 1.0)
   - 叙事是在加速传播还是减速
   - 正值: 越来越多人在讨论，传播在加速
   - 负值: 热度在消退，人们转向其他话题
   - 0=稳定

5. **dominant_emotion**
   - "greed": 贪婪，怕错过 (FOMO)
   - "fear": 恐惧，怕崩盘
   - "neutral": 中性，理性讨论
   - "confused": 困惑，方向不明

## 输出格式

```json
{{
  "slogan_repetition_ratio": 0.0,
  "marginal_buyer_exhaustion": 0.0,
  "narrative_diversity": 0.0,
  "narrative_acceleration": 0.0,
  "dominant_emotion": "neutral",
  "top_narratives": ["叙事1", "叙事2", "叙事3"],
  "summary": "一句话总结当前市场情绪状态"
}}
```

只输出这个JSON，不要额外解释。
"""


NARRATIVE_CROSS_SESSION_PROMPT = """你是A股叙事分析师。对比两次扫描结果，判断叙事方向变化。

## 前次扫描 ({prev_time})
{prev_summary}

## 当前扫描 ({curr_time})
{curr_summary}

## 输出
```json
{{
  "direction": "accelerating" | "decelerating" | "stable" | "reversing",
  "delta_slogan": 0.0,
  "delta_exhaustion": 0.0,
  "delta_diversity": 0.0,
  "regime_change": true | false,
  "alert": "NONE" | "MANIA_BUILDING" | "CAPITULATION_FORMING" | "NARRATIVE_COLLAPSE"
}}
```
"""
