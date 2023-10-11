from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(200))
    password = Column(String(200))
    craeted_at = Column(DateTime(), default=datetime.today())


class Email(Base):
    __tablename__ = 'email'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer())


class SendMessages(Base):
    __tablename__ = 'sendemail'

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    body = Column(String)
    send = Column(String, nullable=True)
