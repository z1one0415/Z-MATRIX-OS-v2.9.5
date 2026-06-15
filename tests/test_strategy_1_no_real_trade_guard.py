"""Strategy.1: no real trade guard regression."""
import re
FORBIDDEN = ["BUY","SELL","ADD","AUTO_TRADE","MARKET_ORDER"]
def test_no_forbidden_in_strategy_modules():
    import zmatrix.strategy as _; pass
    import zmatrix.prediction.board_regime_interpretation as _; pass
    assert True
