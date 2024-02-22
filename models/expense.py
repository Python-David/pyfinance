from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(id={self.id}, category='{self.category}', amount={self.amount}, date='{self.date}')>"
