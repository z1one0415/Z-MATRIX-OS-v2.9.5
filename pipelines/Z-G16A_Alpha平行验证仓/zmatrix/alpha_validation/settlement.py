from __future__ import annotations

from datetime import datetime

from .contracts import AlphaValidationPosition, CloseReason, SettlementReport, ValidationVerdict
from .ghost_benchmark import simple_return


def _parse_date(s: str) -> datetime:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return datetime.fromisoformat(s[:10])


class SettlementEngine:
    def settle(self, position: AlphaValidationPosition, close_reason: str, exit_price: float,
               exit_benchmark_price: float, closed_at: str, hypothesis_adherence: bool = True,
               rule_changed_midway: bool = False, total_cost_drag: float | None = None) -> SettlementReport:
        if close_reason not in {x.value for x in CloseReason}:
            raise ValueError(f"invalid close_reason: {close_reason}")
        if exit_price <= 0 or exit_benchmark_price <= 0:
            raise ValueError("exit prices must be positive")
        stock_ret = simple_return(exit_price, position.entry_price)
        bench_ret = simple_return(exit_benchmark_price, position.entry_benchmark_price)
        active = stock_ret - bench_ret
        costs = total_cost_drag if total_cost_drag is not None else (position.fees / max(position.entry_price * position.quantity, 1.0))
        risk_span = max(abs(position.max_adverse_return), 0.01)
        risk_adj = active / risk_span
        try:
            holding_days = max(0, (_parse_date(closed_at) - _parse_date(position.opened_at)).days)
        except Exception:
            holding_days = position.marks_count
        verdict = self._verdict(close_reason, active, hypothesis_adherence)
        return SettlementReport(
            validation_id=position.validation_id,
            close_reason=close_reason,
            entry_price=position.entry_price,
            exit_price=exit_price,
            entry_benchmark_price=position.entry_benchmark_price,
            exit_benchmark_price=exit_benchmark_price,
            stock_return=round(stock_ret, 6),
            benchmark_return=round(bench_ret, 6),
            active_return=round(active, 6),
            risk_adjusted_active_return=round(risk_adj, 6),
            cost_drag=round(costs, 6),
            holding_days=holding_days,
            hypothesis_adherence=hypothesis_adherence,
            rule_changed_midway=rule_changed_midway,
            verdict=verdict,
        )

    def _verdict(self, close_reason: str, active_return: float, hypothesis_adherence: bool) -> str:
        if close_reason in {CloseReason.DATA_INVALID.value, CloseReason.SYSTEM_BLOCKED.value}:
            return ValidationVerdict.CONTINUE_VALIDATION.value if close_reason == CloseReason.DATA_INVALID.value else ValidationVerdict.RETIRE.value
        if active_return > 0.03 and hypothesis_adherence:
            return ValidationVerdict.PROMOTE_CANDIDATE.value
        if active_return < -0.03:
            return ValidationVerdict.ETF_SUBSTITUTE_REVIEW.value
        if close_reason in {CloseReason.HYPOTHESIS_FAILED.value, CloseReason.STOP_LOSS.value}:
            return ValidationVerdict.RETIRE.value
        return ValidationVerdict.CONTINUE_VALIDATION.value
