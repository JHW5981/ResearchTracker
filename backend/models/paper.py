from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    abstract = Column(Text)
    url = Column(String(1000))
    source = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)