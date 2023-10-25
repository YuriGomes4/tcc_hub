# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

# Database ORMs
class Log_Exec(Base):
    __tablename__ = 'log_exec'

    id = Column(Integer, primary_key = True)
    data_criacao = Column(DateTime)
    data_alteracao = Column(DateTime)
    id_residencia = Column(Integer)
    id_area_residencia = Column(Integer)
    id_dispositivo = Column(Integer)
    acao = Column(String)
    status = Column(String)