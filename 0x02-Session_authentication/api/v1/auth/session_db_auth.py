#!/usr/bin/env python3
"""
Sessions in database
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    auth system based on Session ID stored in DB
    """
    def create_session(self, user_id=None) -> str:
        """
        Create new instance of UserSession with the session duration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return User ID by requesting UserSession in DB based on session_id
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None

        if self.session_duration <= 0:
            return user_session[0].user_id

        created_at = user_session[0].created_at

        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.utcnow():
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on Session ID
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = UserSession.search({'session_id': session_id})
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        user_id[0].remove()

        return True
