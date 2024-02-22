from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    expenses = relationship("Expense", back_populates="user")
    investments = relationship("Investment", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
