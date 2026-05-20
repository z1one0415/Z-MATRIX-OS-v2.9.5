from __future__ import annotations
from .contracts import BMatrixInput, BaseType
from .brand_scarcity_analyzer import brand_scarcity_fit_score

_HIGH_DIVIDEND_INDUSTRIES = {"银行", "电信", "通信运营", "公用事业", "高速公路", "电力", "水务", "港口"}
_RESOURCE_INDUSTRIES = {"煤炭", "石油", "有色金属", "铜", "黄金", "贵金属", "资源"}
_STATE_INFRA_INDUSTRIES = {"电网", "铁路", "高速", "军工", "通信", "交通基础设施", "能源基础设施"}
_QUALITY_INDUSTRIES = {"医药", "消费", "家电", "制造龙头", "软件", "平台经济", "医疗器械"}
_FOOD_BEVERAGE = {"食品饮料", "白酒", "高端白酒", "酒", "饮料"}


def classify_base_type(stock: BMatrixInput) -> BaseType:
    """Classify bottom-holding type before scoring.

    v2.1.1 rule: food & beverage is not automatically compounding quality.
    High-end scarce brands are routed to BRAND_SCARCITY_MONOPOLY.
    """
    if stock.is_st or stock.suspended or stock.delisting_risk:
        return BaseType.NOT_B_MATRIX
    ind = stock.industry or ""

    if any(k in ind for k in _RESOURCE_INDUSTRIES):
        return BaseType.RESOURCE_CASH_COW

    if any(k in ind for k in _STATE_INFRA_INDUSTRIES) and stock.is_state_owned:
        return BaseType.STATE_INFRA_MONOPOLY

    if any(k in ind for k in _FOOD_BEVERAGE):
        fit = brand_scarcity_fit_score(stock)
        # If explicit brand/scarcity features strongly indicate a premium scarce brand,
        # do not route it into the reinvestment compounding bucket.
        if fit >= 7.2:
            return BaseType.BRAND_SCARCITY_MONOPOLY
        # Food companies with reinvestment runway can still be B2.
        if (stock.reinvestment_runway_score or 0) >= 7 and (stock.roic_5y or stock.roe_5y or 0) >= 12:
            return BaseType.COMPOUNDING_QUALITY
        return BaseType.NOT_B_MATRIX

    if any(k in ind for k in _HIGH_DIVIDEND_INDUSTRIES) or (stock.dividend_yield or 0) >= 4.0:
        return BaseType.HIGH_DIVIDEND_ANCHOR

    if any(k in ind for k in _QUALITY_INDUSTRIES) or (stock.roic_5y or stock.roe_5y or 0) >= 12.0:
        return BaseType.COMPOUNDING_QUALITY

    return BaseType.NOT_B_MATRIX
