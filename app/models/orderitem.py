# coding: utf-8
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .base import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(String)
    title = Column(String)
    category_id = Column(String)
    variation_id = Column(Integer)
    warranty = Column(String)
    condition = Column(String)
    unit_price = Column(Integer)
    currency_id = Column(String)
    quantity = Column(Integer)
    requested_quantity = Column(JSON)
    sale_fee = Column(Integer)
    listing_type_id = Column(String)

    seller_id = Column(Integer)
    #seller_id = Column(Integer, ForeignKey('vendedor.id_ml'))

    #vendedor = relationship('Vendedor', lazy='subquery')
    order = relationship("Order", back_populates="order_items", lazy='subquery')
    #order = relationship("Order", lazy='subquery')
    