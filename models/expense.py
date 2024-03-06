from sqlalchemy import (Column, Date, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="expenses")

    # Define a unique constraint for category, amount, date, and user_id
    __table_args__ = (
        UniqueConstraint(
            "category", "amount", "date", "user_id", name="unique_expense_constraint"
        ),
    )

    def __repr__(self):
        return f"<Expense(id={self.id}, category='{self.category}', amount={self.amount}, date='{self.date}')>"
