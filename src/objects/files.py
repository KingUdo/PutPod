from sqlalchemy import Column, Text
from misc.database import Base

class Files(Base):
    __tablename__ = 'files'
    hash = Column(Text, primary_key=True)
    date = Column(Text)
    name = Column(Text)
    source_ip = Column(Text)