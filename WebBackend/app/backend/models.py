import sqlalchemy
import pandas
from sqlalchemy.ext.automap import automap_base
import os
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Column, Integer, String, Table, MetaData
import json
import datetime


class Infection(BaseModel):
    infection_date: datetime.datetime
    school: str
    school_class: str



class Database:
    def connect(self, schema='public'):
        raise NotImplementedError

    def disconnect(self):
        self.session.close()


class InfectionsTable(Database):
    def connect(self, schema='public'):
        path = os.path.join(os.getenv('LOCAL_DB_PATH'), os.getenv('LOCAL_IPIOJO_DB_FILENAME'))
        os.makedirs(os.getenv('LOCAL_DB_PATH'), exist_ok=True)
        
        Base = declarative_base()
        self.engine = sqlalchemy.create_engine(f'sqlite:///{path}')

        metadata = MetaData()
        Table(
            'infections', metadata, 
            Column('id', Integer, primary_key=True), 
            Column('infection_date', DateTime),
            Column('school', String),
            Column('school_class', String)
        )

        metadata.create_all(self.engine)
        Base = automap_base(metadata=metadata)
        Base.prepare()

        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = Session()
        self.Table = Base.classes.infections

    def get_all_infections(self):
        self.connect()
        query = self.session.query(self.Table.infection_date, sqlalchemy.func.count(self.Table.infection_date).label("count"))
        query = query.group_by(self.Table.infection_date).order_by(sqlalchemy.desc("infection_date"))
        data = pandas.read_sql(query.statement, query.session.bind)
        self.disconnect()
        return data

    def report_infection(self):
        self.connect()
        data = {
            'infection_date': datetime.datetime.now().date(),
            'school': "Rufino Blanco",
            'school_class': "Infantil 5 años A"
        }
        row = self.Table(**data)
        self.session.add(row)
        self.session.flush()
        self.session.commit()
        query = self.session.query(self.Table)
        data = pandas.read_sql(query.statement, query.session.bind)
        print(data)
        self.disconnect()
        return True
