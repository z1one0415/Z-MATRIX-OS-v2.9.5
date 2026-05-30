"""Phase 5: Portfolio Validator — factor coverage, IC/RankIC contribution, risk constraints."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class PortfolioValidationResult:
    portfolio_id: str; passed: bool = False
    factor_coverage: float = 0.0; ic_contribution: float = 0.0
    risk_violations: list = field(default_factory=list)
    markdown_report: str = ""; json_report: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PortfolioValidator:
    @staticmethod
    def validate(portfolio, factor_validations: dict) -> PortfolioValidationResult:
        r = PortfolioValidationResult(portfolio_id=portfolio.portfolio_id)
        covered = sum(1 for t in portfolio.tickers if t in factor_validations)
        r.factor_coverage = covered / len(portfolio.tickers) if portfolio.tickers else 0
        r.ic_contribution = sum(factor_validations.get(t, {}).get("ic", 0) for t in portfolio.tickers) / max(len(portfolio.tickers), 1)
        if r.factor_coverage < 0.5: r.risk_violations.append(f"Factor coverage {r.factor_coverage}<0.5")
        if len(portfolio.tickers) > 30: r.risk_violations.append("Position count > 30")
        r.passed = len(r.risk_violations) == 0 and r.factor_coverage >= 0.5
        r.markdown_report = PortfolioValidator._generate_md(r)
        r.json_report = PortfolioValidator._generate_json(r)
        return r

    @staticmethod
    def _generate_md(result) -> str:
        return f"# Validation: {result.portfolio_id}\\n- Passed: {result.passed}\\n- Coverage: {result.factor_coverage:.2%}\\n- IC: {result.ic_contribution:.4f}\\n- Risk: {len(result.risk_violations)} violations\\n## Safety\\n- Production: BLOCKED"

    @staticmethod
    def _generate_json(result) -> str:
        import json; return json.dumps({"portfolio_id":result.portfolio_id,"passed":result.passed,"coverage":result.factor_coverage,"production_allowed":False})
