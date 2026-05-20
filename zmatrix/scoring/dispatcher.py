"""
角色评分分流器 V2.0
──────────────────
定位: 角色化评分层 + 纪律约束输入，不是直接交易决策引擎。
只产生"角色候选与动作建议"，真实下单必须走 Centaur Responsibility Matrix。

V2.0 升级 (2026-05-07):
  1. 多角色输出: 一个标的可以同时是底仓+轮动 → role_candidates 数组
  2. 角色分类不硬切: 由仓位系统决定分配到底仓额度还是轮动额度
  3. 三个矩阵全部评分 → 取最高分角色为建议，其余为备选
"""

from __future__ import annotations
from dataclasses import dataclass, field
from inspect import signature
from typing import Any

from .b_matrix import BMatrix, BMatrixResult
from .r_matrix import RMatrix, RMatrixResult
from .d_matrix import DMatrix, DMatrixResult
from .d_band import evaluate_d_band, aggregate_execution_mode, DBandReport


@dataclass
class RoleCandidate:
    """单个角色候选"""
    role: str                # core_long_term | mid_term_rotation | dark_horse
    role_cn: str
    score: float
    grade: str
    recommendation: str
    stop_loss: float
    matrix_name: str         # "B-Matrix" | "R-Matrix" | "D-Matrix"
    execution_mode: str = "paper"
    allowed_action: str | None = None
    component: str | None = None
    lifecycle_stage: str | None = None
    real_trade_allowed: bool | None = None
    notes: list[str] = field(default_factory=list)

    def to_execution_candidate(self) -> dict[str, Any]:
        """Return the execution aggregation shape used by D-Matrix v2.1."""
        return {
            "role": self.role,
            "role_cn": self.role_cn,
            "matrix": self.matrix_name,
            "score": self.score,
            "grade": self.grade,
            "execution_mode": self.execution_mode,
            "execution": self.execution_mode,
            "allowed_action": self.allowed_action,
            "component": self.component,
            "stage": self.lifecycle_stage,
            "real_trade_allowed": self.real_trade_allowed,
            "warnings": self.notes,
        }


@dataclass
class BMatrixCompatResult:
    """Compatibility surface for B-Matrix v2.1 inside the V2.0 dispatcher.

    The selection workbench and cockpit still consume the stable role-scoring
    contract: total_score / grade / recommendation / stop_loss.  B-Matrix v2.1
    returns richer base-type and quality-gate fields, so this adapter preserves
    the old surface while carrying the new evidence forward.
    """

    code: str
    name: str
    total_score: float
    grade: str
    recommendation: str
    stop_loss: float
    base_type: str = ""
    raw_score: float = 0
    final_score: float = 0
    rating_cap: str = "A"
    eligibility: str = ""
    quality_flags: list[str] = field(default_factory=list)
    trap_flags: list[str] = field(default_factory=list)
    thesis_snapshot: dict[str, Any] = field(default_factory=dict)
    thesis_stop_rules: list[str] = field(default_factory=list)
    allowed_action: str = ""
    forbidden: list[str] = field(default_factory=list)

    @classmethod
    def from_v21(cls, result: Any, *, current_price: float) -> "BMatrixCompatResult":
        grade = str(getattr(result, "rating", "D") or "D")
        total_score = round(float(getattr(result, "final_score", getattr(result, "raw_score", 0)) or 0), 1)
        quality_flags = list(getattr(result, "quality_flags", []) or [])
        trap_flags = list(getattr(result, "trap_flags", []) or [])
        recommendation = _b_recommendation(grade, getattr(result, "eligibility", ""), quality_flags, trap_flags)
        stop_loss = round(current_price * 0.90, 2) if current_price > 0 else 0
        return cls(
            code=str(getattr(result, "symbol", "") or ""),
            name=str(getattr(result, "name", "") or ""),
            total_score=total_score,
            grade=grade,
            recommendation=recommendation,
            stop_loss=stop_loss,
            base_type=str(getattr(result, "base_type", "") or ""),
            raw_score=round(float(getattr(result, "raw_score", total_score) or 0), 1),
            final_score=total_score,
            rating_cap=str(getattr(result, "rating_cap", "A") or "A"),
            eligibility=str(getattr(result, "eligibility", "") or ""),
            quality_flags=quality_flags,
            trap_flags=trap_flags,
            thesis_snapshot=dict(getattr(result, "thesis_snapshot", {}) or {}),
            thesis_stop_rules=list(getattr(result, "thesis_stop_rules", []) or []),
            allowed_action=str(getattr(result, "allowed_action", "") or ""),
            forbidden=list(getattr(result, "forbidden", []) or []),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "total_score": self.total_score,
            "grade": self.grade,
            "recommendation": self.recommendation,
            "stop_loss": self.stop_loss,
            "base_type": self.base_type,
            "raw_score": self.raw_score,
            "final_score": self.final_score,
            "rating_cap": self.rating_cap,
            "eligibility": self.eligibility,
            "quality_flags": self.quality_flags,
            "trap_flags": self.trap_flags,
            "thesis_snapshot": self.thesis_snapshot,
            "thesis_stop_rules": self.thesis_stop_rules,
            "allowed_action": self.allowed_action,
            "forbidden": self.forbidden,
        }


