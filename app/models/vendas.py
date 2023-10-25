# coding: utf-8
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .base import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_closed = Column(DateTime)
    last_updated = Column(DateTime)
    manufacturing_ending_date = Column(DateTime)
    comment = Column(String)
    pack_id = Column(Integer)
    pickup_id = Column(Integer)
    total_amount = Column(Integer)
    paid_amount = Column(Integer)
    expiration_date = Column(DateTime)
    currency_id = Column(String)
    status = Column(String)
    status_detail = Column(String)
    shipping = Column(String)
    json = Column(String)

    buyer_id = Column(ForeignKey('buyer.id'))
    seller_id = Column(ForeignKey('vendedor.id_ml'))

    buyer = relationship("Buyer", lazy='subquery')
    vendedor = relationship('Vendedor', lazy='subquery')
    order_items = relationship("OrderItem", back_populates="order", lazy='subquery')
    payments = relationship("Payment", back_populates="order", lazy='subquery')
