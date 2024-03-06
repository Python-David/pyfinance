from datetime import datetime
from typing import Dict, Iterator, List, Optional, Tuple, Type, Union

from sqlalchemy import and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from database import SessionLocal
from models.expense import Expense
from models.finance_data import FinanceFilter, FinanceRecord
from models.investment import Investment
from views.utilities import validate_and_convert_date


class FinanceController:
    def __init__(self):
        # Initialize a new SQLAlchemy session
        self.db_session = SessionLocal()

    def add_finance_record(
        self,
        finance_record: FinanceRecord,
        record_class: Type[Union[Expense, Investment]],
    ) -> Tuple[bool, str]:
        date_obj, message = validate_and_convert_date(finance_record.date)
        if date_obj is None:
            return False, message
        try:
            if record_class == Expense:
                new_record = Expense(
                    user_id=finance_record.user_id,
                    category=finance_record.category,
                    amount=finance_record.amount,
                    date=date_obj,
                    description=finance_record.description,
                )
            elif record_class == Investment:
                new_record = Investment(
                    user_id=finance_record.user_id,
                    type=finance_record.investment_type,
                    amount=finance_record.amount,
                    date=date_obj,
                    description=finance_record.description,
                )
            else:
                return False, "Invalid record class."

            self.db_session.add(new_record)
            self.db_session.commit()
            return True, f"{record_class.__name__} added successfully."
        except IntegrityError as e:
            self.db_session.rollback()
            return (
                False,
                f"Failed to add {record_class.__name__.lower()}: a similar record already exists.",
            )
        except Exception as e:
            self.db_session.rollback()
            return False, f"Failed to add {record_class.__name__.lower()}: {e}"

    def get_expenses_by_category(
        self, finance_filter: FinanceFilter
    ) -> Iterator[Dict[str, float]]:
        """Yield expenses aggregated by category for a specific user, optionally filtered by year, month, and day."""
        try:
            query = self.db_session.query(
                Expense.category, func.sum(Expense.amount).label("total_amount")
            ).filter(Expense.user_id == finance_filter.user_id)

            # Apply filters based on provided arguments
            if finance_filter.year:
                query = query.filter(
                    func.extract("year", Expense.date) == finance_filter.year
                )
            if finance_filter.month:
                query = query.filter(
                    func.extract("month", Expense.date) == finance_filter.month
                )
            if finance_filter.day:
                query = query.filter(
                    func.extract("day", Expense.date) == finance_filter.day
                )

            query = query.group_by(Expense.category)

            for expense in query:
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

    def get_finance_records(
        self,
        finance_filter: FinanceFilter,
        record_class: Union[Type[Expense], Type[Investment]],
    ) -> List[Union[Expense, Investment]]:
        """Fetch finance records (expenses or investments) for a specific user, filtered by year, month, and day."""
        query: Query = self.db_session.query(record_class).filter(
            record_class.user_id == finance_filter.user_id
        )

        # Apply filters based on provided arguments
        if finance_filter.year:
            query = query.filter(
                func.extract("year", record_class.date) == finance_filter.year
            )
        if finance_filter.month:
            query = query.filter(
                func.extract("month", record_class.date) == finance_filter.month
            )
        if finance_filter.day:
            query = query.filter(
                func.extract("day", record_class.date) == finance_filter.day
            )

        # If no year, month, or day is specified, default to the current month and year
        if not any([finance_filter.year, finance_filter.month, finance_filter.day]):
            today = datetime.now()
            query = query.filter(
                and_(
                    func.extract("year", record_class.date) == today.year,
                    func.extract("month", record_class.date) == today.month,
                )
            )

        # Order by date for chronological listing
        return query.order_by(record_class.date.asc()).all()

    # Make sure to close the session when it's no longer needed
    def close_session(self) -> None:
        self.db_session.close()