@dataclass
class RoleScore:
    """V2.0 多角色评分结果"""
    code: str
    name: str

    # 所有角色的候选 (按score降序)
    role_candidates: list[RoleCandidate] = field(default_factory=list)

    # 各个矩阵的完整结果 (都计算，都保留)
    b_result: BMatrixResult | None = None
    r_result: RMatrixResult | None = None
    d_result: DMatrixResult | None = None
    d_band_report: DBandReport | None = None
    d_band_error: str | None = None

    # 执行模式
    execution_mode: str = "paper"  # blocked | none | paper | human_confirm | auto
    execution_note: str = ""
    execution_aggregation: dict[str, Any] | None = None

    # 统一接口 (取最高分角色)
    @property
    def primary_role(self) -> RoleCandidate | None:
        return self.role_candidates[0] if self.role_candidates else None

    @property
    def total_score(self) -> float:
        return self.primary_role.score if self.primary_role else 0

    @property
    def grade(self) -> str:
        return self.primary_role.grade if self.primary_role else "D"

    @property
    def recommendation(self) -> str:
        return self.primary_role.recommendation if self.primary_role else "❌ 无建议"

    @property
    def stop_loss(self) -> float:
        return self.primary_role.stop_loss if self.primary_role else 0

    @property
    def matrix_name(self) -> str:
        return self.primary_role.matrix_name if self.primary_role else "None"

    def summary(self) -> str:
        """人类可读的多角色摘要。"""
        lines = [f"{self.name} ({self.code})"]
        for rc in self.role_candidates:
            lines.append(
                f"  [{rc.matrix_name}] {rc.role_cn}({rc.role}) "
                f"评分{rc.score:.1f} {rc.grade}级 — {rc.recommendation}"
            )
        if self.execution_mode != "auto":
            lines.append(f"  ⚠️ 执行模式: {self.execution_mode} — {self.execution_note}")
        return "\n".join(lines)


