"""ZC35 CatalystLifecycleEngine v2.0 — 测试套件

覆盖:
- v1.0 向后兼容 (classify)
- v2.0 催化分类学 (get_taxonomy)
- v2.0 残值计算 (compute_residual_power)
- v2.0 情绪阶段识别 (identify_sentiment_phase)
- v2.0 叠加效应 (compute_stack_effect)
- v2.0 完整分析 (full_lifecycle_analysis)
- v2.0 批量分析 (batch_analyze)
- 股票档案加载 (from stock_profiles JSON)
"""
from __future__ import annotations
import json
from pathlib import Path


def test_v1_classify_backward_compat():
    """ZC35 v1.0 classify接口向后兼容"""
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    engine = CatalystLifecycleEngine()

    # 无 publish_time
    result = engine.classify({})
    assert result["status"] == "DATA_INSUFFICIENT"
    assert result["real_trade_allowed"] is False

    # D级证据
    result = engine.classify({"publish_time": "2026-05-12", "evidence_level": "D"})
    assert result["lifecycle"] == "PRE_EVENT"
    assert result["action"] == "WATCH_ONLY"

    # 正常事件
    result = engine.classify({"publish_time": "2026-05-12", "evidence_level": "A"})
    assert result["lifecycle"] == "EVENT_ACTIVE"
    assert result["residual_power"] == 0.8


def test_v2_taxonomy():
    """催化分类学完整性"""
    from zmatrix.zc35.catalyst_lifecycle import CATALYST_TAXONOMY

    assert "S" in CATALYST_TAXONOMY
    assert "A" in CATALYST_TAXONOMY
    assert "B" in CATALYST_TAXONOMY
    assert "C" in CATALYST_TAXONOMY
    assert "D" in CATALYST_TAXONOMY

    s = CATALYST_TAXONOMY["S"]
    assert s["half_life_days"] == 7
    assert s["full_decay_days"] == 15
    assert s["tradeable"] is True

    d = CATALYST_TAXONOMY["D"]
    assert d["price_amplification"] < 0  # 负信号!
    assert d["tradeable"] is False


def test_v2_residual_power():
    """残值计算"""
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    engine = CatalystLifecycleEngine()

    # S级: D+0 = 0.8
    assert abs(engine.compute_residual_power("S", 0) - 0.8) < 0.01
    # S级: D+7 (half-life) = 0.5
    assert abs(engine.compute_residual_power("S", 7) - 0.5) < 0.01
    # S级: D+15 (full decay) = 0.0
    assert engine.compute_residual_power("S", 15) == 0.0
    # S级: D+30 = 0.0
    assert engine.compute_residual_power("S", 30) == 0.0

    # D级: 始终为负
    assert engine.compute_residual_power("D", 0) < 0
    assert engine.compute_residual_power("D", 5) < 0

    # A级: half_life=2, full_decay=5
    assert abs(engine.compute_residual_power("A", 0) - 0.55 * 0.8) < 0.01
    assert abs(engine.compute_residual_power("A", 2) - 0.55 * 0.5) < 0.01
    assert engine.compute_residual_power("A", 5) == 0.0


def test_v2_sentiment_phase():
    """情绪阶段识别"""
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    engine = CatalystLifecycleEngine()

    # S级催化
    assert engine.identify_sentiment_phase("S", -3) == "PRE_RUN"
    assert engine.identify_sentiment_phase("S", 0) == "EVENT_BURST"
    assert engine.identify_sentiment_phase("S", 5) == "CONTINUATION"
    assert engine.identify_sentiment_phase("S", 10) == "PLATEAU"
    assert engine.identify_sentiment_phase("S", 13) == "DECAY"
    assert engine.identify_sentiment_phase("S", 16) == "VACUUM"


def test_v2_stack_effect():
    """催化叠加效应"""
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    engine = CatalystLifecycleEngine()

    # 单催化
    single = engine.compute_stack_effect([
        {"level": "S", "days_since_event": 5, "name": "GD01"}
    ])
    assert single["stack_count"] == 1
    assert single["penalty_factor"] == 1.0

    # 双催化叠加 (S+A)
    double = engine.compute_stack_effect([
        {"level": "S", "days_since_event": 8, "name": "GD01"},
        {"level": "A", "days_since_event": 0, "name": "发改委"},
    ])
    assert double["stack_count"] == 2
    assert double["penalty_factor"] > 1.0
    assert double["warning"] is not None

    # 三催化叠加 → 应有警告
    triple = engine.compute_stack_effect([
        {"level": "S", "days_since_event": 8, "name": "GD01"},
        {"level": "A", "days_since_event": 0, "name": "发改委"},
        {"level": "C", "days_since_event": 1, "name": "Google IO"},
    ])
    assert triple["stack_count"] == 3
    assert triple["penalty_factor"] >= 1.5
    assert "加速催熟" in (triple.get("warning") or "")


def test_v2_full_analysis():
    """一站式分析"""
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    engine = CatalystLifecycleEngine()

    result = engine.full_lifecycle_analysis("S", 8, "宇树GD01")
    assert result["evidence_level"] == "S"
    assert result["lifecycle"] == "POST_EVENT_DECAY"
    assert result["sentiment_phase"] == "CONTINUATION"
    assert 0.3 < result["residual_power"] < 0.6
    assert result["tradeable"] is True


def test_v2_batch_analyze():
    """批量分析"""
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    engine = CatalystLifecycleEngine()

    result = engine.batch_analyze([
        {"level": "S", "days_since_event": 17, "name": "宇树GD01"},
        {"level": "A", "days_since_event": 7, "name": "发改委政策"},
    ])
    assert result["total_events"] == 2
    assert result["active_count"] <= 1  # 二者均已过期
    assert result["dominant_sentiment"] == "VACUUM"


def test_stock_profile_loading():
    """股票档案JSON加载"""
    profile_path = Path(__file__).parent.parent.parent / "data" / "stock_profiles" / "002472_双环传动_catalyst_profile.json"
    if not profile_path.exists():
        # 尝试从workspace路径
        profile_path = Path.home() / "Documents" / "Z-MATRIX-OS v2.9.5" / "data" / "stock_profiles" / "002472_双环传动_catalyst_profile.json"
    
    assert profile_path.exists(), f"股票档案不存在: {profile_path}"
    
    with open(profile_path) as f:
        profile = json.load(f)
    
    assert profile["ticker"] == "002472"
    assert len(profile["historical_catalysts"]) == 6
    assert len(profile["signal_matrix"]["true_positive"]) == 5
    assert len(profile["signal_matrix"]["false_positive"]) == 3
    assert profile["support_resistance_live"]["cost_broken"] is True
    assert profile["four_king_resonance_current"]["resonance_status"] == "CYCLE_RESONANCE_ENTRY"
