from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class Investment(Base):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    returns = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="investments")

    def __repr__(self):
        return f"<Investment(id={self.id}, type='{self.type}', amount={self.amount}, date='{self.date}', returns={self.returns})>"
