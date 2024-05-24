#!/usr/bin/env python3
"""
SessionExpAuth
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    def __init__(self):
        """Initialize SessionExpAuth instance
        """
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Create a session with expiration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        user_id = session_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id
        if 'created_at' not in session_dict:
            return None
        if session_dict.get('created_at') + \
            timedelta(seconds=self.session_duration) < \
                datetime.now():
            return None
        return user_id
