#!/usr/bin/env python3
"""
M-FLOW 自动同步守护 v1.0
扫描 memory/ + Obsidian投资记忆银行 → 新文件自动推M-FLOW
"""

import json, os, time, subprocess, hashlib, uuid

BASE = "http://localhost:8001"
CHECKPOINT = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/hermes/.mflow_sync_checkpoint.json")
MEMORY_DIR = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/memory")
OBSIDIAN_DIR = os.path.expanduser("~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行")
MEMORY_PALACE_DIR = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/记忆宫殿")

# ═══ 文件扫描 ═══

def scan_files():
    """扫描所有需要同步的文件"""
    files = []
    for directory in [MEMORY_DIR, OBSIDIAN_DIR, MEMORY_PALACE_DIR]:
        if not os.path.exists(directory):
            continue
        for root, _, filenames in os.walk(directory):
            for fn in filenames:
                if fn.endswith(('.md', '.json')) and not fn.startswith('.'):
                    fpath = os.path.join(root, fn)
                    stat = os.stat(fpath)
                    files.append({
                        'path': fpath,
                        'mtime': stat.st_mtime,
                        'size': stat.st_size,
                        'hash': hashlib.md5(fpath.encode()).hexdigest()[:12]
                    })
    return files


def load_checkpoint():
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT) as f:
            return json.load(f)
    return {'synced': {}, 'last_sync': None}


def save_checkpoint(cp):
    with open(CHECKPOINT, 'w') as f:
        json.dump(cp, f, indent=2)


# ═══ M-FLOW通信 ═══

def get_endpoint():
    r = subprocess.run(['curl','-sN','--max-time','5',f'{BASE}/sse'],
                       capture_output=True, text=True, timeout=6)
    for line in r.stdout.split('\n'):
        if 'data:' in line and '/messages' in line:
            return f'{BASE}{line.split("data:")[1].strip()}'
    return None


def init_session(endpoint):
    subprocess.run(['curl','-s','-X','POST', endpoint,
        '-H','Content-Type: application/json',
        '-d', json.dumps({'jsonrpc':'2.0','method':'initialize',
            'params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'z2-sync','version':'1.0'}},
            'id':'init'})], capture_output=True, timeout=5)


def save_to_mflow(endpoint, text):
    """存储一段文本到M-FLOW"""
    subprocess.run(['curl','-s','-X','POST', endpoint,
        '-H','Content-Type: application/json',
        '-d', json.dumps({'jsonrpc':'2.0','method':'tools/call',
            'params':{'name':'save_interaction','arguments':{'content':text}},
            'id': uuid.uuid4().hex[:8]})], capture_output=True, timeout=5)


def read_file_chunks(path, chunk_size=2000):
    """读文件并分割成块"""
    try:
        with open(path) as f:
            text = f.read()
        fn = os.path.basename(path)
        chunks = []
        # Split by double newline (paragraphs) and recombine to chunks
        paras = text.split('\n\n')
        current = f"[来源: {fn}]\n"
        for p in paras:
            if len(current) + len(p) > chunk_size:
                chunks.append(current.strip())
                current = f"[来源: {fn}]\n{p}"
            else:
                current += '\n' + p
        if current.strip():
            chunks.append(current.strip())
        return chunks
    except:
        return []


# ═══ 主流程 ═══

def sync():
    endpoint = get_endpoint()
    if not endpoint:
        print("❌ M-FLOW未连接")
        return 0
    
    init_session(endpoint)
    time.sleep(0.5)
    
    cp = load_checkpoint()
    files = scan_files()
    
    new_count = 0
    for f in files:
        key = f['hash']
        if key in cp['synced'] and cp['synced'][key] >= f['mtime']:
            continue
        
        # New or modified file
        size_kb = f['size'] / 1024
        print(f"📄 {os.path.basename(f['path'])} ({size_kb:.0f}KB)")
        
        chunks = read_file_chunks(f['path'])
        for chunk in chunks:
            save_to_mflow(endpoint, chunk)
            time.sleep(0.3)
        
        cp['synced'][key] = f['mtime']
        new_count += 1
    
    # Trigger indexing
    if new_count > 0:
        subprocess.run(['curl','-s','-X','POST', endpoint,
            '-H','Content-Type: application/json',
            '-d', json.dumps({'jsonrpc':'2.0','method':'tools/call',
                'params':{'name':'memorize','arguments':{}},
                'id':'mem'})], capture_output=True, timeout=5)
        print(f"🧠 索引已触发")
    
    cp['last_sync'] = time.strftime('%Y-%m-%d %H:%M:%S')
    save_checkpoint(cp)
    
    return new_count


if __name__ == '__main__':
    print("M-FLOW 自动同步守护 v1.0")
    n = sync()
    print(f"\n✅ 同步完成: {n}个新/改文件 → M-FLOW")
