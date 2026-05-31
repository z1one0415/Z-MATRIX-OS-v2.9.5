import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
FORBIDDEN = ["BUY", "SELL", "ADD", "REDUCE", "PLACE_ORDER", "SEND_ORDER", "AUTO_EXECUTE",
             "alpha_validated", "stock_has_alpha", "predictive_alpha=True",
             "suggested_position", "target_price", "stop_loss"]
CASES = W / "runtime_reports" / "cases"
def test_no_forbidden_in_any_json():
    for jf in ["core_12_real_returns.json", "csi300_benchmark_returns.json",
               "core_12_benchmark_relative_returns.json", "v5_core12_real_return_packet.json"]:
        fp = CASES / jf
        if not fp.exists(): continue
        text = fp.read_text()
        for word in FORBIDDEN:
            assert word not in text, f"{jf} contains forbidden: {word}"
def test_no_investment_recommendations():
    for jf in CASES.glob("v5_*.json"):
        text = jf.read_text()
        assert "建议买入" not in text
        assert "建议卖出" not in text
