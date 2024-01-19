#!/usr/bin/env python3
"""
SessionAuth that inherits from Auth
"""
from models.user import User
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session-based Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user_id

        Args:
            user_id : user ID for which a session is to be created

        Returns:
            str: generated Session ID, otherwise None
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get User ID based on Session ID

        Args:
            session_id: Session ID for which linked User ID is to be retrieved

        Returns:
            str: User ID if the session_id is found in the dict, otherwise None
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        Get the current User based on the session cookie

        Args:
            request: Flask request object

        Returns:
            User: User instance if found, else None.
        """
        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
