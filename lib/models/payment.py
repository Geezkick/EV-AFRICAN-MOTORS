# lib/models/payment.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(String, nullable=False, default="completed")
    vehicle = relationship("Vehicle", back_populates="payments")
    customer = relationship("Customer", back_populates="payments")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Payment amount must be a positive number")
        self._amount = float(value)
