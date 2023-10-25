# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

# Database ORMs
class Area_Residencia(Base):
    __tablename__ = 'area_residencia'

    id = Column(Integer, primary_key = True)
    data_criacao = Column(DateTime)
    data_alteracao = Column(DateTime)
    id_residencia = Column(Integer)
    nome = Column(String(100))