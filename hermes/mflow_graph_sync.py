#!/usr/bin/env python3
"""
Hermes → M-FLOW 双向记忆同步 v1.0
功能: Hermes决策卡双写M-FLOW知识图谱，实现多跳图路由查询
图结构: 决策卡 → (标签) → 信号因子 → (关联) → 标的
"""
import json, os, time, uuid, requests

MFLOW_BASE = "http://localhost:8001"
HERMES_PATH = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/hermes/memory_bank.json")

# ═══════ 图路由结构 ═══════

GRAPH_EDGES = {
    # 标签 → 关联信号因子
    'D1洗盘':     ['R2_d1d2', 'T1_trend', 'I2_trend', 'I4_catalyst'],
    '信号确认':   ['R1_stage', 'T5_technical', 'I1_sector_rank'],
    '执行不足':   ['F3_capacity', 'T4_flow'],
    '过度乐观':   ['M2_fed', 'M3_inflation', 'M1_dollar'],
    '买入过早':   ['M1_dollar', 'M2_fed', 'M3_inflation', 'R4_event_days'],
    '宏观逆风':   ['M1_dollar', 'M2_fed', 'M3_inflation', 'M5_geo'],
    '过度保守':   ['F2_growth', 'I4_catalyst', 'R1_stage'],
    '卖出过早':   ['F2_growth', 'I2_trend', 'I4_catalyst'],
    '止损执行':   ['T1_trend', 'F4_institution'],
    '正确操作':   ['F3_capacity', 'T5_technical'],
}

SIGNAL_NAMES = {
    'M1_dollar':'美元指数','M2_fed':'美联储表态','M3_inflation':'CPI/PPI',
    'M4_us_china':'中美关系','M5_geo':'地缘风险',
    'I1_sector_rank':'板块排名','I2_trend':'板块趋势','I3_commodity':'核心商品',
    'I4_catalyst':'事件催化','I5_crowding':'拥挤度',
    'F1_pe':'PE估值','F2_growth':'业绩增速','F3_capacity':'产能订单',
    'F4_institution':'机构评级','F5_insider':'股东行为',
    'T1_trend':'趋势形态','T2_turnover':'换手率','T3_correlation':'板块联动',
    'T4_flow':'资金流向','T5_technical':'关键技术位',
    'R1_stage':'轮动阶段','R2_d1d2':'D1-D2模式','R3_neighbor':'相邻板块',
    'R4_event_days':'事件距今天数',
}


def connect_mflow():
    """连接M-flow并获取消息端点"""
    try:
        resp = requests.get(f"{MFLOW_BASE}/sse", stream=True, timeout=5)
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data:") and "/messages" in line:
                msg_url = f"{MFLOW_BASE}{line[5:].strip()}"
                resp.close()
                # Init
                requests.post(msg_url, json={"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"z2-hermes","version":"2.9.3"}},"id":"init"}, timeout=5)
                time.sleep(1)
                return msg_url
        resp.close()
    except:
        pass
    return None


def sync_decision_cards():
    """将Hermes决策卡同步为M-FLOW图结构记忆"""
    if not os.path.exists(HERMES_PATH):
        return 0
    
    with open(HERMES_PATH) as f:
        bank = json.load(f)
    
    cards = bank.get('cards', [])
    msg_url = connect_mflow()
    if not msg_url:
        return 0
    
    synced = 0
    for card in cards:
        tags = card.get('tags', [])
        stock = card.get('stock', '')
        
        # 构建图路由记忆
        edges = []
        for tag in tags:
            if tag in GRAPH_EDGES:
                for sig in GRAPH_EDGES[tag]:
                    sig_name = SIGNAL_NAMES.get(sig, sig)
                    edges.append(f"({tag})--[影响]-->({sig}:{sig_name})")
        
        graph_context = f"""
【图路由】决策卡→信号因子映射:
  STOCK:{stock}
  标签: {', '.join(tags)}
  图边: {' | '.join(edges[:5])}
  教训: {card.get('lesson','')[:200]}
  代价: {card.get('cost',0)}元
  情绪: {card.get('emotion','?')}
  场景: {card.get('priority_scene','?')}
  → 可多跳查询: MATCH (决策卡)-[影响]->(信号因子)-[关联]->(标的)
"""
        requests.post(msg_url, json={
            "jsonrpc":"2.0","method":"tools/call",
            "params":{"name":"save_interaction","arguments":{"content":graph_context}},
            "id":uuid.uuid4().hex[:8]
        }, timeout=5)
        synced += 1
    
    # 触发索引构建
    requests.post(msg_url, json={
        "jsonrpc":"2.0","method":"tools/call",
        "params":{"name":"memorize","arguments":{}},
        "id":"mem"
    }, timeout=5)
    
    return synced


def multi_hop_search(stock_code=None, lesson_tag=None):
    """多跳图查询: 通过决策卡→信号因子→标的链路搜索"""
    msg_url = connect_mflow()
    if not msg_url:
        return []
    
    queries = []
    if stock_code:
        queries.append(f"STOCK:{stock_code}")
    if lesson_tag:
        queries.append(f"标签包含{lesson_tag}的所有决策卡及其关联信号因子")
    
    query = " ".join(queries) if queries else "决策卡信号因子的图路由关系"
    
    requests.post(msg_url, json={
        "jsonrpc":"2.0","method":"tools/call",
        "params":{"name":"search","arguments":{"query":query}},
        "id":"q1"
    }, timeout=5)
    
    time.sleep(2)
    results = []
    try:
        resp2 = requests.get(f"{MFLOW_BASE}/sse", stream=True, timeout=5)
        for line in resp2.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                try:
                    data = json.loads(line[5:])
                    if "result" in data and "content" in data["result"]:
                        results = [c.get("text","") for c in data["result"]["content"]]
                        break
                except:
                    pass
        resp2.close()
    except:
        pass
    
    return results


if __name__ == '__main__':
    print("═══ Hermes→M-FLOW 图路由同步 ═══")
    
    # 1. 双写同步
    synced = sync_decision_cards()
    print(f"💾 双写: {synced}张决策卡 → M-FLOW图结构")
    
    # 2. 展示图路由结构
    print(f"\n🧠 图路由结构 ({len(GRAPH_EDGES)}个标签类型):")
    for tag, signals in list(GRAPH_EDGES.items())[:5]:
        signal_names = [SIGNAL_NAMES.get(s,'?') for s in signals[:3]]
        print(f"  ({tag}) → {' → '.join(signal_names)}")
    
    # 3. 多跳查询示例
    print(f"\n🔍 多跳查询: '双环传动相关决策→信号因子'")
    results = multi_hop_search('002472')
    if results:
        for r in results[:2]:
            print(f"  {r[:150]}...")
    else:
        print("  (索引构建中，搜索就绪后可多跳查询)")
    
    print(f"\n✅ 图路由双写完成")
    print(f"   下次查询: '双环D1洗盘那次涉及哪些信号因子?' → M-flow自动多跳路由")
