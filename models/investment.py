from sqlalchemy import (Column, Date, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from base import Base


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    returns = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="investments")

    # Define a unique constraint for category, amount, date, and user_id
    __table_args__ = (
        UniqueConstraint(
            "type", "amount", "date", "user_id", name="unique_investment_constraint"
        ),
    )

    def __repr__(self):
        return f"<Investment(id={self.id}, type='{self.type}', amount={self.amount}, date='{self.date}', returns={self.returns})>"
