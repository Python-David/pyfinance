from database import SessionLocal
from models.expense import Expense
from models.investment import Investment


class FinanceTracker:
    def __init__(self):
        # Initialize a new SQLAlchemy session
        self.db_session = SessionLocal()

    def add_expense(self, user_id, category, amount, date):
        try:
            new_expense = Expense(user_id=user_id, category=category, amount=amount, date=date)
            self.db_session.add(new_expense)
            self.db_session.commit()
            return True, "Expense added successfully."
        except Exception as e:
            self.db_session.rollback()  # Rollback the session to undo the operation in case of error
            return False, f"Failed to add expense: {e}"

    def add_investment(self, user_id, type, amount, date, returns=None):
        try:
            new_investment = Investment(user_id=user_id, type=type, amount=amount, date=date, returns=returns)
            self.db_session.add(new_investment)
            self.db_session.commit()
            return True, "Investment added successfully."
        except Exception as e:
            self.db_session.rollback()  # Rollback in case of an error
            return False, f"Failed to add investment: {e}"

    # Make sure to close the session when it's no longer needed
    def close_session(self):
        self.db_session.close()
