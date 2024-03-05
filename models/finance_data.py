from dataclasses import dataclass
from typing import Optional


@dataclass
class FinanceRecord:
    user_id: int
    amount: float
    date: str
    category: str = None
    investment_type: str = None
    description: str = None


@dataclass
class FinanceFilter:
    user_id: int
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
