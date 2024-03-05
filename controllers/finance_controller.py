from datetime import datetime
from typing import Dict, Iterator, List, Optional, Tuple

from sqlalchemy import and_, func
from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models.expense import Expense
from models.finance_record import FinanceRecord
from models.investment import Investment
from views.utilities import validate_and_convert_date


class FinanceController:
    def __init__(self):
        # Initialize a new SQLAlchemy session
        self.db_session = SessionLocal()

    def add_expense(self, expense_record: FinanceRecord) -> Tuple[bool, str]:
        date_obj, message = validate_and_convert_date(expense_record.date)
        if date_obj is None:
            return False, message
        try:
            new_expense = Expense(
                user_id=expense_record.user_id,
                category=expense_record.category,
                amount=expense_record.amount,
                date=date_obj
            )
            self.db_session.add(new_expense)
            self.db_session.commit()
            return True, "Expense added successfully."
        except IntegrityError as e:
            self.db_session.rollback()
            return False, "Failed to add expense: a similar expense already exists."
        except Exception as e:
            self.db_session.rollback()
            return False, f"Failed to add expense: {e}"

    def add_investment(self, investment_record: FinanceRecord) -> Tuple[bool, str]:
        date_obj, message = validate_and_convert_date(investment_record.date)
        if date_obj is None:
            return False, message
        try:
            new_investment = Investment(
                user_id=investment_record.user_id,
                type=investment_record.investment_type,
                amount=investment_record.amount,
                date=date_obj
            )
            self.db_session.add(new_investment)
            self.db_session.commit()
            return True, "Investment added successfully."
        except IntegrityError as e:
            self.db_session.rollback()
            return False, "Failed to add investment: a similar investment already exists."
        except Exception as e:
            self.db_session.rollback()
            return False, f"Failed to add investment: {e}"

    def get_expenses_by_category(self, user_id: int) -> Iterator[Dict[str, float]]:
        """Yield expenses aggregated by category for a specific user using a generator."""
        try:
            # Query to aggregate expenses by category
            expenses_by_category_query = (
                self.db_session.query(
                    Expense.category, func.sum(Expense.amount).label("total_amount")
                )
                .filter(Expense.user_id == user_id)
                .group_by(Expense.category)
            )

            # Use a generator to yield each result one at a time
            for expense in expenses_by_category_query:
                yield {
                    "category": expense.category,
                    "total_amount": float(expense.total_amount),
                }

        except Exception as e:
            self.db_session.rollback()
            yield {
                "error": True,
                "message": f"Failed to fetch expenses by category: {e}",
            }

    def get_expenses(
        self,
        user_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
    ) -> List[Expense]:
        """Fetch expenses for a specific user, filtered by year, month, and day, all optional."""
        query = self.db_session.query(Expense).filter(Expense.user_id == user_id)

        # Apply filters based on provided arguments
        if year:
            query = query.filter(func.extract("year", Expense.date) == year)
        if month:
            query = query.filter(func.extract("month", Expense.date) == month)
        if day:
            query = query.filter(func.extract("day", Expense.date) == day)

        # If no year, month, or day is specified, default to the current month and year
        if not any([year, month, day]):
            today = datetime.now()
            query = query.filter(
                and_(
                    func.extract("year", Expense.date) == today.year,
                    func.extract("month", Expense.date) == today.month,
                )
            )

        # Order by date for chronological listing
        query = query.order_by(Expense.date.asc())

        return query.all()

    # Make sure to close the session when it's no longer needed
    def close_session(self) -> None:
        self.db_session.close()
