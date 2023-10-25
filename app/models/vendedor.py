# coding: utf-8
from sqlalchemy import Column, Integer, String, DateTime
#from sqlalchemy.orm import relationship
from .base import Base

class Vendedor(Base):
    __tablename__ = 'vendedor'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    client_ml = Column(String)
    secret_ml = Column(String)
    id_ml = Column(String)
    refresh_tk_ml = Column(String)
    tk_ml = Column(String)
    tk_tiny = Column(String)
    last_updated = Column(DateTime)