class RoleDispatcher:
    """V2.0 角色评分分发器。

    核心改变:
    - 对所有候选全部运行三个矩阵评分
    - 输出 role_candidates 数组 (而非单一角色)
    - D-Matrix 默认 paper/shadow 模式
    - 最终角色分配由仓位系统决定
    
    🔒 宪法围栏: 调用 evaluate() 前必须先通过 DataGate。
       使用 gated_dispatch() 作为唯一入口。
    """

    def __init__(self):
        self._b = BMatrix()
        self._r = RMatrix()
        self._d = DMatrix()

    def evaluate(self, code: str, name: str, *,
                 # B-Matrix 参数
                 financials: dict | None = None,
                 spot: dict | None = None,
                 industry: str = "",
                 is_soe: bool = False,
                 is_leader: bool = False,
                 cashflow_quality: dict | None = None,

                 # R-Matrix 参数
                 kline_records: list[dict] | None = None,
                 sector_state: str = "NEUTRAL",
                 sector_name: str = "",
                 north_flow_consecutive: int = 0,
                 market_cap: float = 0,
                 pe: float = 0,
                 historical_high: float = 0,
                 decline_converging: bool = False,
                 sector_diffusion_ok: bool = False,

                 # D-Matrix 参数
                 catalyst: dict | None = None,
                 dragon_tiger: dict | None = None,
                 overhead_resistance: float = 0,
                 distance_to_ath: float = 0,
                 consecutive_limit_up: int = 0,
                 is_tradable: bool = True,
                 is_locked_board: bool = False,
                 d_band_payload: dict | None = None,
                 global_blockers: list[str] | None = None,
                 ) -> RoleScore:
        """V2.0 全矩阵评估 — 一次调用，三个矩阵都跑。

        Returns:
            RoleScore with role_candidates array
        """
        result = RoleScore(code=code, name=name)

        # ── 并行运行三个矩阵 ──────────────────────────
        # B-Matrix
        b_kwargs = dict(
            financials=financials, spot=spot, industry=industry,
            is_soe=is_soe, is_leader=is_leader,
            cashflow_quality=cashflow_quality,
        )
        result.b_result = self._score_b_matrix(code, name, **b_kwargs)

        # R-Matrix
        r_kwargs = dict(
            kline_records=kline_records, sector_state=sector_state,
            sector_name=sector_name, north_flow_consecutive=north_flow_consecutive,
            market_cap=market_cap, pe=pe, historical_high=historical_high,
            decline_converging=decline_converging,
            sector_diffusion_ok=sector_diffusion_ok,
        )
        result.r_result = self._r.score(code, name, **r_kwargs)

        # D-Matrix
        d_kwargs = dict(
            catalyst=catalyst, spot=spot, kline_records=kline_records,
            dragon_tiger=dragon_tiger, overhead_resistance=overhead_resistance,
            distance_to_ath=distance_to_ath,
            consecutive_limit_up=consecutive_limit_up,
            is_tradable=is_tradable, is_locked_board=is_locked_board,
        )
        result.d_result = self._d.score(code, name, **d_kwargs)

        # D-Matrix v2.1 / D-Band Phase1: early black-horse preheat.
        # It is a paper-only lifecycle signal, not a replacement for confirmed D-Matrix.
        if d_band_payload is not None:
            try:
                payload = dict(d_band_payload)
                payload.setdefault("code", code)
                payload.setdefault("name", name)
                result.d_band_report = evaluate_d_band(payload)
            except Exception as exc:  # keep B/R/D scoring usable if preheat payload is incomplete
                result.d_band_error = str(exc)

        # ── 组装多角色候选 ────────────────────────────
        candidates = []

        # B-Matrix 候选
        if result.b_result and result.b_result.grade != "D":
            candidates.append(RoleCandidate(
                role="core_long_term", role_cn="底仓",
                score=result.b_result.total_score,
                grade=result.b_result.grade,
                recommendation=result.b_result.recommendation,
                stop_loss=result.b_result.stop_loss,
                matrix_name="B-Matrix",
                execution_mode="human_confirm",
                allowed_action="HUMAN_CONFIRM",
                real_trade_allowed=True,
            ))

        # R-Matrix 候选
        if result.r_result and result.r_result.grade != "D":
            r_rec = result.r_result.recommendation
            # 无右侧确认 → 降级到 watch/paper
            if result.r_result.execution_mode == "paper":
                r_mode = "paper"
                r_action = "WATCH"
                if "纸面" not in r_rec:
                    r_rec += " ⚠️ 数据/权限不足 → watch/paper模式"
            elif not decline_converging and not sector_diffusion_ok:
                r_rec += " ⚠️ 无右侧确认 → watch/paper模式"
                r_mode = "paper"
                r_action = "WATCH"
            else:
                r_mode = "human_confirm"
                r_action = "HUMAN_CONFIRM"
            candidates.append(RoleCandidate(
                role="mid_term_rotation", role_cn="轮动",
                score=result.r_result.total_score,
                grade=result.r_result.grade,
                recommendation=r_rec,
                stop_loss=result.r_result.stop_loss,
                matrix_name="R-Matrix",
                execution_mode=r_mode,
                allowed_action=r_action,
                real_trade_allowed=r_mode == "human_confirm",
            ))

        # D-Matrix 候选 — 默认 paper/shadow 模式
        if result.d_result and result.d_result.grade != "D":
            d_rec = result.d_result.recommendation
            if not is_tradable or is_locked_board:
                d_rec += " ⚠️ 不可交易(一字板/停牌) → paper模式"
                d_mode = "paper"
                d_action = "WATCH"
            else:
                d_mode = "human_confirm"
                d_action = "HUMAN_CONFIRM"
            candidates.append(RoleCandidate(
                role="dark_horse", role_cn="黑马",
                score=result.d_result.total_score,
                grade=result.d_result.grade,
                recommendation=d_rec,
                stop_loss=result.d_result.stop_loss,
                matrix_name="D-Matrix",
                execution_mode=d_mode,
                allowed_action=d_action,
                real_trade_allowed=d_mode == "human_confirm",
            ))

        # D-Matrix v2.1 candidate — preheat only. It may enter Alpha validation,
        # but Phase1 must never grant real-trade authority.
        if result.d_band_report and result.d_band_report.allowed_action.value != "NONE":
            report = result.d_band_report
            candidates.append(RoleCandidate(
                role="dark_horse",
                role_cn="黑马预热",
                score=report.d_early_score,
                grade=_grade_from_score(report.d_early_score),
                recommendation=(
                    f"D-Matrix v2.1 {report.d_lifecycle_stage.value}："
                    f"{report.allowed_action.value}，仅允许进入 Alpha 平行验证仓"
                ),
                stop_loss=0,
                matrix_name="D-Matrix v2.1",
                execution_mode=report.execution_mode.value,
                allowed_action=report.allowed_action.value,
                component="D-Matrix v2.1",
                lifecycle_stage=report.d_lifecycle_stage.value,
                real_trade_allowed=False,
                notes=report.warnings + report.caps_applied + report.forbidden,
            ))

        # 按分数降序
        candidates.sort(key=lambda x: x.score, reverse=True)
        result.role_candidates = candidates

        # ── 执行模式判定 ──────────────────────────────
        primary = result.primary_role
        if primary is None:
            result.execution_mode = "none"
            result.execution_note = "无有效候选"
        else:
            agg = aggregate_execution_mode(
                selected_role=primary.role,
                role_candidates=[c.to_execution_candidate() for c in candidates],
                global_blockers=global_blockers or [],
            )
            result.execution_aggregation = agg.to_dict()
            result.execution_mode = agg.final_execution_mode
            if result.execution_mode == "blocked":
                result.execution_note = "存在全局阻断条件，禁止进入真实建仓"
            elif primary.matrix_name == "D-Matrix v2.1":
                result.execution_note = "D-Matrix v2.1 Phase1 只能进入 Alpha 平行验证仓"
            elif primary.role == "dark_horse":
                result.execution_note = "黑马需人工确认后方可实盘"
            elif primary.role == "mid_term_rotation" and primary.execution_mode == "paper":
                result.execution_note = "无右侧确认 → 纸笔跟踪，不入实盘"
            elif primary.role == "mid_term_rotation":
                result.execution_note = "轮动需人工确认周期位置后执行"
            else:
                result.execution_note = "底仓需人工确认估值后执行"

        return result

    def _score_b_matrix(
        self,
        code: str,
        name: str,
        *,
        financials: dict | None = None,
        spot: dict | None = None,
        industry: str = "",
        is_soe: bool = False,
        is_leader: bool = False,
        cashflow_quality: dict | None = None,
    ) -> Any:
        """Score B-Matrix while bridging legacy V2.0 inputs to V2.1."""
        if _score_accepts_legacy_b_contract(self._b.score):
            return self._b.score(
                code,
                name,
                financials=financials,
                spot=spot,
                industry=industry,
                is_soe=is_soe,
                is_leader=is_leader,
                cashflow_quality=cashflow_quality,
            )

        spt = spot or {}
        v21_result = self._b.score(
            code,
            name,
            **_b_v21_kwargs(
                financials=financials,
                spot=spt,
                industry=industry,
                is_soe=is_soe,
                is_leader=is_leader,
                cashflow_quality=cashflow_quality,
            ),
        )
        return BMatrixCompatResult.from_v21(v21_result, current_price=_current_price_from_spot(spt))


