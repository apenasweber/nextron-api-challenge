from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Expression(Base):
    __tablename__ = "expression"
    id = Column(Integer, primary_key=True, index=True, name="id")
    expression = Column(String, nullable=False, name="expression")
    result = Column(Boolean, nullable=True, name="result", default=None)


