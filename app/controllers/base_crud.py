
from operator import and_
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from alembic.config import Config

class CRUDBase:
    def __init__(self, class_model, class_schema):
        alembic_cfg = Config("alembic.ini")  # Caminho para o arquivo alembic.ini
        self.engine = create_engine(alembic_cfg.get_section_option("alembic", "sqlalchemy.url"))
        self.Session = sessionmaker(bind=self.engine)
        self.class_model = class_model
        self.class_schema = class_schema
    
    def create(self, **kwargs):
        obj = self.class_model(**kwargs)
        session = self.Session()
        session.add(obj)
        session.commit()
        session.close()
    
    def read(self, schema=None, **kwargs):
        session = self.Session()
        result = session.query(self.class_model).filter_by(**kwargs).first()
        session.close()

        if schema:
            if type(result) == list:
                result = self.class_schema().dump(result, many=True)
            else:
                result = self.class_schema().dump(result)

        return result
    
    def read_multi(self, schema=None, date_created=None, **kwargs):
        session = self.Session()
        query = session.query(self.class_model)
        
        if date_created:
            date_from, date_to = date_created
            query = query.filter(and_(
                self.class_model.date_created >= date_from,
                self.class_model.date_created <= date_to
            ))
        
        result = query.filter_by(**kwargs).all()
        session.close()

        if schema:
            result = self.class_schema().dump(result, many=True)

        return result
    
    def read_ids(self, schema=None):
        session = self.Session()
        result = session.query(self.class_model.id).all()
        session.close()

        if schema:
            result = self.class_schema().dump(result)
        else:
            newresult = []
            for item in result:
                newresult.append(str(item[0]))

            result = newresult
        return result
    
    def update(self, obj):
        session = self.Session()
        session.merge(obj)
        session.commit()
        session.close()
    
    def delete(self, **kwargs):
        session = self.Session()
        session.query(self.class_model).filter_by(**kwargs).delete()
        #session.delete(obj)
        session.commit()
        session.close()