

from sqlalchemy import Column, Integer, String, Text, Date
from connection.database import Base

class ClassifiedDataByPriority(Base): 
    __tablename__ = "classified_data_by_priority_and_problem"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    problem = Column(Text, nullable=False)
    submission_date = Column(Date, nullable=False)
    problem_priority = Column(String, nullable=False)
    problem_type = Column(String, nullable=False)



