from tracker.finance_tracker import FinanceTracker
from datetime import datetime


class FinanceController:
    def __init__(self):
        self.finance_tracker = FinanceTracker()

    def add_expense(self, user_id, category, amount, date_str):
        success, message = self.finance_tracker.add_expense(user_id, category, amount, date_str)
        return success, message

    def add_investment(self, user_id, investment_type, amount, date_str, returns=None):
        success, message = self.finance_tracker.add_investment(user_id, investment_type, amount, date_str, returns)
        return success, message

    def get_expenses_by_category(self, user_id):
        expenses = self.finance_tracker.get_expenses_by_category(user_id)
        return expenses

    def get_expenses(self, user_id, year=None, month=None, day=None):
        expenses = self.finance_tracker.get_expenses(user_id, year, month, day)
        return expenses

    def close_session(self):
        self.finance_tracker.close_session()
