# coding: utf-8
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .base import Base

class Historico(Base):
    __tablename__ = 'historico'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    seller = Column(String)
    type = Column(String)
    ref_id = Column(String)
    change = Column(String)
    old_value = Column(String)
    new_value = Column(String)