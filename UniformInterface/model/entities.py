from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import connector


class User(connector.Manager.Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    cursos=relationship("Curso", backref="user")


class Curso(connector.Manager.Base):
    __tablename__ = 'curso'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_id=Column(Integer, ForeignKey('user.id'))
    notas=relationship("Nota", backref="curso")


class Nota(connector.Manager.Base):
    __tablename__ = 'nota'
    id = Column(Integer, primary_key=True)
    variable = Column(String(50))
    nota= Column(Integer)
    porcentaje = Column(Integer)
    curso_id=Column(Integer, ForeignKey('curso.id'))


