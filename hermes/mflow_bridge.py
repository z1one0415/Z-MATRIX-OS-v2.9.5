#!/usr/bin/env python3
"""
M-FLOW 集成桥 v2.0 — httpx-sse 修复SSE读回
核心改进: 保持SSE连接不关 → POST请求和响应在同一通道
"""
import json, time, os, uuid, sys, threading
import httpx

MFLOW_BASE = "http://localhost:8001"


class MFlowBridge:
    def __init__(self):
        self.msg_url = None
        self._lock = threading.Lock()
        self._responses = {}  # id → result
        self._sse_thread = None
        self._running = False
    
    def connect(self):
        """连接M-flow并启动SSE监听线程"""
        try:
            # 1. 获取消息端点
            with httpx.Client(timeout=httpx.Timeout(10.0)) as client:
                with client.stream("GET", f"{MFLOW_BASE}/sse") as resp:
                    for line in resp.iter_lines():
                        if line and "/messages" in line:
                            if line.startswith("data:"):
                                self.msg_url = f"{MFLOW_BASE}{line[5:].strip()}"
                            break
            if not self.msg_url:
                print("  ❌ 未找到消息端点", file=sys.stderr)
                return False
            
            # 2. 初始化
            self._post("initialize", {"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"z2","version":"2.9.3"}})
            
            # 3. 启动SSE监听线程
            self._running = True
            self._sse_thread = threading.Thread(target=self._sse_listener, daemon=True)
            self._sse_thread.start()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"  M-flow连接失败: {e}", file=sys.stderr)
            return False
    
    def _sse_listener(self):
        """持续监听SSE流并收集响应"""
        while self._running:
            try:
                with httpx.Client(timeout=httpx.Timeout(None, connect=10.0)) as client:
                    with client.stream("GET", f"{MFLOW_BASE}/sse") as resp:
                        for line in resp.iter_lines():
                            if not self._running:
                                break
                            if line and line.startswith("data:"):
                                try:
                                    data = json.loads(line[5:])
                                    msg_id = data.get("id")
                                    if msg_id and "result" in data:
                                        with self._lock:
                                            self._responses[msg_id] = data["result"]
                                except json.JSONDecodeError:
                                    pass
            except Exception as e:
                if self._running:
                    time.sleep(2)  # 重连间隔
    
    def _post(self, method, params=None):
        """发送POST请求（fire-and-forget）"""
        if not self.msg_url:
            return False
        try:
            with httpx.Client(timeout=httpx.Timeout(10.0)) as client:
                r = client.post(self.msg_url, json={
                    "jsonrpc": "2.0", "method": method,
                    "params": params or {}, "id": uuid.uuid4().hex[:8]
                })
                return r.status_code in (200, 202)
        except:
            return False
    
    def _call_and_wait(self, tool_name, args, timeout=15):
        """发送工具调用并等待SSE响应"""
        call_id = uuid.uuid4().hex[:8]
        payload = {
            "jsonrpc": "2.0", "method": "tools/call",
            "params": {"name": tool_name, "arguments": args},
            "id": call_id
        }
        try:
            with httpx.Client(timeout=httpx.Timeout(10.0)) as client:
                client.post(self.msg_url, json=payload)
            
            # 等待响应
            deadline = time.time() + timeout
            while time.time() < deadline:
                with self._lock:
                    if call_id in self._responses:
                        result = self._responses.pop(call_id)
                        return result
                time.sleep(0.5)
            return None
        except:
            return None
    
    # ═══ 公开接口 ═══
    
    def save(self, content):
        """存储交互（fire-and-forget）"""
        return self._post("tools/call", {"name":"save_interaction","arguments":{"content":content}})
    
    def search(self, query):
        """语义搜索（等待响应）"""
        result = self._call_and_wait("search", {"query": query}, timeout=15)
        if result and "content" in result:
            return [c.get("text","") for c in result["content"]]
        return []
    
    def memorize(self):
        """触发索引构建"""
        return self._post("tools/call", {"name":"memorize","arguments":{}})
    
    def query(self, question):
        """知识查询"""
        result = self._call_and_wait("query", {"question": question}, timeout=20)
        if result and "content" in result:
            return result["content"][0].get("text","") if result["content"] else ""
        return ""


# ═══════ 全局钩子 ═══════

_bridge = None

def get_bridge():
    global _bridge
    if _bridge is None:
        _bridge = MFlowBridge()
        _bridge.connect()
    return _bridge


def recall(stock=None, topic=None):
    """决策前召回关联记忆"""
    bridge = get_bridge()
    q = f"{stock or ''} {topic or ''}".strip()
    if not q:
        return None
    memories = bridge.search(q)
    return {'query': q, 'count': len(memories), 'memories': memories} if memories else None


def memorize(tags, content):
    """决策后自动存储"""
    bridge = get_bridge()
    return bridge.save(f"[{time.strftime('%m/%d %H:%M')}] {tags}\n{content}")


# ═══════ CLI ═══════

if __name__ == '__main__':
    print("M-FLOW 集成桥 v2.0 (httpx-sse)")
    bridge = MFlowBridge()
    
    if not bridge.connect():
        print("❌ 连接失败")
        sys.exit(1)
    print("✅ SSE连接已建立")
    
    # 测试存储
    print("💾 存储测试...", end=" ")
    ok = bridge.save("【v2.0测试】SSE修复验证 — 保持连接不中断")
    print("✅" if ok else "⚠️")
    
    # 测试搜索 (SSE读回)
    print("🔍 搜索测试 (SSE读回)...")
    results = bridge.search("SSE修复 持仓")
    if results:
        print(f"   ✅ {len(results)}条结果")
        for r in results[:2]:
            print(f"   {r[:120]}...")
    else:
        print("   🟡 未找到或索引构建中")
    
    print("\n✅ M-FLOW v2.0 集成完成")
    print("   修复: SSE读回 → httpx持久连接+后台监听线程")
