from sqlalchemy import Integer, Column, String, Text, Date
from connection.database import Base

class Data(Base):
    __tablename__ = "extracteddata"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    problem = Column(Text, nullable=False)
    submission_date = Column(Date, nullable=False)
