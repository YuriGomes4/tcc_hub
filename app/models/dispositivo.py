# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .base import Base

# Database ORMs
class Dispositivo(Base):
    __tablename__ = 'dispositivo'

    id = Column(Integer, primary_key = True)
    data_criacao = Column(DateTime)
    data_alteracao = Column(DateTime)
    id_residencia = Column(Integer)
    id_area_residencia = Column(Integer)
    tipo = Column(String)
    nome = Column(String(100))
    codigo = Column(String)
    info = Column(JSON)