from sqlalchemy import Integer, Column, String
from connection.database import Base

class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)

