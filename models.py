from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Certificate(Base):
    __tablename__ = "certificate"  # matches your existing table

    id = Column(Integer, primary_key=True, autoincrement=True)
    cn = Column(String, nullable=False)
    expiry = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
