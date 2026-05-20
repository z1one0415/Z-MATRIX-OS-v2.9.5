from __future__ import annotations

from .contracts import AlphaValidationPosition, MarkToMarketSnapshot
from .ghost_benchmark import simple_return


class MarkToMarketEngine:
    def mark(self, position: AlphaValidationPosition, mark_date: str, symbol_price: float, benchmark_price: float,
             system_verdict: str | None = None, underperform_threshold: float = -0.03) -> MarkToMarketSnapshot:
        if symbol_price <= 0 or benchmark_price <= 0:
            raise ValueError("mark prices must be positive")
        stock_ret = simple_return(symbol_price, position.entry_price)
        bench_ret = simple_return(benchmark_price, position.entry_benchmark_price)
        active = stock_ret - bench_ret
        max_adverse = min(position.max_adverse_return, stock_ret)
        max_favorable = max(position.max_favorable_return, stock_ret)
        triggers = []
        if stock_ret <= position.max_acceptable_drawdown:
            triggers.append("max_acceptable_drawdown_breached")
        if active <= underperform_threshold:
            triggers.append("benchmark_underperform_threshold")
        if system_verdict in {"BLOCK", "SYSTEM_BLOCKED", "DATA_INVALID"}:
            triggers.append("system_blocked_or_data_invalid")
        return MarkToMarketSnapshot(
            validation_id=position.validation_id,
            mark_date=mark_date,
            symbol_price=symbol_price,
            benchmark_price=benchmark_price,
            stock_return=round(stock_ret, 6),
            benchmark_return=round(bench_ret, 6),
            active_return=round(active, 6),
            max_adverse_return=round(max_adverse, 6),
            max_favorable_return=round(max_favorable, 6),
            triggered_conditions=triggers,
            system_verdict=system_verdict,
        )

    def apply_mark_to_position(self, position: AlphaValidationPosition, snapshot: MarkToMarketSnapshot) -> AlphaValidationPosition:
        position.max_adverse_return = snapshot.max_adverse_return
        position.max_favorable_return = snapshot.max_favorable_return
        position.last_mark_date = snapshot.mark_date
        position.marks_count += 1
        return position
