"""Compatibility shim for V4.0 smoke gates — logic migrated to zc40/zc45/zc35/strategy."""
from zmatrix.zc40.limit_board_fillability import LimitBoardFillabilityGate
from zmatrix.zc45.proxy_hedge_stress import ProxyHedgeStressTest
from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
from zmatrix.strategy.multi_strategy_sleeve import MultiStrategySleeve
__all__ = ["LimitBoardFillabilityGate","ProxyHedgeStressTest","CatalystLifecycleEngine","MultiStrategySleeve"]
