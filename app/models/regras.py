# coding: utf-8
from sqlalchemy import Column, Float, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Regra(Base):
    __tablename__ = 'regras'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_id_obj = Column(String)
    tabela_obj = Column(String)
    coluna_obj = Column(String)
    valor_obj = Column(String)
    operador = Column(String)
    ref_id_new = Column(String)
    tabela_new = Column(String)
    coluna_new = Column(String)
    valor_new = Column(String)
    funcao = Column(String)
    feito = Column(Boolean)

    def __repr__(self):
        attr_list = [f"{attr}={getattr(self, attr)!r}" for attr in self.__dict__ if not attr.startswith('_')]
        return f"{self.__class__.__name__}({', '.join(attr_list)})"