def _score_accepts_legacy_b_contract(score_fn: Any) -> bool:
    try:
        return "financials" in signature(score_fn).parameters
    except (TypeError, ValueError):
        return False


def _b_v21_kwargs(
    *,
    financials: dict | None,
    spot: dict | None,
    industry: str,
    is_soe: bool,
    is_leader: bool,
    cashflow_quality: dict | None,
) -> dict[str, Any]:
    fin = financials or {}
    spt = spot or {}
    cf = cashflow_quality or {}

    ocf_3y = _num(_first_present(cf, fin, ("ocf_3y", "operating_cashflow_3y", "ocf")), 0)
    profit_3y = _num(_first_present(cf, fin, ("profit_3y", "net_profit_3y", "profit")), 0)
    if "ocf_to_profit" in cf and profit_3y <= 0:
        profit_3y = 1.0
        ocf_3y = _num(cf.get("ocf_to_profit"), 1.0)

    fcf = _num(_first_present(cf, fin, ("fcf", "free_cashflow", "free_cash_flow")), 0)
    dividends = _num(_first_present(cf, fin, ("dividends", "dividend_cash", "cash_dividend")), 0)
    debt_rising = bool(cf.get("debt_rising") or fin.get("debt_rising"))
    if cf.get("dividend_from_debt"):
        debt_rising = True
        if dividends <= 0:
            dividends = 1.0

    return {
        "industry": industry,
        "is_soe": is_soe,
        "is_leader": is_leader,
        "gross_margin": _num(_first_present(fin, spt, ("gross_margin", "gross_profit_margin")), 50),
        "brand_score": _num(_first_present(fin, spt, ("brand_score",)), 5),
        "capex_reinvest": _num(_first_present(fin, spt, ("capex_reinvest", "capex_reinvestment")), 5),
        "roe": _num(_first_present(fin, spt, ("roe", "roe_current", "roe_5y", "roe_5y_avg")), 10),
        "dy": _num(_first_present(spt, fin, ("dividend_yield", "dy")), 2),
        "pe": _num(_first_present(fin, spt, ("pe", "pe_current", "pe_ttm")), 15),
        "pb": _num(_first_present(fin, spt, ("pb", "pb_current")), 1.5),
        "debt": _num(_first_present(fin, spt, ("debt_ratio", "debt_to_assets", "debt")), 50),
        "ocf_3y": ocf_3y,
        "profit_3y": profit_3y,
        "fcf": fcf,
        "dividends": dividends,
        "debt_rising": debt_rising,
        "ar_divergence": bool(cf.get("receivables_abnormal") or cf.get("ar_divergence") or fin.get("ar_divergence")),
        "inv_divergence": bool(cf.get("inventory_abnormal") or cf.get("inv_divergence") or fin.get("inv_divergence")),
        "cycle_position": str(_first_present(fin, spt, ("cycle_position", "cycle_pos")) or "normal"),
        "cost_adv": _num(_first_present(fin, spt, ("cost_adv", "cost_advantage")), 5),
        "resource_q": _num(_first_present(fin, spt, ("resource_q", "resource_quality")), 5),
        "roic_trend": str(_first_present(fin, spt, ("roic_trend",)) or "stable"),
        "cf_quality": _num(_first_present(fin, cf, ("cf_quality", "cashflow_quality_score")), 5),
        "policy_stability": _num(_first_present(fin, spt, ("policy_stability",)), 5),
        "cf_visibility": _num(_first_present(fin, spt, ("cf_visibility", "cashflow_visibility")), 5),
        "monopoly": _num(_first_present(fin, spt, ("monopoly",)), 5),
        "dividend_discipline": _num(_first_present(fin, spt, ("dividend_discipline",)), 5),
        "has_monopoly_license": bool(fin.get("has_monopoly_license") or spt.get("has_monopoly_license")),
        "has_entry_barrier": bool(fin.get("has_entry_barrier") or spt.get("has_entry_barrier")),
    }


