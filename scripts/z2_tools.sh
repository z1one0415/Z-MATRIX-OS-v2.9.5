#!/bin/bash
# z2_tools.sh — Z2 信息熔炉工具集 v2.9.1
# 路径: /Users/z1/.openclaw/agents/z2-analyst/workspace/scripts/

source "/Users/z1/.openclaw/workspace/scripts/zmatrix_env.sh"

case "${1:-help}" in
    chain|industry) shift; exec "$ZMATRIX_PYTHON" -m zmatrix.cli sector-scan "$@" ;;
    v3|sandbox) shift; exec "$ZMATRIX_PYTHON" -m zmatrix.cli run-once --mode v3 "$@" ;;
    reflexivity|crowd) exec "$ZMATRIX_PYTHON" -m zmatrix.cli reflexivity ;;
    chaos|chaos-budget) exec "$ZMATRIX_PYTHON" -m zmatrix.cli chaos-budget ;;
    frontnight|war) shift; exec "$ZMATRIX_PYTHON" -m zmatrix.cli frontnight "$@" ;;
    tape|tape-health) exec "$ZMATRIX_PYTHON" -m zmatrix.cli tape-health ;;
    graph) shift; exec "$ZMATRIX_PYTHON" -m zmatrix.cli graph "$@" ;;
    knowledge|kg) shift; exec "$ZMATRIX_PYTHON" -m zmatrix.cli kg-commit "$@" ;;
    sensor|sensors) exec "$ZMATRIX_PYTHON" -m zmatrix.cli sensor-status ;;
    l25|accuracy) shift; exec "$ZMATRIX_PYTHON" -m zmatrix.cli l25-accuracy "$@" ;;
    *) cat << 'HELP'
Z2 信息熔炉工具集 v2.9.1

命令:
  z2 chain              产业链分析
  z2 v3                 V3 压力沙盒
  z2 reflexivity        群体反身性信号
  z2 chaos-budget       混沌预算余额
  z2 frontnight         前夜战报
  z2 tape-health        盘口故障安全
  z2 graph daily        盘前主链图
  z2 graph confirm      盘中确认图
  z2 knowledge          知识图谱查询
  z2 sensor             传感器阵列状态
  z2 l25-accuracy       前夜战报准确率
HELP
esac

    # ═══ Hermes 天师命令 ═══
    hermes) shift
        case "${1:-help}" in
            research) shift
                exec "$ZMATRIX_PYTHON" -c "
import sys; sys.path.insert(0,'/Users/z1/.openclaw/agents/z2-analyst/workspace')
from contracts.research_contracts import ResearchRequest
from hermes.research_kernel import get_hermes_kernel
kernel = get_hermes_kernel()
request = ResearchRequest(request_id='cli_$(date +%s)', task_type='target_deep', symbol='${1:-?}', name='${2:-}')
insight = kernel.run_research(request)
print(insight.research_summary)
print(f'symbol={insight.symbol} confidence={insight.confidence} role={insight.suggested_role}')
" 2>&1
                ;;
            memory) shift
                case "${1:-stats}" in
                    query) shift
                        exec "$ZMATRIX_PYTHON" -c "
import sys; sys.path.insert(0,'/Users/z1/.openclaw/agents/z2-analyst/workspace')
from hermes.memory_bank import get_memory_bank
bank = get_memory_bank()
results = bank.query_by_symbol('${1:-}')
for r in results:
    print(f'{r[\"fingerprint\"]}: conf={r[\"confidence\"]} decayed={r[\"decayed_confidence\"]:.2f}')
" 2>&1
                        ;;
                    list) exec "$ZMATRIX_PYTHON" -c "
import sys; sys.path.insert(0,'/Users/z1/.openclaw/agents/z2-analyst/workspace')
from hermes.memory_bank import get_memory_bank
bank = get_memory_bank()
for m in bank.list_active():
    print(f'{m[\"fingerprint\"]}: {m[\"decayed_confidence\"]:.2f}')
" 2>&1
                        ;;
                    stats) exec "$ZMATRIX_PYTHON" -c "
import sys; sys.path.insert(0,'/Users/z1/.openclaw/agents/z2-analyst/workspace')
from hermes.memory_bank import get_memory_bank
print(get_memory_bank().stats())
" 2>&1
                        ;;
                esac
                ;;
            hypothesis) exec "$ZMATRIX_PYTHON" -c "
import sys; sys.path.insert(0,'/Users/z1/.openclaw/agents/z2-analyst/workspace')
from contracts.research_contracts import ResearchHypothesis
print('Hypothesis module ready.')
" 2>&1
                ;;
            learn) shift
                exec "$ZMATRIX_PYTHON" -c "
import sys; sys.path.insert(0,'/Users/z1/.openclaw/agents/z2-analyst/workspace')
from hermes.z9_learning_adapter import Z9LearningAdapter, ReviewEvent
adapter = Z9LearningAdapter()
review = ReviewEvent(review_id='manual_$(date +%s)', trading_day='$(date +%F)', symbol='${1:-?}', pattern='${2:-MANUAL}', deviation_magnitude=0.3, pattern_frequency=1)
candidates = adapter.consume_z9_review(review)
print(f'Generated {len(candidates)} candidates')
" 2>&1
                ;;
            *) cat << 'HH'
天师 Hermes 命令:
  z2 hermes research <symbol>    深度研究
  z2 hermes memory query <sym>   查询记忆
  z2 hermes memory list          列出活跃记忆
  z2 hermes memory stats         记忆库统计
  z2 hermes hypothesis <symbol>  生成假设
  z2 hermes learn <sym> <pat>    从 Review 学习
HH
        esac
        ;;
