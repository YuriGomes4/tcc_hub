# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

# Database ORMs
class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key = True)
    data_criacao = Column(DateTime)
    data_alteracao = Column(DateTime)
    id_publico = Column(String(50), unique = True)
    nome = Column(String(100))
    email = Column(String(70), unique = True)
    senha = Column(String(80))