def _b_recommendation(grade: str, eligibility: Any, quality_flags: list[str], trap_flags: list[str]) -> str:
    base = {
        "A": "✅ 核心底仓",
        "B": "✅ 次级底仓",
        "C": "⚠️ 不推荐底仓",
        "D": "❌ 不符合底仓标准",
    }.get(grade, "❌ 不符合底仓标准")
    notes = []
    eligibility_text = str(eligibility or "")
    if eligibility_text and eligibility_text not in {"B_ELIGIBLE", "B_DISQUALIFIED"}:
        notes.append(eligibility_text)
    if quality_flags:
        notes.append("质量闸门: " + "/".join(quality_flags[:2]))
    if trap_flags:
        notes.append("陷阱标记: " + "/".join(trap_flags[:2]))
    return base if not notes else f"{base}；{'；'.join(notes)}"


def _current_price_from_spot(spot: dict | None) -> float:
    spt = spot or {}
    return _num(_first_present(spt, ("current", "price", "current_price", "last_price", "close")), 0)


def _first_present(*sources_and_keys: Any) -> Any:
    if not sources_and_keys:
        return None
    *sources, keys = sources_and_keys
    if not isinstance(keys, tuple):
        keys = (keys,)
    for source in sources:
        if not isinstance(source, dict):
            continue
        for key in keys:
            if key in source and source[key] not in (None, ""):
                return source[key]
    return None


