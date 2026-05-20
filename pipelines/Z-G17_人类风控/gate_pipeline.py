#!/usr/bin/env python3
"""☯️ Z-G17 人类风控 — v1.0 | 每次HumanOverride | L1.6+Confession+记录"""
import argparse, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
LEDGER = WORKSPACE.parent / "human_behavior_ledger.jsonl"
sys.path.insert(0, str(WORKSPACE))

def run(override=None):
    now = datetime.now(timezone(timedelta(hours=8)))
    override = override or {"ticker":"002463","system_action":"WAIT","human_action":"WATCH","reason":"我觉得会涨"}
    
    result = {"pipeline_signature":"Z-G17_人类风控_v2.9.5-draft","timestamp":now.isoformat()}
    
    print(f"\n☯️ Z-G17 人类风控 — HumanOverride检测")
    print("=" * 60)
    
    # L1.6 Tilt检测
    tilt = False
    tilt_reasons = []
    if "觉得" in override.get("reason",""): tilt = True; tilt_reasons.append("主观感觉词")
    if override["system_action"] in ("BLOCK","WAIT") and override["human_action"] in ("WATCH",):
        tilt = True; tilt_reasons.append("覆盖系统BLOCK/WAIT")
    
    icon = "⚠️" if tilt else "✅"
    print(f"\n{icon} 覆盖检测:")
    print(f"  系统: {override['system_action']} → 人类: {override['human_action']}")
    print(f"  理由: {override['reason']}")
    if tilt:
        print(f"  ⚠️ TILT触发: {', '.join(tilt_reasons)}")
        print(f"  → 需要Confession Room确认")
        print(f"  → 降低系统背书")
        print(f"  → 记录到HumanBehaviorLedger")
    else:
        print(f"  ✅ 无TILT, 正常覆盖")
    
    # 记录
    entry = {**override, "timestamp":now.isoformat(),"tilt":tilt,"tilt_reasons":tilt_reasons}
    try:
        with open(LEDGER, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"\n📝 已记录: {LEDGER}")
    except Exception as e:
        print(f"⚠️ 记录失败: {e}")
    
    result["override"] = entry
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G17 人类风控")
    p.add_argument("--ticker", default="002463")
    p.add_argument("--system", default="WAIT")
    p.add_argument("--human", default="WATCH")
    p.add_argument("--reason", default="我觉得会涨")
    args = p.parse_args()
    run({"ticker":args.ticker,"system_action":args.system,"human_action":args.human,"reason":args.reason})
