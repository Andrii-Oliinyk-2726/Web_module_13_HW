import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, event, Date, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, index=True)
    birthday = Column(Date)
    add_info = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)



