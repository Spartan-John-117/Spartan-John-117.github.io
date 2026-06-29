from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    login = Column(String(30), nullable=False, unique=True)
    desc = Column(Text, nullable=True)

# Créez la base de données si nécessaire
def init_db():
    engine = create_engine('sqlite:///model/logins.db')
    Base.metadata.create_all(engine)

