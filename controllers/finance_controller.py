from tracker.finance_tracker import FinanceTracker
from datetime import datetime


class FinanceController:
    def __init__(self):
        self.finance_tracker = FinanceTracker()

    def add_expense(self, user_id, category, amount, date_str):
        try:
            # date = datetime.strptime(date_str, '%Y-%m-%d').date()
            self.finance_tracker.add_expense(user_id, category, amount, date_str)
            return True, "Expense added successfully."
        except Exception as e:
            return False, str(e)

    def add_investment(self, user_id, investment_type, amount, date_str):
        try:
            # date = datetime.strptime(date_str, '%Y-%m-%d').date()
            self.finance_tracker.add_investment(user_id, investment_type, amount, date_str)
            return True, "Investment added successfully."
        except Exception as e:
            return False, str(e)

    def close_session(self):
        self.finance_tracker.close_session()
