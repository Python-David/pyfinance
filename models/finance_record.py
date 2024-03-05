from dataclasses import dataclass


@dataclass
class FinanceRecord:
    user_id: int
    amount: float
    date: str
    category: str = None
    investment_type: str = None
