# coding: utf-8
from sqlalchemy import Column, Float, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(String, primary_key=True)
    category_id = Column(String)
    cost = Column(Float)
    price = Column(Float)
    title = Column(String)
    listing_type_id = Column(String)
    free_shipping = Column(String)
    shipping_free_cost = Column(Float)
    sale_fee = Column(Float)
    sales = Column(Integer)
    invoicing = Column(Float)
    seller = Column(ForeignKey('vendedor.id'))
    json = Column(String)

    vendedor = relationship('Vendedor')

    def __init__(self, id, category_id, cost, price, title, listing_type_id, free_shipping, shipping_free_cost, sale_fee, sales, invoicing, seller, json):
        self.id = id
        self.category_id = category_id
        self.cost = cost
        self.price = price
        self.title = title
        self.listing_type_id = listing_type_id
        self.free_shipping = free_shipping
        self.shipping_free_cost = shipping_free_cost
        self.sale_fee = sale_fee
        self.sales = sales
        self.invoicing = invoicing
        self.seller = seller
        self.json = json

    def __repr__(self):
        attr_list = [f"{attr}={getattr(self, attr)!r}" for attr in self.__dict__ if not attr.startswith('_')]
        return f"{self.__class__.__name__}({', '.join(attr_list)})"