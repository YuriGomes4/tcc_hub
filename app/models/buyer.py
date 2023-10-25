# coding: utf-8
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .base import Base

class Buyer(Base):
    __tablename__ = 'buyer'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    first_name = Column(String)
    last_name = Column(String)