def _num(value: Any, default: float) -> float:
    try:
        if value in (None, ""):
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


# ── 便捷函数 ─────────────────────────────────────────────

def quick_evaluate(code: str, name: str, **kwargs) -> RoleScore:
    """快速评估: 创建 Dispatcher 并评估。
    
    ⚠️ 不经过 DataGate！仅用于测试/非交易场景。
    生产环境请使用 gated_dispatch()。
    """
    d = RoleDispatcher()
    return d.evaluate(code, name, **kwargs)


# ── 🔒 宪法围栏：唯一入口 ─────────────────────────────────

def gated_dispatch(
    candidates: list[dict],
    market_context: dict | None = None,
) -> dict:
    """
    🔒 宪法强制门禁入口 — Agent 评分的唯一合法入口。
    
    流程:
      1. 运行 DataGate 门禁图
      2. BLOCK → 返回 blocked，不评分
      3. DEGRADED → 评分但标注 ⚠️
      4. ALLOW → 正常评分
      
    candidates 格式: [{"code": "002371", "name": "北方华创", ...}, ...]
    """
    from zmatrix.graph.data_gate import run_data_gate, BLOCK

    codes = [c["code"] for c in candidates]
    gate = run_data_gate(codes)

    if gate["data_gate"] == BLOCK:
        return {
            "status": "BLOCKED",
            "gate": gate,
            "reason": gate["gate_reason"],
            "results": [],
        }

    # 注入核验价格
    prices = gate.get("prices_valid", {})
    dispatcher = RoleDispatcher()
    results = []

    for c in candidates:
        code = c["code"]
        name = c.get("name", code)
        validated_price = prices.get(code)

        spot = c.get("spot", {})
        if validated_price and not spot.get("price"):
            spot["price"] = validated_price
            spot["source"] = "data_gate"

        try:
            score = dispatcher.evaluate(
                code, name,
                financials=c.get("financials"),
                spot=spot or None,
                industry=c.get("industry", ""),
                is_soe=c.get("is_soe", False),
                is_leader=c.get("is_leader", False),
                kline_records=c.get("kline_records"),
                sector_state=c.get("sector_state", "NEUTRAL"),
                market_cap=float(c.get("market_cap", 0) or 0),
                pe=float(c.get("pe", 0) or 0),
                catalyst=c.get("catalyst"),
                is_tradable=c.get("is_tradable", True),
            )
            results.append(score)
        except Exception as exc:
            results.append({"code": code, "name": name, "error": str(exc)})

    return {
        "status": gate["data_gate"],  # ALLOW or DEGRADED
        "gate": gate,
        "results": results,
        "candidates_scored": len(results),
        "prices_validated": len(prices),
    }


def _grade_from_score(score: float) -> str:
    if score >= 8.0:
        return "A"
    if score >= 6.5:
        return "B"
    if score >= 5.0:
        return "C"
    return "D"
