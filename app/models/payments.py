# coding: utf-8
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .base import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    payer_id = Column(Integer)
    payment_method_id = Column(String)
    currency_id = Column(String)
    transaction_amount = Column(Integer)
    status = Column(String)

    order = relationship("Order", back_populates="payments", lazy='subquery')