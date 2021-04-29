import os
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv


load_dotenv(verbose=True)
user = os.getenv('user')
password = os.getenv('pass')
host = os.getenv('host')
port = os.getenv('port')
database = os.getenv('database')

db_url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'

Base = declarative_base()
Session = sessionmaker()

class Lotto(Base):
    __tablename__ = 'lotto'
    round = Column(Integer, primary_key=True)
    date = Column(Date)
    first_count = Column(Integer)
    first_price = Column(Integer)
    second_count = Column(Integer)
    second_price = Column(Integer)
    third_count = Column(Integer)
    third_price = Column(Integer)
    fourth_count = Column(Integer)
    fourth_price = Column(Integer)
    fifth_count = Column(Integer)
    fifth_price = Column(Integer)
    num1 = Column(Integer)
    num2 = Column(Integer)
    num3 = Column(Integer)
    num4 = Column(Integer)
    num5 = Column(Integer)
    num6 = Column(Integer)
    bonus = Column(Integer)

db = create_engine(db_url, encoding='utf-8', pool_recycle=500)
Session.configure(bind=db, expire_on_commit=False)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
