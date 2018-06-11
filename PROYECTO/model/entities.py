from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship
from database import connector

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(12))

class Curso(connector.Manager.Base):
    __tablename__ = 'curso'
    id = Column(Integer, primary_key=True)
    subject = Column(String(50))

