from app.udaconnect.config import Base

from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
