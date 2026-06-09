"""Stage E: Build V13.F5.5.4 Signal Source Recovery Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")
OUT.mkdir(parents=True, exist_ok=True)

SOURCES_DIR = Path("research/factor_library/sources")
AUDIT = OUT / "v13_f5_5_4_historical_factor_artifact_audit.json"
SAFETY = OUT / "v13_f5_5_4_signal_source_recovery_safety_audit.json"

TARGET_FACTORS = ["F04", "F10", "F11", "F14", "F15", "F16"]


def main():
    audit = json.loads(AUDIT.read_text())
    safety = json.loads(SAFETY.read_text())

    # Check which factors were successfully restored
    restored = []
    blocked = []
    for fid in TARGET_FACTORS:
        fdir = SOURCES_DIR / fid
        has_manifest = (fdir / "factor_manifest.json").exists()
        has_formula = (fdir / "formula_contract.json").exists()
        has_requirements = (fdir / "signal_materialization_requirements.json").exists()
        has_provenance = (fdir / "source_provenance.json").exists()

        if all([has_manifest, has_formula, has_requirements, has_provenance]):
            restored.append(fid)
        else:
            blocked.append(fid)

    all_pass = (
        len(restored) == len(TARGET_FACTORS) and
        safety["violation_count"] == 0
    )

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-4-SIGNAL-SOURCE-RECOVERY-CLOSEOUT",
        "status": ("V13_F5_5_4_SIGNAL_SOURCE_RECOVERY_PASS" if all_pass
                   else "V13_F5_5_4_SIGNAL_SOURCE_RECOVERY_PARTIAL"),
        "base_commit": "3f9f5ca",
        "source_recovery_executed": True,
        "restored_factors": restored,
        "blocked_factors": blocked,
        "ready_for_signal_materialization": restored,
        "all_10_factors_now_have_source": len(restored) == 6,
        "signal_score_generation_executed": False,
        "monitoring_rerun_executed": False,
        "candidate_state_update_executed": False,
        "ready_for_promotion_review": [],
        "promotion_allowed": False,
        "runner_enabled": False,
        "execution_allowed": False,
        "v13_6_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "recommended_next_action": "PREPARE_V13_F5_5_4_1_SIGNAL_SCORE_MATERIALIZATION_FOR_RESTORED_BATCH1_BATCH2_FACTORS"
    }

    out_path = OUT / "v13_f5_5_4_signal_source_recovery_closeout.json"
    out_path.write_text(json.dumps(closeout, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Status: {closeout['status']}")
    print(f"Restored: {len(restored)}, Blocked: {len(blocked)}")


if __name__ == "__main__":
    main()
