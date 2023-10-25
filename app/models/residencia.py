# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

# Database ORMs
class Residencia(Base):
    __tablename__ = 'residencia'

    id = Column(Integer, primary_key = True)
    data_criacao = Column(DateTime)
    data_alteracao = Column(DateTime)
    id_usuario = Column(Integer)
    nome = Column(String(100))