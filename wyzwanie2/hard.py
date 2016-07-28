import os
import hashlib
import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def check_entry_type(entry):
    if entry.is_symlink():
        return "o"
    elif entry.is_file():
        return "f"
    elif entry.is_dir():
        return "d"
    else:
        return "o"


def count_directory_contents(entry):
    return len(os.scandir(entry.path))


def get_directory_size(entry):
    return sum(item.stat().st_size for item in os.scandir(entry.path))


def get_checksum(entry):
    return hashlib.md5(open(entry.path, 'rb').read()).hexdigest()


Base = declarative_base()


class Entry(Base):

    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    type = Column(String)
    size = Column(Integer)


class Cardinality(Base):

    __tablename__ = 'cardinality'

    id = Column(Integer, ForeignKey("objects.id"), primary_key=True, autoincrement=False)
    nbr_of_elements = Column(Integer)


class Checksum(Base):

    __tablename__ = 'checksums'

    id = Column(Integer, ForeignKey("objects.id"), primary_key=True, autoincrement=False)
    checksum = Column(String)


engine = create_engine("sqlite:///" + sys.argv[2] + ".db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


directory_contents = os.scandir(sys.argv[1])
for entry in directory_contents:
    entry_type = check_entry_type(entry)
    if entry_type == "d":
        item = Entry(path=entry.path, type=entry_type, size=get_directory_size(entry))
        session.add(item)
        session.commit()
        session.add(Cardinality(id=session.query(Entry).filter_by(path=entry.path).first().id,
                                nbr_of_elements=count_directory_contents(entry)))
        session.commit()
    elif entry_type == "f":
        item = Entry(path=entry.path, type=entry_type, size=entry.stat().st_size)
        session.add(item)
        session.commit()
        session.add(Checksum(id=session.query(Entry).filter_by(path=entry.path).first().id,
                             checksum=get_checksum(entry)))
    else:
        item = Entry(path=entry.path, type=entry_type, size=entry.stat().st_size)
        session.add(item)
        session.commit()




