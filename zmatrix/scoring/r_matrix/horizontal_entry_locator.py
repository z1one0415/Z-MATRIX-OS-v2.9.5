"""Type A 水平通道位置定位器 — zone + allowed_action mapping"""
from dataclasses import dataclass

@dataclass
class HorizontalEntryResult:
    zone: str
    allowed_action: str
    next_trigger: list

def locate_horizontal_position(position):
    if position < 0:
        return HorizontalEntryResult("BREAKDOWN_REPAIR_WATCH","WAIT",
            ["5日内重新站回箱体","L1.5承接确认","不得放量破位"])
    if position <= 0.20:
        return HorizontalEntryResult("LOW_SUPPORT_ZONE","WATCH",
            ["支撑区止跌","缩量企稳","L3板块不逆风","L1.5承接确认"])
    if position <= 0.35:
        return HorizontalEntryResult("LOW_MID_ZONE","WAIT",
            ["回踩支撑区","或放量突破中轴"])
    if position < 0.70:
        return HorizontalEntryResult("MID_NO_EDGE_ZONE","WAIT",
            ["等待靠近下沿或上沿收割"])
    if position < 0.85:
        return HorizontalEntryResult("HIGH_WARNING_ZONE","HARVEST",
            ["接近阻力区","不追高","观察放量滞涨"])
    return HorizontalEntryResult("RESISTANCE_HARVEST_ZONE","HARVEST",
        ["阻力区兑现","不新增纸面试仓"])
