"""
Z-MATRIX 三维角色评分矩阵 V2.0

v2.9.4: 模块正在逐步迁移, __init__.py使用防御性导入。
"""

# B-Matrix v2.1.1
try:
    from .b_matrix import BMatrixInput, BMatrixResult, evaluate_b_matrix
except ImportError:
    pass

# R-Matrix v1.1
try:
    from .r_matrix import OscillationKingResult, rank_type_b_rising_channel, OscillationType
except ImportError:
    pass

# D-Matrix v2.2
try:
    from .d_band import evaluate_d_early_v22
except ImportError:
    pass
