from typing import Dict, Iterable, List, Optional, Tuple

from controllers.finance_controller import FinanceController
from controllers.user_controller import UserController
from models import Expense
from models.finance_record import FinanceRecord


class MainController:
    def __init__(self):
        self.finance_controller: FinanceController = FinanceController()
        self.user_controller: UserController = UserController()
        self.current_user_id: Optional[int] = None

    def add_expense(self, expense_record: FinanceRecord) -> Tuple[bool, str]:
        return self.finance_controller.add_expense(expense_record)

    def add_investment(self, investment_record: FinanceRecord) -> Tuple[bool, str]:
        return self.finance_controller.add_investment(investment_record)

    def register_new_user(
        self, name: str, email: str, password: str
    ) -> Tuple[bool, str]:
        return self.user_controller.register_new_user(name, email, password)

    def validate_login(
        self, email: str, password: str
    ) -> Tuple[bool, str, Optional[str]]:
        return self.user_controller.validate_login(email, password)

    def is_session_valid(self, session_token: str) -> bool:
        return self.user_controller.is_session_valid(session_token)

    def get_user_id_from_session(self, session_token: str) -> Optional[int]:
        return self.user_controller.get_user_id_from_session(session_token)

    def get_expenses_by_category(self, user_id: int) -> Iterable[Dict[str, float]]:
        return self.finance_controller.get_expenses_by_category(user_id)

    def get_expenses(
        self,
        user_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
    ) -> List[Expense]:
        return self.finance_controller.get_expenses(user_id, year, month, day)

    def close_sessions(self) -> None:
        self.finance_controller.close_session()
        self.user_controller.close_session()
