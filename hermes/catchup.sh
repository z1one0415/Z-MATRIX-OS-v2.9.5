#!/bin/bash
# Z2 任务补跑 — 检测遗漏的cron任务并补执行
LAST_RUN=$(cat ~/.openclaw/agents/z2-analyst/workspace/hermes/.last_catchup 2>/dev/null || echo "1970-01-01")
NOW=$(date +%Y-%m-%d)
if [ "$LAST_RUN" != "$NOW" ]; then
    echo "$NOW" > ~/.openclaw/agents/z2-analyst/workspace/hermes/.last_catchup
    echo "📅 今日首次启动，检查遗漏任务..."
    # 如果15:30已过且今天还没生成日卡 → 立即生成
    if [ $(date +%H) -ge 16 ]; then
        DAY_CARD="/Users/z1/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行/日记忆卡/${NOW}_日报.md"
        if [ ! -f "$DAY_CARD" ]; then
            echo "  ⚠️ 日记忆卡遗漏，正在补生成..."
            ~/workspace-dev/.venv_glm5/bin/python3 ~/.openclaw/agents/z2-analyst/workspace/hermes/daily_card.py "$NOW" 2>/dev/null
        fi
    fi
fi
