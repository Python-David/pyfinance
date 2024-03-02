from typing import Dict, Iterable, List, Optional, Tuple

from controllers.finance_controller import FinanceController
from controllers.user_controller import UserController
from models import Expense


class MainController:
    def __init__(self):
        self.finance_controller: FinanceController = FinanceController()
        self.user_controller: UserController = UserController()
        self.current_user_id: Optional[int] = None

    def add_expense(
        self, user_id: int, category: str, amount: float, date_str: str
    ) -> Tuple[bool, str]:
        return self.finance_controller.add_expense(user_id, category, amount, date_str)

    def add_investment(
        self, user_id: int, investment_type: str, amount: float, date_str: str
    ) -> Tuple[bool, str]:
        return self.finance_controller.add_investment(
            user_id, investment_type, amount, date_str
        )

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
