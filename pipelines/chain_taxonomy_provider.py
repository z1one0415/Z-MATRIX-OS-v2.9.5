"""Chain taxonomy provider — unified产业链映射

Replaces G14's hardcoded keyword-based chain mapping.
Each chain maps to industry codes and concept keywords.
"""
from __future__ import annotations

CHAINS = {
    "机器人": {
        "codes": ["002472", "002979", "002050", "300124", "688160", "002896", "688322",
                  "300024", "002527", "688017", "300680"],
        "keywords": ["双环", "雷赛", "三花", "绿的", "步科", "兆威", "奥比", "柯力",
                     "新松", "埃斯顿", "拓斯达", "禾川", "机器人", "伺服", "减速器"],
        "sw_sectors": ["机械设备", "自动化设备"],
    },
    "AI算力": {
        "codes": ["300308", "300394", "300502", "688256", "688041", "688111",
                  "000977", "002837", "002881", "603019", "688981"],
        "keywords": ["中际", "天孚", "新易盛", "寒武纪", "海光", "浪潮", "华工", "沪电",
                     "中贝", "英维克", "高澜", "美格", "恒玄", "光模块", "PCB", "液冷"],
        "sw_sectors": ["电子", "通信", "计算机"],
    },
    "半导体": {
        "codes": ["688981", "688256", "688041", "688111", "002049", "603986",
                  "300782", "300661", "688536", "688126"],
        "keywords": ["688", "兆易", "韦尔", "北方华创", "中微", "长电", "华天",
                     "晶圆", "封测", "EDA", "光刻", "芯片"],
        "sw_sectors": ["电子", "半导体"],
    },
    "资源周期": {
        "codes": ["601899", "601898", "600519", "000858", "601088", "600028",
                  "600188", "600547"],
        "keywords": ["紫金", "中煤", "神华", "黄金", "石油", "铜", "铝", "锂"],
        "sw_sectors": ["有色金属", "煤炭", "石油石化"],
    },
    "消费品牌": {
        "codes": ["600519", "000858", "002304", "600809", "000568"],
        "keywords": ["茅台", "五粮液", "洋河", "汾酒", "老窖", "白酒", "食品"],
        "sw_sectors": ["食品饮料"],
    },
}


def match_chain(ticker: str, name: str, industry: str = "") -> str | None:
    """Match a stock to its primary chain. Returns chain name or None."""
    for chain, info in CHAINS.items():
        if ticker in info["codes"]:
            return chain
        if industry and industry in info.get("sw_sectors", []):
            return chain
        if name:
            for kw in info.get("keywords", []):
                if kw in name:
                    return chain
    return None


def chain_density(tickers, names=None, industries=None) -> dict[str, int]:
    """Count tickers per chain. Returns {chain_name: count}."""
    density = {c: 0 for c in CHAINS}
    blind = 0
    for i, t in enumerate(tickers):
        n = names[i] if names and i < len(names) else ""
        ind = industries[i] if industries and i < len(industries) else ""
        ch = match_chain(t, n, ind)
        if ch:
            density[ch] += 1
        else:
            blind += 1
    density["⚠️未映射(盲区)"] = blind
    return density
