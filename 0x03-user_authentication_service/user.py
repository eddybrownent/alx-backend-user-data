#!/usr/bin/env python3
"""
SQLAlchemy model
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    Class User
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    sesssion_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
