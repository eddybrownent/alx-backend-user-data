#!/usr/bin/env python3
"""
Authenitcation module
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """
    Generates representation of a new UUID

    Returns:
        str: _description_
    """
    id = uuid4()
    return str(id)


def _hash_password(password: str) -> bytes:
    """
    Hash the input password with bcrypt

    Args:
        password: password to be hashed

    Returns:
            bytes: salted hash of the password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        try:
            user = self._db.find_user_by(email=email)
            hashed = user.hashed_password
            entered_password = password.encode('utf-8')

            return bcrypt.checkpw(entered_password, hashed)
        except Exception:
            return False
