from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .contracts import GhostBenchmark, new_id


# 产业链级幽灵基准映射 (优先级 > 角色默认)
CHAIN_BENCHMARKS: Dict[str, GhostBenchmark] = {
    "AI算力":     GhostBenchmark(new_id("bp"), "512480.SH", "半导体ETF",    "AI算力链默认对比半导体基准"),
    "机器人":     GhostBenchmark(new_id("bp"), "562500.SH", "机器人ETF",    "机器人链默认对比机器人板块基准"),
    "半导体":     GhostBenchmark(new_id("bp"), "512480.SH", "半导体ETF",    "半导体链默认对比半导体基准"),
    "资源周期":   GhostBenchmark(new_id("bp"), "512400.SH", "有色金属ETF",  "资源链默认对比有色基准"),
    "消费":       GhostBenchmark(new_id("bp"), "159928.SZ", "消费ETF",      "消费链默认对比消费板块基准"),
    "新能源":     GhostBenchmark(new_id("bp"), "516160.SH", "新能源ETF",    "新能源链默认对比新能源基准"),
    "军工":       GhostBenchmark(new_id("bp"), "512660.SH", "军工ETF",      "军工链默认对比军工板块基准"),
    "医药":       GhostBenchmark(new_id("bp"), "512010.SH", "医药ETF",      "医药链默认对比医药板块基准"),
    "金融地产":   GhostBenchmark(new_id("bp"), "510230.SH", "金融ETF",      "金融链默认对比金融板块基准"),
    "消费电子":   GhostBenchmark(new_id("bp"), "159732.SZ", "消费电子ETF",  "消费电子链默认对比板块基准"),
}

# 角色级默认基准 (fallback, 产业链不匹配时使用)
ROLE_BENCHMARKS: Dict[str, GhostBenchmark] = {
    "B_MATRIX": GhostBenchmark(new_id("bp"), "000300.SH", "沪深300", "底仓默认对比宽基质量/大盘基准"),
    "R_MATRIX": GhostBenchmark(new_id("bp"), "399905.SZ", "中证500", "轮动默认对比中盘机会基准"),
    "D_MATRIX": GhostBenchmark(new_id("bp"), "399006.SZ", "创业板指", "黑马/高弹性默认对比成长风险基准"),
    "OSCILLATION_KING": GhostBenchmark(new_id("bp"), "399905.SZ", "中证500", "波动王默认对比中盘波动基准"),
}


@dataclass
class BenchmarkBindingRequest:
    primary_role: str
    explicit_symbol: Optional[str] = None
    explicit_name: Optional[str] = None
    reason: Optional[str] = None
    sector: Optional[str] = None
    chain: Optional[str] = None


class GhostBenchmarkBinder:
    def bind(self, req: BenchmarkBindingRequest) -> GhostBenchmark:
        # 优先级: 显式指定 > 产业链匹配 > 角色匹配 > fallback
        if req.explicit_symbol:
            return GhostBenchmark(
                benchmark_pair_id=new_id("bp"),
                symbol=req.explicit_symbol,
                name=req.explicit_name or req.explicit_symbol,
                reason=req.reason or "用户显式指定幽灵基准",
            )
        
        # 产业链匹配 (优先级高于角色)
        chain = (req.chain or "").strip()
        for chain_key, benchmark in CHAIN_BENCHMARKS.items():
            if chain_key in chain:
                return GhostBenchmark(
                    benchmark_pair_id=new_id("bp"),
                    symbol=benchmark.symbol,
                    name=benchmark.name,
                    reason=req.reason or f"产业链={chain_key} 自动绑定幽灵基准 {benchmark.name}",
                    benchmark_type=benchmark.benchmark_type,
                )
        
        # 角色匹配 (fallback)
        role = (req.primary_role or "").upper()
        base = ROLE_BENCHMARKS.get(role) or ROLE_BENCHMARKS["R_MATRIX"]
        return GhostBenchmark(
            benchmark_pair_id=new_id("bp"),
            symbol=base.symbol,
            name=base.name,
            reason=req.reason or f"角色={role or 'UNKNOWN'} 自动绑定幽灵基准 {base.name}",
            benchmark_type=base.benchmark_type,
        )


def simple_return(current_price: float, entry_price: float) -> float:
    if entry_price <= 0:
        raise ValueError("entry_price must be positive")
    return current_price / entry_price - 1.0
