
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Date, DateTime 
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import re
from pandas import *
engine = create_engine('mysql://jfields:c@keandc00kies@localhost/cchdo_test')
Base = declarative_base()

class Click(Base):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True)
    expocode = Column(String(32))
    date = Column(Date)
    user = Column(String(32))
    location = Column(String(32))
    source_location = Column(String(32))
    file_type = Column(String(32))

if __name__ == "__main__":
    print "Checking table settings."
    Base.metadata.create_all(engine)
