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

    def is_session_valid(self, session_token):
        return self.user_controller.is_session_valid(session_token)

    def get_user_id_from_session(self, session_token):
        return self.user_controller.get_user_id_from_session(session_token)

    def close_sessions(self):
        self.finance_controller.close_session()
        self.user_controller.close_session()
