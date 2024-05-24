#!/usr/bin/env python3
"""
SessionDBAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """Create a session and store it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID from the
         request cookie
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
