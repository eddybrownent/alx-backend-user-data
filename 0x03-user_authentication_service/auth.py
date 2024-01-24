#!/usr/bin/env python3
"""
Authenitcation module
"""
from uuid import uuid4
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash the input password with bcrypt

    Args:
        password: password to be hashed

    Returns:
            bytes: salted hash of the password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates representation of a new UUID

    Returns:
        str: _description_
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
         Register a new user.

        Args:
            email: User's email
            password: User's password

        Returns:
            User: The newly registered user

        Raises:
            ValueError: If user with given email already exists
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if given  email & password equals a valid login

        Args:
            email: email of the user
            password: password to be checked

        Returns:
            bool: True if login is valid else False
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed = user.hashed_password
            entered_password = password.encode('utf-8')

            return bcrypt.checkpw(entered_password, hashed)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user

        Args:
            email: User's email

        Returns:
            str: Session ID

        Raises:
            ValueError: If user of the provided email is not found
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return

        session_id = _generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """
        Gets user based on the provided session ID

        Args:
            session_id: The session ID

        Returns:
            User or None: the User if found else None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id)
            return user
        except NoResultFound:
            return None
