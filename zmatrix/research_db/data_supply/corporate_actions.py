"""CorporateActions — dividend, split, bonus, rights, delist, suspend adjustments."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class ActionType(str, Enum):
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"
    BONUS = "BONUS"
    RIGHTS = "RIGHTS"
    DELIST = "DELIST"
    SUSPEND = "SUSPEND"


@dataclass
class CorporateAction:
    ticker: str
    action_type: ActionType
    ex_date: str
    announcement_date: str = ""
    ratio: float = 1.0
    cash_per_share: float = 0.0
    description: str = ""
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False

    def adjust_price(self, price: float, forward: bool = True) -> float:
        if self.action_type == ActionType.SPLIT:
            if forward:
                return price / self.ratio
            else:
                return price * self.ratio
        elif self.action_type == ActionType.DIVIDEND:
            if forward:
                return price - self.cash_per_share
            else:
                return price + self.cash_per_share
        elif self.action_type == ActionType.BONUS:
            if forward:
                return price / (1.0 + self.ratio)
            else:
                return price * (1.0 + self.ratio)
        elif self.action_type == ActionType.RIGHTS:
            if forward:
                return (price * 1.0 + self.ratio) / (1.0 + self.ratio)
            else:
                return price * (1.0 + self.ratio) - self.ratio
        elif self.action_type in (ActionType.DELIST, ActionType.SUSPEND):
            return 0.0
        return price


def adjust_price(action: CorporateAction, price: float, forward: bool = True) -> float:
    return action.adjust_price(price, forward=forward)
