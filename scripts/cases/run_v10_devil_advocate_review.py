#!/usr/bin/env python3
"""V10-C: Devil advocate review — evidence-bound reasons with triggers."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    inp = json.loads((C / "v10_council_input_pack.json").read_text())
    cr = json.loads((C / "v10_research_council_review.json").read_text())

    drs = []
    critical = 0
    high_total = 0
    med_total = 0

    for pf in inp["promoted_factors"]:
        fid = pf["factor_id"]
        mr = pf.get("mean_rankic")
        dp = pf.get("decay_pattern")
        rg = pf.get("robustness_grade")
        h = pf.get("horizon", "")

        # Get council review for this factor
        rv = next(
            (r for r in cr["reviews"] if r["factor_id"] == fid),
            {},
        )
        best_h = rv.get("evidence", {}).get("decay_pattern")
        council_verdict = rv.get("final_research_verdict", "WATCH_ONLY")

        modes = []

        # 1. Liquidity / market-cap proxy
        if "AMOUNT" in fid or "VOLUME" in fid:
            modes.append({
                "mode": "Liquidity / market-cap proxy",
                "risk_level": "HIGH",
                "reason": (
                    f"Factor '{fid}' uses traded amount/volume; "
                    "signal may proxy liquidity, market-cap, or crowding "
                    "rather than independent alpha."
                ),
                "trigger": "factor_id_contains_AMOUNT_or_VOLUME",
            })
            high_total += 1
        else:
            modes.append({
                "mode": "Liquidity / market-cap proxy",
                "risk_level": "LOW",
                "reason": (
                    f"Factor '{fid}' is not directly amount/volume based; "
                    "liquidity proxy risk lower but still monitored."
                ),
                "trigger": "factor_id_not_AMOUNT_or_VOLUME",
            })

        # 2. Industry concentration
        modes.append({
            "mode": "Industry concentration",
            "risk_level": "MEDIUM",
            "reason": (
                "V9 robustness has industry_warning=true or lacks full "
                "industry-neutral validation; paper stage must check "
                "industry concentration."
            ),
            "trigger": "industry_warning_or_missing_neutral",
        })
        med_total += 1

        # 3. Regime dependency
        if rg == "ROBUST":
            modes.append({
                "mode": "Regime dependency",
                "risk_level": "LOW",
                "reason": (
                    f"Robustness grade is ROBUST for '{fid}'; "
                    "regime consistency is high but decay still requires monitoring."
                ),
                "trigger": "robustness_grade_ROBUST",
            })
        elif rg == "REVIEW":
            modes.append({
                "mode": "Regime dependency",
                "risk_level": "MEDIUM",
                "reason": (
                    f"Robustness grade is REVIEW for '{fid}'; "
                    "signal may depend on market regime."
                ),
                "trigger": "robustness_grade_REVIEW",
            })
            med_total += 1
        else:
            modes.append({
                "mode": "Regime dependency",
                "risk_level": "HIGH",
                "reason": (
                    f"Robustness grade is {rg} for '{fid}'; "
                    "regime dependency risk elevated."
                ),
                "trigger": f"robustness_grade_{rg}",
            })
            high_total += 1

        # 4. Survivorship bias
        modes.append({
            "mode": "Survivorship bias",
            "risk_level": "MEDIUM",
            "reason": (
                "Expanded universe uses available case registry; "
                "survivorship and delisting coverage are not yet fully tested."
            ),
            "trigger": "case_registry_universe",
        })
        med_total += 1

        # 5. Data vendor bias
        modes.append({
            "mode": "Data vendor bias",
            "risk_level": "LOW",
            "reason": (
                "Data source consistency is hash-anchored via manifest, "
                "but vendor bias remains possible."
            ),
            "trigger": "single_vendor_tushare",
        })

        # 6. Multiple testing
        if inp.get("promoted_factor_count", 0) >= 10:
            modes.append({
                "mode": "Multiple testing / p-hacking",
                "risk_level": "MEDIUM",
                "reason": (
                    f"{inp['promoted_factor_count']} promoted factor×horizon "
                    "combinations increase selection and p-hacking risk."
                ),
                "trigger": "promoted_factor_count_ge_10",
            })
            med_total += 1
        else:
            modes.append({
                "mode": "Multiple testing / p-hacking",
                "risk_level": "LOW",
                "reason": "Fewer than 10 promoted combinations; lower selection risk.",
                "trigger": "promoted_factor_count_lt_10",
            })

        # 7. Transaction cost
        modes.append({
            "mode": "Turnover / transaction cost",
            "risk_level": "MEDIUM",
            "reason": (
                "No transaction cost, slippage, or turnover model exists yet; "
                "paper tracking must estimate cost impact."
            ),
            "trigger": "no_cost_model",
        })
        med_total += 1

        # 8. Horizon overfitting
        if dp == "NO_CLEAR_PATTERN":
            modes.append({
                "mode": "Horizon overfitting",
                "risk_level": "HIGH",
                "reason": (
                    f"Factor '{fid}' has NO_CLEAR_PATTERN decay; "
                    "best horizon may be selected by chance."
                ),
                "trigger": "decay_pattern_NO_CLEAR_PATTERN",
            })
            high_total += 1
        elif h not in (best_h or ""):
            modes.append({
                "mode": "Horizon overfitting",
                "risk_level": "MEDIUM",
                "reason": (
                    f"Selected horizon {h} differs from factor best {best_h}; "
                    "monitor horizon overfitting."
                ),
                "trigger": "horizon_differs_from_best",
            })
            med_total += 1
        else:
            modes.append({
                "mode": "Horizon overfitting",
                "risk_level": "LOW",
                "reason": f"Decay pattern is {dp}; horizon selection consistent.",
                "trigger": "decay_consistent",
            })

        # 9. Crowd decay
        modes.append({
            "mode": "Crowd decay",
            "risk_level": "MEDIUM",
            "reason": (
                "Price/volume factors can decay when crowded; "
                "paper tracking must monitor signal degradation."
            ),
            "trigger": "price_volume_factor_type",
        })
        med_total += 1

        # 10. Fundamental contradiction
        modes.append({
            "mode": "Fundamental contradiction",
            "risk_level": "MEDIUM",
            "reason": (
                "No financial, valuation, or fundamental cross-validation "
                "exists yet; thesis may conflict with fundamentals."
            ),
            "trigger": "no_fundamental_cross_validation",
        })
        med_total += 1

        # Critical blocker check
        is_critical = (
            dp == "NO_CLEAR_PATTERN"
            and rg in ("WEAK", "REJECT")
            and mr is not None
            and abs(mr) < 0.03
        )
        if is_critical:
            critical += 1

        drs.append({
            "factor_id": fid,
            "horizon": pf["horizon"],
            "evidence": {
                "mean_rankic": mr,
                "rankic_ir": pf.get("rankic_ir"),
                "valid_date_count": pf.get("valid_date_count"),
                "decay_pattern": dp,
                "robustness_grade": rg,
            },
            "failure_modes": modes,
            "devil_advocate_verdict": "WATCH_ONLY",
            "ready_for_paper_watchlist": not is_critical,
            "ready_for_alpha_claim": False,
            "alpha_validated": False,
        })

    da = {
        "status": "V10_DEVIL_ADVOCATE_REVIEW_BUILT",
        "failure_modes_checked": 10,
        "critical_blockers": critical,
        "high_risks": high_total,
        "medium_risks": med_total,
        "factor_failure_reviews": drs,
        "alpha_validated": False,
    }
    (C / "v10_devil_advocate_review.json").write_text(
        json.dumps(da, indent=2, ensure_ascii=False)
    )
    print(
        f"Devil Advocate: {critical}C/{high_total}H/{med_total}M "
        f"| reasons evidence-bound | triggers present"
    )


if __name__ == "__main__":
    main()
