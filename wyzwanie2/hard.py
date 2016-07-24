from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///test.db")
Base = declarative_base()


class Entry(Base):
    __tablename__ = "Objects"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    type = Column(String)
    size = Column(Integer)


Base.metadata.create_all(engine)
