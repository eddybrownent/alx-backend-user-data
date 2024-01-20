#!/usr/bin/env python3
"""
model UserSession
"""
from models.base import Base


class UserSession(Base):
    """
    Usersession class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Usersession initilizer
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
