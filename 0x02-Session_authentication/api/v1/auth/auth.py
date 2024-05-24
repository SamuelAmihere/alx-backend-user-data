#!/usr/bin/env python3
"""
The authentication module.
"""
from os import getenv
from flask import request
from typing import List, TypeVar
from models.user import User
import fnmatch


class Auth:
    """The authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """The require_auth method.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Ensure path ends with a '/'
        path = path + '/' if not path.endswith('/') else path

        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """The authorization_header method.
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """The current_user method.
        """
        return None


    def session_cookie(self, request=None):
        """Returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
