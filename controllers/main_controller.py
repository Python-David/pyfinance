from controllers.finance_controller import FinanceController
from controllers.user_controller import UserController


class MainController:
    def __init__(self):
        self.finance_controller = FinanceController()
        self.user_controller = UserController()
        self.current_user_id = None

    def add_expense(self, user_id, category, amount, date_str):
        return self.finance_controller.add_expense(user_id, category, amount, date_str)

    def add_investment(self, user_id, investment_type, amount, date_str):
        return self.finance_controller.add_investment(user_id, investment_type, amount, date_str)

    def register_new_user(self, name, email, password):
        return self.user_controller.register_new_user(name, email, password)

    def validate_login(self, email, password):
        return self.user_controller.validate_login(email, password)

    def close_sessions(self):
        self.finance_controller.close_session()
        self.user_controller.close_session()
